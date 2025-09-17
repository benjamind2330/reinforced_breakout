
from .ball import ball
from .paddle import paddle
from .brick import brick
from physics.intersections import intersects
from physics.vec2 import vec2
from enum import Enum

class paddle_move(Enum):
    LEFT = -1
    STAY = 0
    RIGHT = 1

class WinState(Enum):
    ONGOING = 0
    WON = 1
    LOST = 2

class GameState:

    def __init__(self, ball: ball, paddle: paddle, bricks: list[brick], win_state: WinState):
        self.ball = ball
        self.paddle = paddle
        self.bricks = bricks
        self.win_state = win_state
    
    def __repr__(self):
        return f"GameState(win_state={self.win_state}, num_bricks_left={sum(b.alive for b in self.bricks)})"


class breakout_sim:
    def __init__(self, size: vec2, brick_rows: int, brick_size: vec2, paddle_size: vec2, ball_radius: float, paddle_vel: float):
        self.size = size
        self.brick_rows = brick_rows
        self.brick_size = brick_size
        self.paddle_size = paddle_size
        self.ball_radius = ball_radius
        self.paddle_vel = paddle_vel
        self.win_state = WinState.ONGOING

        self.reset()

    def reset(self):
        self.ball = ball(position=vec2(self.size.x / 2, self.size.y / 2), radius=self.ball_radius)
        self.paddle = paddle(position=vec2(self.size.x / 2 - self.paddle_size.x / 2, self.size.y - self.paddle_size.y))
        self.bricks = [
            brick(position=vec2(col * self.brick_size.x, row * self.brick_size.y))
            for row in range(self.brick_rows)
            for col in range(self.size.x // self.brick_size.x)
        ]

    def game_state(self) -> GameState:
        return GameState(ball=self.ball, paddle=self.paddle, bricks=self.bricks, win_state=self.win_state)

    def step(self, dt: float, paddle_action: paddle_move) -> GameState:
        # Move paddle
        if paddle_action == paddle_move.LEFT:
            self.paddle.move(-self.paddle_vel * dt)
        elif paddle_action == paddle_move.RIGHT:
            self.paddle.move(self.paddle_vel * dt)

        # Update ball position
        self.ball.update(dt)

        # Check for wall collisions
        if self.ball.position.x - self.ball.radius < 0 or self.ball.position.x + self.ball.radius > self.size.x:
            self.ball.velocity.x *= -1  # Bounce off left/right walls
        if self.ball.position.y - self.ball.radius < 0:
            self.ball.velocity.y *= -1  # Bounce off top wall
        if self.ball.position.y + self.ball.radius > self.size.y:
            self.win_state = WinState.LOST  # Ball fell below paddle

        # Check for paddle collision
        if intersects(self.ball.shape, self.paddle.position):
            normal = vec2(0, -1)  # Normal pointing upwards
            self.ball.bounce(normal)

        # Check for brick collisions
        for brick in self.bricks:
            if brick.alive and intersects(self.ball.shape, brick.position):
                normal = brick.hit(self.ball.position)
                self.ball.bounce(normal)
                break  # Only handle one brick collision per step

        return self.game_state()
