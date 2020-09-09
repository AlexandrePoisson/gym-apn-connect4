import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

class ApnConnect4Env(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    self.n_col = 7
    self.n_raw = 6
    self.board = np.full((self.n_raw, self.n_col), 0)
    self.action_spaces = spaces.Discrete(14)
    self.player_turn = 1
    # 0 : player one column 0
    # 1 : player one column 1
    # 7 : player two column 0
    # 13 : player two column 7 

  def step(self, action):

    def connect4found(board, k):
        # TODO : update to search in diags
        res = [(board[j,i:i+4]==np.array([k, k, k, k])).all() for i in range(0,7-4) for j in range(0,6)]
        res.extend([(board[j:j+4,i]==np.array([k, k, k, k])).all() for i in range(0,7) for j in range(0,6-4)])
        connect4found = any(res)
        return connect4found

    def eval_reward(board):
        if connect4found(board,1):
          reward = 1
          done = True
        elif connect4found(board,2):
          reward = -1
          done = True
        else:
          reward = 0
          done = False
        return done, reward

    col_number = action % self.n_col
    value = action // self.n_col + 1

    j = 0

    while self.board[j][col_number] != 0:
      j = j + 1
    self.board[j][col_number] = value

    done, reward = eval_reward(self.board)
    observation = None

    if self.player_turn == 1:
      self.player_turn = 2
    
    else:
      self.player_turn = 1

    return observation, reward, done, None


  def is_legal_move(self, move):
    col_number = move % self.n_col
    if self.board[self.n_raw-1][col_number] != 0:
      return False
    
    elif self.player_turn == 1 and move >= self.n_col :
      return False

    elif self.player_turn == 2 and move < self.n_col :
      return False

    else:
      return True

  def reset(self):
    self.board = np.full((self.n_raw, self.n_col), 0)
    self.player_turn = 1


  def render(self, mode='human'):
    print("")
    print(self.board)


  def close(self):
    pass

