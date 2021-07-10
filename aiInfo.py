import random
import time
from typing import NewType

import helperFunctions as hf

class AIInfo:
    def __init__(self, ai_tank, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ai_tank = ai_tank

        self.new_dest()
        self.reset_travel_time()

    def new_dest(self):
        self.aiDest = (random.randint(50, self.screen_width - 50), random.randint(50, self.screen_height - 50))
        self.aiVels = hf.get_vel_components(self.ai_tank.tankSpeed, hf.get_angle_to_hit(self.aiDest[0], self.aiDest[1], self.screen_width - 100, self.screen_height - 100))

    def reset_travel_time(self):
        self.travelTime = time.time()