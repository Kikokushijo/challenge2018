"""
const of AI code use.
"""
#action

AI_NothingToDo    = 0
AI_MoveWayChange  = 1
AI_Explosion      = 2
AI_MultiBullet    = 3
AI_Canon          = 4
AI_Sacrifice      = 5
AI_NuclearCrisis  = 6
AI_Rainbow        = 7
AI_Resonance      = 8

"""
a base of AI.
"""
class BaseAI:
    def __init__( self , helper ):
        self.skill = []
        self.helper = helper

    def decide( self ):
        pass