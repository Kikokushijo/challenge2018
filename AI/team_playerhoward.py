from AI.base import *
from pygame.math import Vector2 as Vec

import random

class TeamAI( BaseAI ):
    def __init__( self , helper ):
        self.helper = helper
        self.skill = []
    def ingrav(self, pos):
        gravs = self.helper.getAllGravs()
        for g in gravs:
            if (pos - Vec(g[0])).length_squared() < g[1] ** 2:
                return True
        return False
    def mirror(self, pos):
        if pos.x < 0:
            pos.x = - pos.x
        if pos.y < 0:
            pos.y = - pos.y
        if pos.x > 800:
            pos.x = 800 - (pos.x - 800)
        if pos.y > 800:
            pos.y = 800 - (pos.y - 800)
    def stay_alive(self):
        helper = self.helper
        hPos = Vec(helper.getMyHeadPos())
        head_radius = helper.head_radius
        head_dir = Vec(helper.getMyDir())
        body_radius = helper.body_radius
        normal_speed = helper.normal_speed
        bullet_list = helper.getAllPlayerBullet()
        body_list = helper.getAllBodyPos()
        circling = helper.checkMeCircling()
        dash_time = helper.dash_time
        dash_speed = helper.dash_speed
        if not helper.checkMeInGrav():
            nxtpos = hPos + Vec(head_dir * normal_speed)
            nxt_bullet_list = [((b[1][0]+b[2][0]*b[4],b[1][1]+b[2][1]*b[4]), b[3]) for b in bullet_list]
            for b in nxt_bullet_list:
                #print((Vec(b[0]) - nxtpos).length())
                if (Vec(b[0]) - nxtpos).length() <= (head_radius + b[1] + 1) * 2:
                    return AI_MoveWayChange
            for b in body_list:
                if (Vec(b) - nxtpos).length() <= (body_radius + head_radius + 1) * 2 and \
                    head_dir.dot(Vec(b) - nxtpos) > 0:
                    return AI_MoveWayChange

            if not self.ingrav(hPos):
                nxt_bullet_list = [((b[1][0]+b[2][0]*b[4]*dash_time,b[1][1]+b[2][1]*b[4]*dash_time), b[3]) for b in bullet_list]
                nxtpos = hPos + Vec(head_dir * dash_speed * dash_time)
                self.mirror(nxtpos)
                for b in nxt_bullet_list:
                    #print((Vec(b[0]) - nxtpos).length())
                    bv = Vec(b[0])
                    self.mirror(bv)
                    if (bv - nxtpos).length() <= (head_radius + b[1] + 1) * 2:
                        return AI_NothingToDo
                for b in body_list:
                    if (Vec(b) - nxtpos).length() <= (body_radius + head_radius + 1) * 2 and \
                        head_dir.dot(Vec(b) - nxtpos) > 0:
                        return AI_NothingToDo
                #if self.ingrav(nxtpos):
                #    return AI_NothingToDo
            #if self.ingrav(nxtpos):
            #    return AI_MoveWayChange
            return None
        else:
            gcenter, gr = helper.getMyGrav()
            gcenter = Vec(gcenter)
            dotval = head_dir.dot(gcenter - hPos)
            if not circling and dotval > 0.1:
                return AI_MoveWayChange
            elif circling:
                return AI_MoveWayChange
            return None

    def decide( self ):
        helper = self.helper
        if helper.getMyDashRemainTime() > 0:
            return AI_NothingToDo
        reply = self.stay_alive()
        if reply == None:
            reply = self.attack()
            return AI_NothingToDo
        else:
            return reply