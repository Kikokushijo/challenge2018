# from Model.GameObject.utils import Vec
from pygame.math import Vector2 as Vec
import Model.const as modelConst
import View.const as viewConst
from Model.GameObject.body import Body 
import random

class White_Ball(object):
    def __init__(self, pos = Vec(-1,-1), following = False, target = -1, index = -1):
        self.following = following
        self.target = target
        self.index = index
        self.color = viewConst.wbColor
        self.radius = modelConst.wb_radius
        self.speed = modelConst.wb_speed
        self.age = 0
        if pos == Vec(-2, -2) :
        	randpos = Vec(random.randint(0+modelConst.wb_radius, viewConst.ScreenSize[0]-480-modelConst.wb_radius), random.randint(0+modelConst.wb_radius, viewConst.ScreenSize[1]-modelConst.wb_radius))
        	screen_mid = Vec( viewConst.ScreenSize[1]/2, viewConst.ScreenSize[1]/2 )
        	while (randpos - screen_mid).length_squared() < modelConst.init_no_wb_r ** 2:
        		randpos = Vec(random.randint(0+modelConst.wb_radius, viewConst.ScreenSize[0]-480-modelConst.wb_radius), random.randint(0+modelConst.wb_radius, viewConst.ScreenSize[1]-modelConst.wb_radius))
        	self.pos = randpos
        elif pos == Vec(-1, -1) :
            #random init the position of balls
            self.pos = Vec(random.randint(0+modelConst.wb_radius, viewConst.ScreenSize[0]-480-modelConst.wb_radius), random.randint(0+modelConst.wb_radius, viewConst.ScreenSize[1]-modelConst.wb_radius))
        else:
            #use the pos passed in
            self.pos = Vec(pos)

    def update(self, player_list):
        self.age += 1
        if not self.following:
            return True
        else:
            targetobj = player_list[self.target].body_list[-1]
            targetpos = targetobj.pos_log[0]
            if (self.pos - targetpos).length_squared() < self.speed ** 2:
                player_list[targetobj.index].body_list.append(Body(player_list[targetobj.index].body_list[-1]))
                return False
            else:
                direction = (targetpos - self.pos).normalize()
                self.pos += direction * self.speed
                return True



