from AI.base import *
from pygame.math import Vector2 as Vec

import random

class TeamAI( BaseAI ):
    def __init__( self , helper ):
        self.helper = helper
        self.skill = []

    def decide( self ):
        print ('enter')
        helper = self.helper
        hPos = helper.getMyHeadPos()
        hDir = helper.getMyDir()
        wb_radius = helper.getWhiteballRadius()
        if not helper.checkMeInGrav():
            body_list = helper.bodyOnRoute()
            if body_list:
                dPos = helper.getMyShotPos()
                for bPos in body_list:
                    if (bPos - hPos).magnitude() + 3 * wb_radius < (dPos - hPos).magnitude():
                        return AI_MoveWayChange

            head_list = helper.bodyOnRoute()
            if head_list:
                dPos = helper.getMyShotPos()
                for Pos in head_list:
                    if (Pos - hPos).magnitude() + 3 * wb_radius < (dPos - hPos).magnitude():
                        return AI_MoveWayChange
        else :
            gPos, gRadius = helper.getMyGrav()
            if not helper.checkMeCircling():
                if hDir.dot(gPos - hPos) < 0:
                    ball_list = helper.canGetBySpin()
                    if ball_list:
                        return AI_MoveWayChange
            else :
                ball_list = helper.canGetBySpin()
                if not ball_list:
                        return AI_MoveWayChange

        return AI_NothingToDo
