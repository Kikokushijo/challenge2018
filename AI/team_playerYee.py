from AI.base import *
from pygame.math import Vector2 as Vec
from Model.GameObject.head import Head
from math import sin,cos

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
            if isinstance(obj[0], Head):
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
                #print(self.theta, self.speed/self.circling_radius)
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
        
def too_close(pos1, r1, pos2, r2, distance = 0.0):
    return (pos1 - pos2).length_squared() <= (r1 + distance + r2)** 2

class TeamAI( BaseAI ):
    def __init__( self , helper ):
        self.helper = helper
        self.skill = []
        self.gravs = self.helper.getAllGravs()
        self.me = None
        self.reset_esc = False
        self.escaping = False
        self.danger=[] #0:body 1:bullet 2:enemy's head
    
    def stimulate_collision(self, obj1, obj2, esc_time):
        obj1 = Stimulate_Obj(self.gravs, obj1)
        obj2 = Stimulate_Obj(self.gravs, obj2)
        
        for _ in range(esc_time):
            if not obj2.update():
                return False
            obj1.update()

            is_too_close=too_close(obj1.pos, obj1.radius, obj2.pos, obj2.radius)
            if is_too_close:
                return True
            if obj1.is_circling and not is_too_close:
                return False
        return False
        
    def decide(self):
        helper = self.helper
        self.me = helper.model.player_list[helper.index]

        if self.me.init_timer > 0 or not helper.checkPlayerAlive(helper.index) or helper.checkInvisible():
            return AI_NothingToDo
        is_ingrav=helper.checkMeInGrav()
        
        if is_ingrav:
            if self.reset_esc:
                self.escaping = False
                self.reset_esc = False
            
            if helper.checkMeCircling():
                if self.escaping:
                    if self.danger[-1]==0:
                        #原本是直行, 遇到危險變circling, 在前方仍有太近的body下繼續旋轉, 直到脫離
                        for body in helper.bodyOnRoute():
                            if not too_close(self.me.pos, self.me.radius, Vec(body), helper.body_radius, 5 * helper.head_radius):
                                self.escaping=False
                                break
                        else:
                            self.escaping = True
                    elif self.danger[-1]==1:
                        for bullet in self.model.bullet_list:
                            if bullet.index == self.me.index:
                                continue
                    elif self.danger[-1] == 2:
                        pass
                else:
                    grav_center=Vec(helper.getMyGrav()[0])
                    for body_pos in helper.getAllBodyPos():
                        grav_to_me = self.me.pos - grav_center
                        grav_to_body = Vec(body_pos) - grav_center
                        #has body on the circle and it is close enough
                        if abs(self.me.circling_radius - grav_to_body.length()) <= 2 * helper.head_radius \
                            and self.me.circling_radius*grav_to_me.angle_to(grav_to_body)<=8*helper.head_radius:
                            self.danger.append(0)
                            self.escaping=True
                            return AI_MoveWayChange
                    
                    for bullet in helper.model.bullet_list:
                        if bullet.index == helper.index:
                            continue
                        if self.stimulate_collision(self.me, bullet, 30):
                            self.danger.append(1)
                            self.escaping=True
                            return AI_MoveWayChange

                    
                    


            else: #is going straight
                if self.escaping:
                    if self.danger[-1]==0:
                        #原本是circling, 遇到危險變直行, 在grav_to_me的軌道上仍有body時繼續直行，直到脫離或離開grav
                        grav_center=Vec(helper.getMyGrav()[0])
                        for body_pos in helper.getAllBodyPos():
                            grav_to_me = self.me.pos - grav_center
                            grav_to_body = Vec(body_pos) - grav_center
                            #has body on the circle and it is close enough
                            if not (abs(grav_to_me.length() - grav_to_body.length()) <= 2 * helper.head_radius \
                                and self.me.circling_radius*grav_to_me.angle_to(grav_to_body)<=8*helper.head_radius):
                                self.escaping = False
                                self.danger.pop()
                                break
                    elif self.danger[-1] == 1:
                        pass
                    elif self.danger[-1] == 2:
                        pass
                else:
                    for body in body_on_route:
                        if too_close(self.me.pos, self.me.radius, Vec(body), helper.body_radius, 5 * helper.head_radius):
                            self.escaping=True
                            return AI_MoveWayChange
            
        else:
            for bullet in helper.model.bullet_list:
                if bullet.index == helper.index:
                    continue
                if self.stimulate_collision(self.me, bullet, 30):
                    self.escaping=True
                    return AI_MoveWayChange

            for enemy in helper.model.player_list:
                if enemy.index == self.me.index or not enemy.is_alive:
                    continue
                if not helper.checkPlayerInGrav(enemy.index) and enemy.dash_cool <= 0 and helper.collisionOnRoute(enemy.pos, enemy.radius, enemy.direction, self.me.pos, self.me.radius) \
                    and 
                if helper.collisionOnRoute(enemy.pos, enemy.radius, enemy.direction, self.me.pos, self.me.radius) \
                                            and not helper.checkMeInGrav() and too_close(self.me.pos, self.me.radius, enemy.pos, enemy.radius, 3 * helper.wb_radius):
                    return AI_MoveWayChange
        else:
            self.reset_esc = True
            

        for bullet in helper.model.bullet_list:
            if bullet.index == helper.index:
                continue
            if (is_ingrav and self.stimulate_collision(self.me, bullet, 30)) \
                or (too_close(self.me.pos, self.me.radius, bullet.pos, bullet.radius ,8*helper.wb_radius)) and self.stimulate_collision(self.me, bullet,15)):
                return AI_MoveWayChange

        for enemy in helper.model.player_list:
            if enemy.index == self.me.index or not enemy.is_alive:
                continue
            if is_ingrav:
                if helper.collisionOnRoute(enemy.pos, enemy.radius, enemy.direction, self.me.pos, self.me.radius) \
                    and not helper.checkPlayerInGrav(enemy.index)
            if helper.collisionOnRoute(enemy.pos, enemy.radius, enemy.direction, self.me.pos, self.me.radius) \
                                        and not helper.checkMeInGrav() and too_close(self.me.pos, self.me.radius, enemy.pos, enemy.radius, 3 * helper.wb_radius) and enemy.dash_cool <= 0:
                return AI_MoveWayChange
        
        body_on_route = helper.bodyOnRoute()
        if len(body_on_route) == 0:
            self.body_esc=False
        else:
            for body in body_on_route:
                if not body_esc and too_close(self.me.pos, self.me.radius, Vec(body), helper.body_radius, 5 * helper.wb_radius):
                    self.body_esc=True
                    return AI_MoveWayChange
        
        #attack
        if len(self.me.body_list)>1 and not helper.checkMeInGrav():
            bullet = Stimulate_Obj(self.gravs, self.me.pos, self.me.direction, helper.bullet_speed, helper.bullet_radius, helper.bullet_acc)
            for player in helper.model.player_list:
                if player.index != helper.index and self.stimulate_collision(player, bullet, 10):
                    return AI_MoveWayChange
        
        if helper.canGetBySpin() == 0 and helper.checkMeCircling():
            return AI_MoveWayChange
        
        return AI_NothingToDo
