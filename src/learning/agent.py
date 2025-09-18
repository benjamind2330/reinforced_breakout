from .model import Linear_QNet, QTrainer, RUN_DEVICE
from .plotting import plotter

import torch
import random
import numpy as np
from collections import deque
from game.breakout_sim import breakout_sim, paddle_move, WinState, GameState
from game.constants import *
from time import time
from datetime import timedelta

MAX_MEMORY = 100_000
SHORT_BATCH_SIZE = 10
BATCH_SIZE = 1000
LR = 0.001
MAX_GAME_TIME = 300.0  # seconds
HIDDEN_NODES = 256
DISCOUNT_FACTOR = 0.9
DISPLAY_RENDER_DT = 1.0 / 30.0  # seconds
NUM_EPISODES = 10
EPISODES_FOR_EXPLORATION = 1

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = DISCOUNT_FACTOR  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        # Placeholder for model and trainer
        self.model = Linear_QNet(input_size=5 + BRICK_ROWS * (SCREEN_SIZE.x // BRICK_SIZE.x), hidden_size=HIDDEN_NODES, output_size=3)
        self.model.load()  # load existing model if available
        self.trainer = QTrainer(model=self.model, lr=LR, gamma=self.gamma)
        self._device = RUN_DEVICE
        self.short_mem = []

    def remember(self, state: np.ndarray, action: float, reward: float, next_state: np.ndarray, done: bool):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state: np.ndarray, action: float, reward: float, next_state: np.ndarray, done: bool):
        self.short_mem.append((state, action, reward, next_state, done))
        if len(self.short_mem) >= SHORT_BATCH_SIZE or done:
            states, actions, rewards, next_states, dones = zip(*self.short_mem)
            self.trainer.train_step(states, actions, rewards, next_states, dones)
            self.short_mem.clear()

    def get_action(self, state: np.ndarray, game_state: GameState) -> np.ndarray:
        self.epsilon = EPISODES_FOR_EXPLORATION - self.n_games
        move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            # move the paddle towards the ball
            ball_x = game_state.ball.position.x
            paddle_x = game_state.paddle.position.x
            if ball_x < paddle_x:
                move[0] = 1  # move left
            elif ball_x > paddle_x:
                move[2] = 1  # move right
            else:
                move[1] = 1  # stay
        else:
            state0 = torch.tensor(state, dtype=torch.float, device=self._device)
            prediction = self.model(state0)
            move_index = torch.argmax(prediction).item()
            move[move_index] = 1
        return np.array(move)

def to_reward(state: GameState, last_state: GameState) -> float:
    if state.win_state == WinState.WON:
        return 1.0
    elif state.win_state == WinState.LOST:
        return -1.0
   
    if (state.num_bricks_left() < last_state.num_bricks_left()):
        return 0.1  # small reward for breaking a brick
    return 0.0

def to_state_vector(state: GameState) -> np.ndarray:
    ball = state.ball
    paddle = state.paddle
    bricks = state.bricks

    # Ball position and velocity
    ball_x = ball.position.x / SCREEN_SIZE.x
    ball_y = ball.position.y / SCREEN_SIZE.y
    ball_vx = (ball.velocity.x + BALL_INITIAL_VEL.x) / (2 * BALL_INITIAL_VEL.x)
    ball_vy = (ball.velocity.y + BALL_INITIAL_VEL.y) / (2 * BALL_INITIAL_VEL.y)

    # Paddle position
    paddle_x = paddle.position.x / SCREEN_SIZE.x

    # Bricks status (flattened)
    bricks_status = [1.0 if brick.alive else 0.0 for brick in bricks]
    
    state_vector = np.array([ball_x, ball_y, ball_vx, ball_vy, paddle_x] + bricks_status, dtype=float)
    return state_vector

def to_paddle_move(action: np.ndarray) -> paddle_move:
    move_index = np.argmax(action)
    if move_index == 0:
        return paddle_move.LEFT
    elif move_index == 1:
        return paddle_move.STAY
    else:
        return paddle_move.RIGHT

def make_game() -> breakout_sim:
    return breakout_sim(size=SCREEN_SIZE, brick_rows=BRICK_ROWS, brick_size=BRICK_SIZE, paddle_size=PADDLE_SIZE, ball_radius=BALL_RADIUS, paddle_vel=PADDLE_SPEED)

class score:
    def __init__(self, game_state: GameState = None):
        self.percentage_broken = 0.0
        self.time = 0.0
        if game_state is not None:
            self.percentage_broken = game_state.num_bricks_broken() / game_state.num_bricks_total() * 100
            self.time = game_state.game_time

    def __repr__(self):
        return f"(%_broke={self.percentage_broken:.2f}, t={self.time:.2f})"
    
    def __lt__(self, other):
        if self.percentage_broken == other.percentage_broken:
            return self.time > other.time  # less time is better
        return self.percentage_broken < other.percentage_broken  # more broken is better


def train(use_display: bool = False):
    a_plotter = plotter()
    record = score()
    agent = Agent()
    game = make_game()
    start_time = time()
    next_display_time = time() + DISPLAY_RENDER_DT
    if use_display:
        from display.display import breakout_display
        disp = breakout_display(game, scale=1, caption="Breakout (AI Training)")
    while agent.n_games < NUM_EPISODES:

        if use_display and time() >= next_display_time:
            disp.render()
            next_display_time =  time() + DISPLAY_RENDER_DT

        # get old state
        state_old = game.game_state()
        state_vector_old = to_state_vector(state_old)

        # get move
        action = agent.get_action(state_vector_old, state_old)
        paddle_action = to_paddle_move(action)
        
        # perform move and get new state
        state_new = game.step(SIM_DT, paddle_action=paddle_action)
        reward = to_reward(state_new, state_old)

        state_vector_new = to_state_vector(state_new)

        if state_new.game_time >= MAX_GAME_TIME:
            #force the game over if we took to long, we then get a punihment for being slow
            state_new.win_state = WinState.LOST

        is_game_over = state_new.win_state != WinState.ONGOING 

        # train short memory
        agent.train_short_memory(state_vector_old, action, reward, state_vector_new, is_game_over)

        # remember
        agent.remember(state_vector_old, action, reward, state_vector_new, is_game_over)

        if is_game_over:
            game = make_game()
            if use_display:
                disp.reset(game)
            # train long memory, plot result
            
            agent.n_games += 1
            agent.train_long_memory()

            new_score = score(state_new)
            if new_score > record:
                print("\nNew Record!")
                agent.model.save()
                record = new_score

            elapsed_time = time() - start_time
            time_p_run = elapsed_time / agent.n_games
            estimated_total_time = time_p_run * NUM_EPISODES
            remaining_time = estimated_total_time - elapsed_time

            print(f'({timedelta(seconds=int(elapsed_time))}: Rem: {timedelta(seconds=int(remaining_time))}: Avg {time_p_run}s) Game {agent.n_games} Result: {state_new.win_state} {new_score}, Record: {record}')
            a_plotter.add_score(new_score)
            a_plotter.plot()

