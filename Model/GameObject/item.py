import Model.const as modelConst
import View.const as viewConst
from pygame.math import Vector2 as Vec
from Model.GameObject.body import Body 

import random
class Item(object):
    def __init__(self,type = None):
        self.type = type
        self.pos = Vec(random.randint(0, viewConst.ScreenSize[0]), random.randint(0, viewConst.ScreenSize[0]))

class Explosion(Item):
    def __init__(self):
        super().__init__(modelConst.PROP_TYPE_EXPLOSION)
        self.radius = modelConst.explosion_radius
        self.color = viewConst.explosion_color
    
    def trigger(self, index, player_list, wb_list):
        self.absorb(index, player_list, wb_list)

    def absorb(self, index, player_list, wb_list):
        #absorb whiteball

        for i,wb in enumerate(wb_list):
            if (wb.pos - self.pos).length_squared() < modelConst.explosion_radius**2:
                player_list[index].body_list.append(Body(player_list[index].body_list[-1]))
                del wb_list[i]
        #absorb competitor's ball
        for other in player_list:
            if other.index == index:
                continue
            for cb in other.body_list[1:]:
                if(cb.pos - self.pos).length_squared() < modelConst.explosion_radius**2:
                    player_list[index].body_list.append(Body(player_list[index].body_list[-1]))
                    other.body_list.pop()




