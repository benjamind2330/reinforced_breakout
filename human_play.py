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
SCREEN_SIZE       = vec2(800, 600)
BRICK_ROWS        = 6
BRICK_SIZE        = vec2(64, 24)
PADDLE_SIZE       = vec2(50, 16)
BALL_RADIUS       = 8
PADDLE_SPEED      = 420.0
BALL_INITIAL_VEL  = vec2(180, -240)
SIM_HZ            = 500          # fixed simulation rate (physics/logic)
RENDER_HZ         = 50           # target render rate
SIM_DT            = 1.0 / SIM_HZ
RENDER_DT         = 1.0 / RENDER_HZ
WINDOW_SCALE      = 1  # keep 1 unless you switch to logical coords
CAPTION           = "Breakout (Human Play)"
MAX_FRAME_SKIP    = 5            # safety clamp to avoid spiral of death
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

    sim_accumulator = 0.0
    render_accumulator = 0.0
    last_time = time.perf_counter()

    running = True
    while running:
        now = time.perf_counter()
        frame_dt = now - last_time
        last_time = now

        # Clamp dt in case of long pause (e.g., debugger break)
        if frame_dt > 0.25:
            frame_dt = 0.25

        sim_accumulator += frame_dt
        render_accumulator += frame_dt

        # Poll input once per outer loop; action reused for all sim steps this frame
        action = disp.poll_input()

        # Run up to MAX_FRAME_SKIP simulation steps to catch up
        steps = 0
        while sim_accumulator >= SIM_DT and steps < MAX_FRAME_SKIP:
            game.step(SIM_DT, action)
            sim_accumulator -= SIM_DT
            steps += 1

        # If we fell badly behind, drop leftover time (prevents spiral of death)
        if steps == MAX_FRAME_SKIP and sim_accumulator >= SIM_DT:
            sim_accumulator = 0.0

        # Render at fixed render cadence
        if render_accumulator >= RENDER_DT:
            disp.render()
            render_accumulator %= RENDER_DT  # keep fractional remainder

        # Post-win/loss handling
        if game.win_state != WinState.ONGOING:
            exit(0)

        # Small sleep to ease CPU usage (tunable)
        time.sleep(0.0001)

if __name__ == "__main__":
    main()