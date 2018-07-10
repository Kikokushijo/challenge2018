from AI.base import *
from pygame.math import Vector2 as Vec

import random

class TeamAI( BaseAI ):
    def __init__( self , helper ):
        self.helper = helper
        self.skill = []
    def stay_alive(self):
        helper = self.helper
        hPos = helper.getMyHeadPos()
        head_radius = helper.getHeadRadius()
        body_radius = helper.getBodyRadius()
        bullet_list = helper.getAllBullet()
        body_list = helper.getAllBodyPos()
        nxtpos = Vec(helper.getNextPos())
        nxt_bullet_list = [((b[1][0]+b[3][0],b[1][1]+b[3][1]), b[2]) for b in bullet_list]
        for b in nxt_bullet_list:
            #print((Vec(b[0]) - nxtpos).length())
            if (Vec(b[0]) - nxtpos).length() <= (head_radius + b[1] + 1) * 2:
                return AI_MoveWayChange
        for b in body_list:
            if (Vec(b) - nxtpos).length() <= (body_radius + head_radius + 1) * 2:
                return AI_MoveWayChange
        return AI_NothingToDo

    def decide( self ):
        helper = self.helper
        hPos = helper.getMyHeadPos()
        head_radius = helper.getHeadRadius()
        body_radius = helper.getBodyRadius()
        return self.stay_alive()