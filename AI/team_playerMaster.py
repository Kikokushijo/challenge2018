from AI.base import *
from pygame.math import Vector2 as Vec
from math import sin, cos
from datetime import datetime

import random
eps = 1e-5
game_size = 800
class Stimulate_Obj(object):
    def __init__(self, gravs, *obj):
        self.is_head = False
        self.gravs = gravs
        
        if len(obj) == 1:
            self.pos = Vec(obj[0].pos)
            self.direction=Vec(obj[0].direction)
            self.speed=obj[0].speed
            self.radius=obj[0].radius
            if hasattr(obj[0],'is_circling'):
                self.is_circling = obj[0].is_circling
                self.circling_radius = obj[0].circling_radius
                self.ori = obj[0].ori
                self.init_timer = obj[0].init_timer
                self.theta = obj[0].theta
                self.is_ingrav = obj[0].is_ingrav
                self.grav_center = Vec(obj[0].grav_center)
                self.is_head = True
                self.acc = 0
            else:
                self.acc=obj[0].acc
        else:
            self.pos=Vec(obj[0])
            self.direction=Vec(obj[1])
            self.speed=obj[2]
            self.radius=obj[3]
            if len(obj) >= 5 and obj[4] is not None:
                self.acc = obj[4]
            else:
                self.acc = 0.0

    def update(self):
        if self.is_head:
            if self.is_circling:
                self.theta += self.speed / self.circling_radius * self.ori
                self.direction = Vec( cos(self.theta), -sin(self.theta) )
            if self.init_timer != -1:
                self.init_timer -= 1
            if self.init_timer > 0:
                return 0
            elif self.init_timer == 0:
                self.is_circling = False
                self.init_timer = -1
            #is in circle
            self.is_ingrav=False
            for i in self.gravs :
                if ( self.pos - i[0] ).length_squared() < i[1]**2 :
                    self.is_ingrav = True
                    self.grav_center = i[0]

        self.pos += self.direction * self.speed

        #collision with wall
        if (self.direction.x > 0 and self.pos.x+self.radius >= game_size - eps) \
            or (self.direction.x < 0 and self.pos.x-self.radius <= -eps):
            self.direction.x *= -1
        if (self.direction.y > 0 and self.pos.y+self.radius >= game_size - eps) \
            or (self.direction.y < 0 and self.pos.y-self.radius <= -eps):
            self.direction.y *= -1
        
        self.speed -= self.acc
        return self.speed > 0

class TeamAI( BaseAI ):
    def __init__( self , helper ):
        self.helper = helper
        self.skill = []
        self.me = None
        self.gravs=self.helper.getAllGravs()
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
            if pos is None:
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
        return None
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
                if pos is None:
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
                if pos is None:
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
                if pos is None:
                    continue
                if (helper.checkPlayerInGrav(i) or helper.getPlayerDashCoolRemainTime(i)>0)\
                    and (pos - hPos).length_squared() < 20 ** 2:
                        #print("attack")
                        return AI_MoveWayChange
            return None

    def debug(self,message):
        print('Master%d: %s %dmin %ds' %(self.helper.index,message,datetime.now().minute,datetime.now().second))

    @staticmethod
    def too_close(pos1, r1, pos2, r2, distance = 0.0):
        return (pos1 - pos2).length_squared() <= (r1 + distance + r2)** 2

    def stimulate_collision(self, obj1, obj2, stimulate_time):
        obj1 = Stimulate_Obj(self.gravs, obj1)
        obj2 = Stimulate_Obj(self.gravs, obj2)
        
        for _ in range(stimulate_time):
            if not obj2.update():
                return False
            obj1.update()

            if self.too_close(obj1.pos, obj1.radius, obj2.pos, obj2.radius):
                return True
        return False

    def attack2(self):
        helper=self.helper
        self.me=helper.model.player_list[helper.index]
        if len(self.me.body_list) <= 1:
            return None
        bullet = Stimulate_Obj(self.gravs, self.me.pos, self.me.direction, helper.bullet_speed, helper.bullet_radius, helper.bullet_acc)
        for player in helper.model.player_list:
            if player.index == helper.index or not helper.checkPlayerAlive(player.index):
                continue
            if player.is_AI:
                if helper.checkPlayerInGrav(player.index):
                    if helper.getPlayerDashCoolRemainTime(player.index) > 0:
                        if helper.checkPlayerInvisible(player.index): #dashing
                            #找到dash結束時head的pos，找到此時bullet的pos
                            st_player=Stimulate_Obj(self.gravs,player)
                            self.mirror(st_player.pos + st_player.direction * helper.dash_speed * helper.getPlayerDashRemainTime(player.index))
                            self.mirror(bullet.pos + bullet.direction * (helper.bullet_speed * helper.getPlayerDashRemainTime(player.index) \
                                            -0.5*helper.bullet_acc*helper.getPlayerDashRemainTime(player.index)**2))
                            #stimulate
                            if self.stimulate_collision(st_player, bullet, helper.dash_cool):
                                self.debug('attack when dashing')
                                return AI_MoveWayChange
                        else: #cooling
                            if self.stimulate_collision(player, bullet, helper.getPlayerDashCoolRemainTime(player.index)):
                                self.debug('attack when cooling')
                                return AI_MoveWayChange
                    else: #not dashing and not cooling
                        if self.stimulate_collision(player, bullet, 20):
                            self.debug('normal attack in grav')
                            return AI_MoveWayChange
                else:  #not in grav
                    if self.stimulate_collision(player, bullet, 15):
                        return AI_MoveWayChange					
            else:
                if helper.checkPlayerInGrav(player.index):
                    if self.stimulate_collision(player, bullet, 20):
                        self.debug('attack in grav')
                        return AI_MoveWayChange
                else:
                    if self.stimulate_collision(player, bullet, 15):
                        return AI_MoveWayChange
        return None

        
    def decide( self ):
        helper = self.helper
        if helper.getMyDashRemainTime() > 0:
            return AI_NothingToDo
        reply = self.stay_alive()
        if reply is None:
            reply = self.attack()
            if reply is None:
                reply = self.attack2()
                if reply is not None:
                    return AI_MoveWayChange
                return AI_NothingToDo
            else:
                print("can move to attack")
                return reply
        else:
            return reply