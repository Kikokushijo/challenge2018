from AI.base import *
from pygame.math import Vector2 as Vec

import random
eps=1e-5
class TeamAI( BaseAI ):
    def __init__( self , helper ):
        self.helper = helper
        self.skill = []
        self.wb_radius = self.helper.getWhiteballRadius()
        self.me = self.helper.model.player_list[self.helper.index]
    
    def is_going_collide(self, bullet):
        x1, y1 = self.me.pos
        v1x, v1y = self.me.direction * self.me.speed
        s1=self.me.speed
        x2, y2 = bullet.pos
        v2x, v2y = bullet.direction * bullet.speed
        s2=bullet.speed
        
        delta = -v1x * v2y + v2x * v1y
        if abs(delta) <= eps:
            return False
        collision_t1 = ((x2 - x1) * (-v2y) + v2x * (y2 - y1)) / delta
        collision_t2 = (v1x * (y2 - y1) - (x2 - x1) * v2x) / delta
        if collision_t1 <= -eps or collision_t2 <= -eps:
            return False
        
        intersect_point = self.me.pos + self.me.direction * self.me.speed * collision_t1
        a = self.me.pos.distance_to(Vec(intersect_point))#me_dist_to_point
        b = bullet.pos.distance_to(Vec(intersect_point))  #bullet_dist_to_point
        v1_dot_v2=self.me.direction.dot(bullet.direction)
        D = 4 * ((a * s1 + b * s2)** 2 - (a ** 2 - 2 * a * b * v1_dot_v2 + b ** 2 - (self.me.radius + bullet.radius)** 2) * (s1 ** 2 - 2 * s1 * s2 * v1_dot_v2 + s2 ** 2))
        if D < 0:
            return False

        
    def decide( self ):
        for bullet in self.helper.getAllPlayerBullet():
            if self.helper.checkMeInGrav():
                pass
            else:
                delta=
        if helper.getOtherBulletNumInRange(hPos, 10 * wb_radius) > 0:
            return AI_MoveWayChange
        if not helper.checkMeInGrav():
            if helper.bodyOnRoute():
                return AI_MoveWayChange
            if helper.bodyOnRoute():
                return AI_MoveWayChange
        else :
            if helper.checkMeCircling() and helper.canGetBySpin() == 0:
                return AI_MoveWayChange
            if not helper.checkMeCircling() and helper.canGetBySpin() > 0:
                return AI_MoveWayChange
        return AI_NothingToDo
