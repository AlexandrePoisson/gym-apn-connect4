import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import random


class ApnConnect4Env(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.n_col = 7
        self.n_raw = 6
        self.board = np.full((self.n_raw, self.n_col), 0, dtype=np.int8)
        self.action_space = spaces.Discrete(14)
        low = np.full((self.n_raw, self.n_col), 0, dtype=np.int8).reshape(self.n_raw * self.n_col)
        high = np.full((self.n_raw, self.n_col), 2, dtype=np.int8).reshape(self.n_raw * self.n_col)
        self.observation_space = spaces.Box(low, high, dtype=np.int8)
        self.player_turn = 1
        # 0 : player one column 0
        # 1 : player one column 1
        # 7 : player two column 0
        # 13 : player two column 7

    def step(self, action):

        def add_to_col(board, col, val):
            res = np.where(board[:, col] == 0)
            if res[0].size == 0:
                raise ValueError('Column is full')
            i_row = np.amin(res, axis=1)[0]
            board[i_row][col] = val
            return board

        def connect4found(board, k):
            # TODO : update to search in diags
            res = [(board[j, i:i + 4] == np.array([k, k, k, k])).all() for i in range(0, 7 - 4) for j in range(0, 6)]
            res.extend(
                [(board[j:j + 4, i] == np.array([k, k, k, k])).all() for i in range(0, 7) for j in range(0, 6 - 4)])
            connect4found = any(res)
            return connect4found

        def eval_reward(board):
            if connect4found(board, 1):
                #print("player 1 win")
                reward = 1
                done = True
            elif connect4found(board, 2):
                #print("player 2 win")

                reward = -1
                done = True
            elif len(self.get_legal_moves()) == 0:
                #print("draw")
                reward = 0.5
                done = True

            else:
                reward = 0
                done = False
            return done, reward

        legal_actions = self.get_legal_moves()
        if action not in legal_actions:
            print("an invalid action was selected")
            if len(legal_actions) > 0:
                action = random.choice(legal_actions)
            else:
                print("Invalid action and no more legal actions !!!")

        col_number = action % self.n_col
        value = action // self.n_col + 1

        try:
            add_to_col(self.board, col_number, value)
        except ValueError:
            print("unable to add to this column")

        done, reward = eval_reward(self.board)

        observation = self.board.reshape(self.n_raw * self.n_col)

        if self.player_turn == 1:
            self.player_turn = 2
        else:
            self.player_turn = 1
        return observation, reward, done, {}

    def get_legal_moves(self):
        res = np.where(self.board[self.n_raw - 1, :] == 0)
        if self.player_turn == 2:
            legal_moves = res[0] + self.n_col
        else:
            legal_moves = res[0]
        a = legal_moves.tolist()
        return a

    def is_legal_move(self, move):
        col_number = move % self.n_col
        if self.board[self.n_raw - 1][col_number] != 0:
            return False
        elif self.player_turn == 1 and move >= self.n_col:
            return False
        elif self.player_turn == 2 and move < self.n_col:
            return False
        else:
            return True

    def reset(self):
        self.board = np.full((self.n_raw, self.n_col), 0)
        self.player_turn = 1
        return self.board.reshape(self.n_raw * self.n_col)

    def render(self, mode='human'):
        print("")
        print(self.board)

    def close(self):
        pass
