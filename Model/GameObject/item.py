import Model.const as modelConst
import View.const as viewConst
from pygame.math import Vector2 as Vec
from Model.GameObject.body import Body 
from Events.Manager import *
from Model.GameObject.white_ball import White_Ball

import random
class Item(object):
    def __init__(self,type = None):
        self.type = type
        self.pos = Vec(random.randint(0+modelConst.item_radius, viewConst.ScreenSize[1]-modelConst.item_radius), random.randint(0+modelConst.item_radius, viewConst.ScreenSize[1]-modelConst.item_radius))
        self.age = 0

    def update(self):
        self.age += 1

class Explosive(Item):
    def __init__(self, evManager):
        super().__init__(modelConst.PROP_TYPE_EXPLOSIVE)
        self.radius = modelConst.item_radius
        self.color = viewConst.explosive_color
        self.evManager = evManager
    
    def trigger(self, index, player_list, wb_list):
        self.evManager.Post(Event_TriggerExplosive(index, self.pos))
        self.absorb(index, player_list, wb_list)

    def absorb(self, index, player_list, wb_list):
        #absorb whiteball

        for i in range(len(wb_list)-1,-1,-1):
            wb = wb_list[i]
            if (wb.pos - self.pos).length_squared() < modelConst.explosive_radius**2:
                wb_list.append(White_Ball(wb.pos,True,index))
                wb_list.pop(i)
        #absorb competitor's ball
        for other in player_list:
            if other.index == index:
                continue
            tag = 0
            for i in range(len(other.body_list)-1,0,-1):
                cb = other.body_list[i]
                if(cb.pos - self.pos).length_squared() < modelConst.explosive_radius**2:
                    tag = 1
            if tag == 0:
                continue
            tag = 0
            for i in range(len(other.body_list)-1,0,-1):
                cb = other.body_list[i]
                if(cb.pos - self.pos).length_squared() < modelConst.explosive_radius**2:
                    wb_list.append(White_Ball(wb.pos,True,index))
                    other.body_list.pop(i)
                    tag = 1
                elif tag == 0:
                    wb_list.append(White_Ball(wb.pos,True,index,index))
                    other.body_list.pop(i)

class Multibullet(Item):
    def __init__(self):
        super().__init__(modelConst.PROP_TYPE_MULTIBULLET)
        self.radius = modelConst.item_radius
        self.color = viewConst.multibullet_color
    
    def trigger(self, index, player_list, wb_list):
        player_list[index].have_bigbullet = False
        player_list[index].have_multibullet = True

class Bigbullet(Item):
    def __init__(self):
        super().__init__(modelConst.PROP_TYPE_BIGBULLET)
        self.radius = modelConst.item_radius
        self.color = viewConst.bigbullet_color
    
    def trigger(self, index, player_list, wb_list):
        player_list[index].have_bigbullet = True
        player_list[index].have_multibullet = False


