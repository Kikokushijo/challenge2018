from AI.base import *
from pygame.math import Vector2 as Vec

import random

class TeamAI( BaseAI ):
    def __init__( self , helper ):
        self.helper = helper
        self.skill = [99, 99, 99, 99, 99, 99, 99]
        self.counter = 0

    def decide( self ):
        if self.counter % 300 == 0:
            self.counter += 1
            return random.randint(2, 8)
        else:
            self.counter += 1
            return AI_NothingToDo