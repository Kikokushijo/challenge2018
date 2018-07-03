import Model.const as modelconst
import View.const as viewconst
import random
from math import pi, sin, cos, atan2
from pygame.math import Vector2 as Vec
# from pygame.math import Vec2d as Vec
from Model.GameObject.white_ball import White_Ball
from Model.GameObject.body import Body 
from Model.GameObject.bullet import Bullet

class Head(object):
    def __init__(self, index, name = "player", is_AI = False):
        # basic data
        self.name = name
        self.index = index
        self.is_AI = is_AI
        self.color = viewconst.playerColor[index]
        screen_mid = Vec( viewconst.ScreenSize[1]/2, viewconst.ScreenSize[1]/2 )

        #up down left right
        self.pos = screen_mid + modelconst.init_r * modelconst.Vec_dir[self.index]        
        self.theta = index * (pi/2)
        self.direction = Vec( cos(self.theta), -sin(self.theta) )
        
        self.speed = modelconst.normal_speed
        self.is_dash = False
        self.dash_timer = 0
        self.radius = modelconst.head_radius
        self.is_alive = True
        self.body_list = [self]
        self.is_ingrav = False
        self.is_circling = False
        self.circling_radius = 0
        self.ori = 0
        #if in grav
        self.grav_center = Vec( 0, 0 )
        self.pos_log = [Vec(self.pos)]

    def update(self,player_list, wb_list, bullet_list):
        if not self.is_alive:
            return

        self.pos += self.direction * self.speed
        #update pos log
        self.pos_log.append(Vec(self.pos))
        if len(self.pos_log) > modelconst.pos_log_max :
            self.pos_log.pop(0)
        
        if self.is_circling:
            self.theta += self.speed / self.circling_radius * self.ori
            #print(self.theta, self.speed/self.circling_radius)
            self.direction = Vec( cos(self.theta), -sin(self.theta) )
        
        #is in circle
        self.is_ingrav=False
        for i in modelconst.grav :
            if ( self.pos - i[0] ).length_squared() < i[1]**2 :
                self.is_ingrav = True
                self.grav_center = i[0]

        #collision with wall
        if (self.direction.x > 0 and self.pos.x + self.radius > viewconst.ScreenSize[1]-modelconst.eps) \
            or (self.direction.x < 0 and self.pos.x - self.radius < 0 - modelconst.eps) :
            self.direction.x *= -1
        if (self.direction.y > 0 and self.pos.y + self.radius > viewconst.ScreenSize[1]-modelconst.eps) \
            or (self.direction.y < 0 and self.pos.y - self.radius < 0 - modelconst.eps) :
            self.direction.y *= -1
        
        #collision with white ball
        for i, wb in enumerate(wb_list):
            if (self.pos - wb.pos).length_squared() < (self.radius + wb.radius)**2 :
                #delete a withe ball
                del wb_list[i]
                #lengthen body list
                self.body_list.append(Body(self.body_list[-1]))
        
        
        #collision with competitor's body and bullet

        if not self.is_dash:
            for enemy in player_list:
                if enemy.index == self.index :
                    continue
                for j in enemy.body_list[1:]:
                    if (self.pos - j.pos).length_squared() < (self.radius + j.radius)**2 :
                        #self die
                        killer = enemy.index
                        self.is_alive = False
                        break
            for bullet in bullet_list :
                if (bullet.index != self.index) and \
                   (self.pos - bullet.pos).length_squared() < (self.radius + bullet.radius)**2 :
                    killer = bullet.index
                    self.is_alive = False
                    break
        if not self.is_alive:
            self.is_dash = True
            while len(self.body_list) > 1:
                player_list[killer].body_list.append(Body(player_list[killer].body_list[-1]))
                self.body_list.pop(-1)

            return
        #collision with competitor's head
        if not self.is_dash:
            for enemy in player_list:
                if enemy.index == self.index or enemy.is_dash == True:
                    continue
                if (self.pos - enemy.pos).length_squared() < (self.radius + enemy.radius)**2 :
                    rrel = enemy.pos - self.pos
                    self.direction.reflect_ip(rrel)
                    enemy.direction.reflect_ip(rrel)
                    self.is_circling = False
        
        #collision with item


        #dash timer
        if self.is_dash:
            self.dash_timer -= 1
            if self.dash_timer == 0:
                self.is_dash = False
                #self.speed = modelconst.normal_speed
        #update theta
        #self.theta = atan2(self.direction.x, -self.direction.y)
        for j in range(1, len(self.body_list)):
                self.body_list[j].update()
    
    def click(self, bullet_list) :
        if not self.is_dash:
            if self.is_ingrav:
                self.is_circling = (not self.is_circling)
                if self.is_circling:
                    self.circling_radius = (self.pos - self.grav_center).length()
                    ori = self.direction.cross(self.pos - self.grav_center)
                    if ori > 0: #counterclockwise
                        self.theta = atan2( self.pos.y - self.grav_center.y , -self.pos.x + self.grav_center.x ) - pi / 2
                        self.direction = Vec( cos(self.theta) , - sin(self.theta) )
                        self.ori = 1
                    else:
                        self.theta = atan2( self.pos.y - self.grav_center.y , -self.pos.x + self.grav_center.x ) + pi / 2
                        self.direction = Vec( cos(self.theta) , - sin(self.theta) )
                        self.ori = -1
                else:
                    self.circling_radius = 0

            else:
                self.is_dash = True
                self.dash_timer = modelconst.max_dash_time * modelconst.dash_speed_multiplier
                #self.speed = modelconst.dash_speed
                if len(self.body_list)>1 :
                    self.body_list.pop(-1)
                    bullet_list.append(Bullet(self.pos,self.direction,self.index))











