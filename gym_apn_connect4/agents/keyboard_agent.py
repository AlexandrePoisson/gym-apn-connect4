import argparse
import sys

import gym
from gym import wrappers, logger

class KeyboardAgent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space

    def act(self):
        nb = -1
        while not nb in self.action_space:
            nb = int(input('Choose a number: '))
        return nb

