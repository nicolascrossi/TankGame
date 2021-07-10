import time
import random

import helperFunctions as hf
from aiMove import AIMove


class AI:

    def __init__(self, ai_tank, enemy_tank, enemy_shells, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.ai_tank = ai_tank
        self.enemy_tank = enemy_tank
        self.enemy_shells = enemy_shells

    def get_ai_actions(self):
        ai = AIMove()

        '''
        To implement your own ai, fill out the ai object created above. See the AIMove class for what functions are available
        '''

        return ai
