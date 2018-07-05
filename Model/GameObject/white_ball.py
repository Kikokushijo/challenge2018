# from Model.GameObject.utils import Vec
from pygame.math import Vector2 as Vec
import Model.const as modelConst
import View.const as viewConst
import random

class White_Ball(object):
    def __init__(self, pos = Vec(-1,-1) ):
        self.color = viewConst.wbColor
        self.radius = modelConst.wb_radius
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


# class WB_List(object):
#   def __init__(self):
#       self.fps=viewConst.FramePerSec
#       self.num=modelConst.wb_init_num
#       #number of balls 
#       self.max_num=modelConst.wb_max_num
#       #max_number of balls 
#       self.born_period=modelConst.wb_born_period
#       self.wb_list=[]
#       # the list of all white balls
#       self.dead_list=[]
#       # the index list of inactive balls
#       self.dead_num=0
#       # the number of inactive balls
#         for x in range(num):
#           self.wb_list[x]=White_Ball()
#         # initialize the list of balls
#     def del_ball(self,index):
#       # call by head, delete all balls
#       self.wb_list[x].active=False
#       self.num-=1
#       self.dead_num+=1
#     def init_ball(self,pos):
#         if self.dead_num==0: 
#                 #all balls are active, so create a new ball at the end of the list
#                 new_ball=White_Ball()
#                 new_ball.pos=Vec(pos)
#                 self.wb_list.append(new_ball)
#             else:
#                 #reuse the dead ball in deadlist
#                 self.wb_list[self.dead_num-1].active=True
#                 self.wb_list[self.dead_num-1].pos=Vec(pos)
#                 self.dead_num-=1
#             self.num+=1
#     def Update(self):
#       if self.num <= self.max_num && random.randint(0,self.born_period*self.fps)==0:
#           # the num of balls < max nu m of balls
#           # && use random to check if we want to create new balls
#           #let's create new balls!
#           if self.dead_num==0: 
#               #all balls are active, so create a new ball at the end of the list
#               new_ball=White_Ball()
#               self.wb_list.append(new_ball)
#           else:
#               #reuse the dead ball in deadlist
#               self.wb_list[self.dead_num-1]=White_Ball()
#               self.dead_num-=1
#           self.num+=1
