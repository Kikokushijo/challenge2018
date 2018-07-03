import Model.const as modelconst
import View.const as viewconst
import random
from math import pi, sin, cos, atan2
from pygame.math import Vector2 as Vec
from Model.GameObject.white_ball import White_Ball
from Model.GameObject.body import Body 
from Model.GameObject.bullet import Bullet

class Head(object):
    def __init__(self, name = "player", index):
        # basic data
        self.name = name
        self.index = index 
        screen_mid = Vec( viewconst.ScreenSize[0]/2, viewconst.ScreenSize[1]/2 )

        #up down left right
        self.pos = screen_mid + modelconst.init_r * modelconst.Vec_dir[self.index]        
        self.theta = index * (pi/2)
        self.direction = Vec( cos(self.theta), sin(self.theta) )
        
        self.speed = modelconst.normal_speed
        self.is_dash = False
        self.dash_timer = 0
        self.radius = modelconst.head_radius
        self.is_alive = True
        self.body_list = [self]
        self.is_ingrav = False
        self.is_circling = False
        self.circling_radius = 0
        #if in grav
        self.grav_center = Vec( 0, 0 )
        self.direction_log = [self.direction]

    def update(self,player_list, wb_list, bullet_list):
        
        if len(self.direction_log) > modelconst.direction_log_max :
                self.direction_log.pop(0)

        self.pos += self.direction * self.speed
        
        if self.is_circling:
            self.theta += (self.speed/self.circling_radius)*modelconst.dt
            self.direction = Vec( cos(self.theta), sin(self.theta) )
        
        #is in circle
        for i in modelconst.grav :
            if ( self.pos - i[0] ).magnitude_squared() < i[1]**2 :
                self.is_ingrav = True
                self.grav_center = i[0]

        #collision with wall
        if (self.direction.x > 0 and self.pos.x + self.radius > viewconst.ScreenSize[0]-modelconst.eps) \
            or (self.direction.x < 0 and self.pos.x - self.radius < 0 - modelconst.eps) :
            self.direction.x *= -1
        if (self.direction.y > 0 and self.pos.y + self.radius > viewconst.ScreenSize[1]-modelconst.eps) \
            or (self.direction.y < 0 and self.pos.y - self.radius < 0 - modelconst.eps) :
            self.direction.y *= -1
        
        #collision with white ball
        for i, wb in enumerate(wb_list):
            if (self.pos - wb.pos).magnitude_squared() < (self.radius + wb.radius)**2 :
                #delete a withe ball
                del wb_list[i]
                #lengthen body list
                self.body_list.append(Body(self.body_list[-1]))
        
        
        #collision with competitor's body and bullet

        if not self.is_dash:
            for enemy in player_list:
                if enemy.index == self.index :
                    continue
                for j in self.body_list[1:]:
                    if (self.pos - j.pos).magnitude_squared() < (self.radius + j.radius)**2 :
                        #self die
                        self.is_alive = False
                        break
            for bullet in bullet_list :
                if (self.pos - bullet.pos).magnitude_squared() < (self.radius + bullet.radius)**2 :
                    self.is_alive = False
                    break

        #collision with competitor's head
        if not self.is_dash:
            for enemy in player_list:
                if enemy.index == self.index or enemy.is_dash == True:
                    continue
                if (self.pos - enemy.pos).magnitude_squared() < (self.radius + enemy.radius)**2 :
                    rrel = enemy.pos - self.pos
                    self.direction.reflect_ip(rrel)
                    enemy.direction.reflect_ip(rrel)
        
        #collision with item


        #dash timer
        if self.is_dash:
            self.dash_timer -= 1
            if self.dash_timer == 0:
                self.is_dash = False
                self.speed = modelconst.normal_speed
        #update direction log
        self.direction_log.append( self.direction )
        #update theta
        self.theta = atan2(self.direction.x, self.direction.y)
    
    def click(self, bullet_list) :
        if not self.is_dash:
            if self.is_ingrav:
                self.is_circling = (not self.is_circling)
                if self.is_circling:
                    circling_radius = (self.pos - self.grav_center).magnitude
                else:
                    circling_radius = 0

            else:
                self.is_dash = True
                self.dash_timer = modelconst.max_dash_time
                self.speed = modelconst.dash_speed
                if len(self.body_list)>1 :
                    self.body_list.pop()
                    bullet_list.append(Bullet(self.pos,self.direction,self.index))











