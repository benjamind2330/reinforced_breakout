from physics.vec2 import vec2

SCREEN_SIZE       = vec2(800, 600)
BRICK_ROWS        = 6
BRICK_SIZE        = vec2(64, 24)
PADDLE_SIZE       = vec2(50, 16)
BALL_RADIUS       = 8
PADDLE_SPEED      = 420.0
BALL_INITIAL_VEL  = vec2(180, -240)
SIM_HZ            = 500          # fixed simulation rate (physics/logic)
SIM_DT            = 1.0 / SIM_HZ