from .ball import ball
from .paddle import paddle
from .brick import brick
from physics.intersections import intersects
from physics.vec2 import vec2
from physics.aabb import aabb
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
    def __init__(self, size: vec2, brick_rows: int, brick_size: vec2, paddle_size: vec2, ball_radius: float, paddle_vel: float,
                 ball_initial_velocity: vec2 | None = None):
        self.size = size
        self.brick_rows = brick_rows
        self.brick_size = brick_size
        self.paddle_size = paddle_size
        self.ball_radius = ball_radius
        self.paddle_vel = paddle_vel
        self.ball_initial_velocity = ball_initial_velocity or vec2(160, -200)
        self.win_state = WinState.ONGOING
        self.reset()

    def reset(self):
        # Center ball
        self.ball = ball(
            position=vec2(self.size.x / 2, self.size.y / 2),
            velocity=self.ball_initial_velocity,
            radius=self.ball_radius
        )

        paddle_centre = vec2(self.size.x / 2, self.size.y - self.paddle_size.y)
        self.paddle = paddle(position=paddle_centre, length=self.paddle_size.x, height=self.paddle_size.y)
        # Bricks laid out in grid
        top_offset = 20  # small gap from the top
        cols = int(self.size.x // self.brick_size.x)
        self.bricks = []
        for row in range(self.brick_rows):
            for col in range(cols):
                x0 = col * self.brick_size.x
                y0 = top_offset + row * self.brick_size.y
                x1 = x0 + self.brick_size.x
                y1 = y0 + self.brick_size.y
                self.bricks.append(brick(box=aabb(vec2(x0, y0), vec2(x1, y1))))

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

        # Check for paddle collision
        if intersects(self.ball.shape, self.paddle.aabb()):
            normal = vec2(0, -1)  # Normal pointing upwards
            self.ball.position.y = self.paddle.aabb().min.y - self.ball.radius - 1
            self.ball.bounce(normal)

        # Check for brick collisions
        for brick in self.bricks:
            if brick.alive and intersects(self.ball.shape, brick.box):
                normal = brick.hit(self.ball.position)
                self.ball.bounce(normal)
                break  # Only handle one brick collision per step

        # Check for wall collisions
        if self.ball.position.x - self.ball.radius < 0 or self.ball.position.x + self.ball.radius > self.size.x:
            self.ball.velocity.x *= -1  # Bounce off left/right walls
        if self.ball.position.y - self.ball.radius < 0:
            self.ball.velocity.y *= -1  # Bounce off top wall
        if self.ball.position.y + self.ball.radius > self.size.y:
            self.win_state = WinState.LOST  # Ball fell below paddle

        return self.game_state()
