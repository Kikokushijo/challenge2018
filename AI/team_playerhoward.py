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
        for i in range(4):
            if i == helper.index:
                continue
            pos = helper.getPlayerHeadPos(i)
            if pos == None:
                continue
            dir = helper.getPlayerDir(i)
            bullet_list.append((i, pos, dir, helper.bullet_radius, helper.bullet_speed))
        body_list = helper.getAllBodyPos()
        circling = helper.checkMeCircling()
        dash_time = helper.dash_time
        dash_speed = helper.dash_speed
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
        if helper.checkMeInGrav():
            gcenter, gr = helper.getMyGrav()
            gcenter = Vec(gcenter)
            dotval = head_dir.dot(gcenter - hPos)
            if not circling and dotval > 0.1:
                return AI_MoveWayChange
            elif not circling:
                return AI_NothingToDo
            elif circling and (hPos - gcenter).length_squared() > (0.95 * gr) ** 2:
                return AI_MoveWayChange
            elif circling:
                return AI_MoveWayChange
    def attack(self):
        helper = self.helper
        hPos = Vec(helper.getMyHeadPos())
        head_radius = helper.head_radius
        head_dir = Vec(helper.getMyDir())
        circling = helper.checkMeCircling()
        if len(helper.getMyBodyPos()) == 0:
            return None
        if circling:
            for i in range(4):
                if i == helper.index:
                    continue
                pos = helper.getPlayerHeadPos(i)
                if pos == None:
                    continue
                pdir = Vec(helper.getPlayerDir(i))
                t1 = head_dir.dot(pdir) / pdir.length() / head_dir.length()
                rrel = pos - hPos
                t2 = head_dir.dot(rrel) / rrel.length() / head_dir.length()
                if 0.98 < t2 and helper.checkPlayerInGrav(i) and rrel.length() < 150:
                    return AI_MoveWayChange
        elif not helper.checkMeInGrav():
            for i in range(4):
                if i == helper.index:
                    continue
                pos = helper.getPlayerHeadPos(i)
                if pos == None:
                    continue
                pdir = Vec(helper.getPlayerDir(i))
                t1 = head_dir.dot(pdir) / pdir.length() / head_dir.length()
                rrel = pos - hPos
                t2 = head_dir.dot(rrel) / rrel.length() / head_dir.length()
                if 0.98 < t2 and helper.checkPlayerInGrav(i) and rrel.length() < 400:
                    return AI_MoveWayChange
            for i in range(4):
                if i == helper.index:
                    continue
                pos = helper.getPlayerHeadPos(i)
                if pos == None:
                    continue
                if (helper.checkPlayerInGrav(i) or helper.getPlayerDashCoolRemainTime(i)>0)\
                    and (pos - hPos).length_squared() < 20 ** 2:
                        #print("attack")
                        return AI_MoveWayChange
            return None
    def decide( self ):
        helper = self.helper
        if helper.getMyDashRemainTime() > 0:
            return AI_NothingToDo
        reply = self.stay_alive()
        if reply == None:
            reply = self.attack()
            if reply == None:
                return AI_NothingToDo
            else:
                print("can move to attack")
                return reply
        else:
            return reply