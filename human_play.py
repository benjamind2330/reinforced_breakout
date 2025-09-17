"""
Human-playable Breakout launcher using breakout_sim + breakout_display.

Globals define tunable game parameters.
Run:
    PYTHONPATH=src python human_play.py
Controls:
    Left / A  - move paddle left
    Right / D - move paddle right
    Esc       - quit
"""
from physics.vec2 import vec2
from game.breakout_sim import breakout_sim, paddle_move, WinState
from display.display import breakout_display
import time

# ----------------- Global configuration -----------------
SCREEN_SIZE      = vec2(800, 600)
BRICK_ROWS       = 6
BRICK_SIZE       = vec2(64, 24)
PADDLE_SIZE      = vec2(96, 16)
BALL_RADIUS      = 8
PADDLE_SPEED     = 420.0
BALL_INITIAL_VEL = vec2(180, -240)
TARGET_FPS       = 60
WINDOW_SCALE     = 1  # keep 1 unless you switch to logical coords
CAPTION          = "Breakout (Human Play)"
# --------------------------------------------------------

def main():
    game = breakout_sim(
        size=SCREEN_SIZE,
        brick_rows=BRICK_ROWS,
        brick_size=BRICK_SIZE,
        paddle_size=PADDLE_SIZE,
        ball_radius=BALL_RADIUS,
        paddle_vel=PADDLE_SPEED,
        ball_initial_velocity=BALL_INITIAL_VEL
    )
    disp = breakout_display(game, scale=WINDOW_SCALE, caption=CAPTION)

    timestep = 1.0 / TARGET_FPS
    accumulator = 0.0
    last_time = time.perf_counter()

    # Simple fixed-step update with uncoupled rendering
    running = True
    while running:
        now = time.perf_counter()
        frame_dt = now - last_time
        last_time = now
        accumulator += frame_dt

        # Poll (latest) input once per frame
        action = disp.poll_input()

        # Fixed updates
        while accumulator >= timestep:
            game.step(timestep, action)
            accumulator -= timestep

        # Render latest state
        disp.render()

        if game.win_state != WinState.ONGOING:
            # Brief pause then reset (optional)
            time.sleep(1.0)

if __name__ == "__main__":
    main()