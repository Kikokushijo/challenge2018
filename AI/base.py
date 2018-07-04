"""
const of AI code use.
"""
#action

AI_NothingToDo = 0
AI_MoveWayChange = 1

"""
a base of AI.
"""
class BaseAI:
    def __init__( self , helper ):
        self.skill = []
        self.helper = helper

    def decide( self ):
        pass