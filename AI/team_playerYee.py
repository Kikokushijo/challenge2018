from math import sin, cos,pi
from AI.base import *
from pygame.math import Vector2 as Vec
from datetime import datetime

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
        self.gravs = self.helper.getAllGravs()
        self.me = None
        self.reset_esc = False
        self.escaping = False
        self.danger=[] #0:body 1:bullet 2:enemy's head
    
    def debug(self,message):
        print('Yee%d: %s %dmin %ds' %(self.helper.index,message,datetime.now().minute,datetime.now().second))

   
    @staticmethod
    def too_close(pos1, r1, pos2, r2, distance = 0.0):
        return (pos1 - pos2).length_squared() <= (r1 + distance + r2)** 2

    def too_close_sec(self, grav_to_me, grav_to_body, second):
        return grav_to_me.length() * abs(grav_to_me.angle_to(grav_to_body)) * pi <= second * self.helper.normal_speed * 180
    
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
    
    def get_all_body(self):
        helper = self.helper
        for player in helper.model.player_list:
            if player.index == helper.index or not player.is_alive:
                continue
            for body in player.body_list[1:]:
                yield body
                    
    def circling_collide(self, second):
        helper=self.helper
        for body in self.get_all_body():
            grav_to_me = self.me.pos - self.me.grav_center
            grav_to_body = body.pos - self.me.grav_center
            #does not have body on the circle and it is close enough
            if abs(self.me.circling_radius - grav_to_body.length()) <= 2 * helper.head_radius \
                and self.too_close_sec(grav_to_me, grav_to_body, second):
                return True
        return False

    def body_escaping(self):
        helper=self.helper
        if helper.checkMeCircling(): #going straight in the past
            for body in helper.bodyOnRoute():
                if self.too_close(self.me.pos, self.me.radius, Vec(body), helper.body_radius, 4 * helper.head_radius):
                    return False
            return True
        else: #circling in the past
            return not self.circling_collide(45)
    
    def body_threat(self):
        helper=self.helper
        if helper.checkMeCircling():
            return self.circling_collide(45)
        else:
            for body in helper.bodyOnRoute():
                if self.too_close(self.me.pos, self.me.radius, Vec(body), helper.body_radius, 10 * helper.head_radius):
                    if not self.circling_collide(45):
                        return True
            return False
            
    def bullet_escaping(self):
        return not self.bullet_threat()

    def bullet_threat(self, esc_time=45):
        helper=self.helper
        for bullet in helper.model.bullet_list:
            if bullet.index == helper.index:
                continue
            if self.too_close(self.me.pos, self.me.radius, bullet.pos, bullet.radius, 20 * helper.head_radius) \
                 and self.stimulate_collision(self.me, bullet, esc_time):
                return True
        return False
    
    def head_point_escaping(self):
        return not self.head_point_threat()

    @staticmethod
    def get_intersect_distance(pos1, dir1, pos2, dir2):
        ''' -> t:float intersection point = pos1 + t*dir1 '''
        cross = dir1.cross(dir2)
        if abs(cross) <= eps:
            return None
        dist = (pos2 - pos1).cross(dir2) / cross
        intersect_point = pos1 + dir1 * dist
        if not (-eps <= intersect_point.x <= game_size + eps and -eps <= intersect_point.y <= game_size + eps):
            return None
        return dist

    @staticmethod
    def point_dist_to_line(point, line_point, line_vec):
        return abs(line_vec.y*(point.x-line_point.x) -line_vec.x*(point.y-line_point.y))

    def head_point_threat(self, stimulate_time=20):
        helper = self.helper
        for enemy in helper.model.player_list:
            if enemy.index == helper.index or not helper.checkPlayerAlive(enemy.index):
                continue
            if not helper.checkPlayerInGrav(enemy.index) and enemy.dash_cool <= 0:
                bullet = Stimulate_Obj(self.gravs, enemy.pos, enemy.direction, helper.bullet_speed, helper.bullet_radius, helper.bullet_acc)
                if self.stimulate_collision(self.me, bullet, stimulate_time):
                    return True
                if self.me.is_ingrav:
                    #distance from enemy to intersection = t (the length of enemy.direction is 1)
                    #distance that enemy dashed = helper.dash_speed * helper.max_dash_time (the length of enemy.direction is 1)
                    dist_to_intersect=self.get_intersect_distance(self.me.pos,self.me.direction,enemy.pos,enemy.direction)
                    dist_dashed = helper.dash_speed * helper.max_dash_time
                    if dist_to_intersect is not None and dist_to_intersect-dist_dashed <= helper.head_radius+eps \
                        and abs(self.point_dist_to_line(self.me.grav_center, enemy.pos, enemy.direction) - (self.me.pos - self.me.grav_center).length()) > 2 * helper.head_radius+eps:
                        return True
        return False
    
    def decide(self):
        helper = self.helper
        self.me = helper.model.player_list[helper.index]

        if self.me.init_timer > 0 or not helper.checkPlayerAlive(helper.index) or helper.checkInvisible() \
            or (not helper.checkMeInGrav() and helper.getMyDashCoolRemainTime()>0):
            return AI_NothingToDo
        
        if helper.checkMeInGrav():
            if self.danger:
                if self.danger[-1] == 0:
                    if self.body_escaping():
                        self.escaping = False
                        self.danger.pop()
                    if self.head_point_threat():
                        self.escaping = True
                        self.danger.append(2)
                    if self.bullet_threat():
                        self.escaping = True
                        self.danger.append(1)
                        
                    if self.escaping and self.danger[-1] != 0:
                        self.debug('%s threat' % 'head'if self.danger[-1]==2 else 'bullet')
                        return AI_MoveWayChange
                elif self.danger[-1] == 1:
                    if self.bullet_escaping():
                        self.escaping = False
                        self.danger.pop()
                    if self.head_point_threat():
                        self.escaping = True
                        self.danger.append(2)                        
                    if self.body_threat():
                        self.escaping = True
                        self.danger.append(0)

                    if self.escaping and self.danger[-1] != 1:
                        self.debug('%s threat' % 'body'if self.danger[-1]==0 else 'head')
                        return AI_MoveWayChange
                elif self.danger[-1] == 2:
                    if self.head_point_escaping():
                        self.escaping = False
                        self.danger.pop()
                    if self.body_threat():
                        self.escaping = True
                        self.danger.append(0)
                    if self.bullet_threat():
                        self.escaping = True
                        self.danger.append(1)                        

                    if self.escaping and self.danger[-1] != 2:
                        self.debug('%s threat' % 'body'if self.danger[-1]==0 else 'bullet')
                        return AI_MoveWayChange

            else:
                if self.head_point_threat():
                    self.escaping = True
                    self.danger.append(2)                    
                if self.body_threat():
                    self.escaping = True
                    self.danger.append(0)
                if self.bullet_threat():
                    self.escaping = True
                    self.danger.append(1)
            
                if self.escaping:
                    self.debug('first encounter threat')
                    return AI_MoveWayChange

                getbyspin=helper.canGetBySpin()
                if getbyspin == 0 and helper.checkMeCircling():
                    self.debug('esc circling')
                    return AI_MoveWayChange
                elif getbyspin > 0 and not helper.checkMeCircling():
                    self.debug('spin to eat')
                    return AI_MoveWayChange

        else: #not in grav
            if self.bullet_threat(12):
                self.debug('normal dudge bullet')
                return AI_MoveWayChange

            if self.head_point_threat(10):
                self.debug('normal dudge head')
                return AI_MoveWayChange

            nearest_grav_on_route=helper.getNearestGravOnRoute()
            dist=helper.max_dash_time * helper.dash_speed if nearest_grav_on_route is not None and (self.me.pos - Vec(nearest_grav_on_route[0])).length_squared()<=helper.head_radius**2 else 5 * helper.head_radius
            for body in helper.bodyOnRoute():
                if self.too_close(self.me.pos, self.me.radius, Vec(body), helper.body_radius, dist):
                    self.debug('normal dudge body')
                    return AI_MoveWayChange
        
            #attack
            if len(self.me.body_list)>1:
                bullet = Stimulate_Obj(self.gravs, self.me.pos, self.me.direction, helper.bullet_speed, helper.bullet_radius, helper.bullet_acc)
                for player in helper.model.player_list:
                    if player.index == helper.index or not helper.checkPlayerAlive(player.index):
                        continue
                    if player.is_AI and not helper.checkPlayerInGrav(player.index):
                        if helper.getPlayerDashCoolRemainTime(player.index)>0 and self.stimulate_collision(player, bullet, helper.getPlayerDashCoolRemainTime(player.index)):
                            self.debug('attack when cooling')
                            return AI_MoveWayChange
                    else:
                        if helper.checkPlayerInGrav(player.index):
                            if self.stimulate_collision(player, bullet, 20):
                                self.debug('attack in grav')
                                return AI_MoveWayChange
                        else:
                            if self.stimulate_collision(player, bullet, 15):
                                return AI_MoveWayChange
        
        return AI_NothingToDo