import sys
from typing import Optional
import pygame
from physics.vec2 import vec2
from game.breakout_sim import breakout_sim, paddle_move, WinState

class breakout_display:
    """
    Lightweight pygame renderer / input helper for breakout_sim.
    Tolerates current inconsistencies in the codebase (vec2 vs aabb for paddle/brick).
    """

    def __init__(self, game: breakout_sim, scale: int = 1, caption: str = "Breakout"):
        self.game = game
        self.scale = scale
        self._screen = None
        self._font = None
        if pygame:
            pygame.init()
            w, h = int(game.size.x * scale), int(game.size.y * scale)
            self._screen = pygame.display.set_mode((w, h))
            pygame.display.set_caption(caption)
            self._font = pygame.font.SysFont("consolas", 14)
        self.colors = {
            "bg": (10, 10, 20),
            "brick": (200, 80, 50),
            "brick_dead": (40, 25, 20),
            "paddle": (80, 180, 220),
            "ball": (250, 250, 250),
            "text": (240, 240, 240),
        }

    # ------------- helpers -------------
    def _scale_pos(self, v: vec2) -> tuple[int, int]:
        return int(v.x * self.scale), int(v.y * self.scale)

    def _draw_aabb(self, box, color):
        if not pygame:
            return
        self._draw_rect(box.min, box.max - box.min, color)

    def _draw_rect(self, top_left: vec2, size: vec2, color):
        if not pygame:
            return
        x, y = self._scale_pos(top_left)
        w, h = int(size.x * self.scale), int(size.y * self.scale)
        pygame.draw.rect(self._screen, color, pygame.Rect(x, y, w, h))

    def _draw_ball(self, center: vec2, radius: float, color):
        if not pygame:
            return
        cx, cy = self._scale_pos(center)
        pygame.draw.circle(self._screen, color, (cx, cy), int(radius * self.scale))

    def _brick_top_left(self, b) -> vec2:
        # Brick.position may be:
        #  - vec2 (top-left) as currently constructed in breakout_sim.reset
        #  - aabb (with .min / .max) if later fixed
        pos = b.box
        if hasattr(pos, "min") and hasattr(pos, "max"):
            return pos.min
        return pos  # assume vec2 top-left

    # ------------- public API -------------
    def poll_input(self) -> Optional[paddle_move]:
        """
        Returns a paddle_move or None (no horizontal input).
        ESC or window close exits program.
        """
        if not pygame:
            return paddle_move.STAY
        move = paddle_move.STAY
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move = paddle_move.LEFT
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move = paddle_move.RIGHT
        return move

    def render(self):
        if not pygame:
            return
        gs = self.game.game_state()
        self._screen.fill(self.colors["bg"])

        # Draw bricks
        for br in gs.bricks:
            top_left = self._brick_top_left(br)
            color = self.colors["brick"] if br.alive else self.colors["brick_dead"]
            self._draw_rect(top_left, self.game.brick_size, color)

        # Draw paddle
        self._draw_aabb(self.game.paddle.aabb(), self.colors["paddle"])

        # Draw ball
        ball_obj = gs.ball
        # ball may expose .position or .shape.center
        center = getattr(ball_obj, "position", getattr(ball_obj.shape, "center", vec2(0, 0)))
        radius = getattr(ball_obj, "radius", getattr(ball_obj.shape, "radius", self.game.ball_radius))
        self._draw_ball(center, radius, self.colors["ball"])

        # Status text
        if self._font:
            status = f"Bricks:{sum(b.alive for b in gs.bricks)}  State:{gs.win_state.name}"
            txt = self._font.render(status, True, self.colors["text"])
            self._screen.blit(txt, (6, 4))

        pygame.display.flip()

    def run_blocking(self, fps: int = 60):
        """
        Convenience loop for manual inspection.
        """
        if not pygame:
            print("pygame not available; run_blocking skipped.")
            return
        clock = pygame.time.Clock()
        while self.game.win_state == WinState.ONGOING:
            dt = clock.tick(fps) / 1000.0
            action = self.poll_input()
            self.game.step(dt, action)
            self.render()

        # Final frame
        self.render()
        while True:
            for ev in pygame.event.get():
                if ev.type in (pygame.QUIT, pygame.KEYDOWN):
                    pygame.quit()
                    return