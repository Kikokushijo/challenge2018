import Model.const as modelConst
import View.const as viewConst
from pygame.math import Vector2 as Vec


import random
class Item(object):
    def __init__(self,type = None):
        self.type = None
        self.status = False
        self.pos = Vec(random.randint(0, viewConst.ScreenSize[0]), random.randint(0, viewConst.ScreenSize[0]))
    def betriggered(self):
        self.status = False

class Explosion(Item):
    def __init__(self):
        super().__init__(modelConst.PROP_TYPE_EXPLOSION)
        self.radius = modelConst.explosion_radius
        self.color = viewConst.explosion_color
    
    def trigger(self, index, player_list, wb_list):
        super().betriggered(self)
        self.absorb(index, player_list, wb_list)

    def absorb(self, index, player_list, wb_list):
        #absorb whiteball
        for wb in (wb_list):
            if (wb.pos - self.pos).length_squre() < modelConst.explosion_radius**2:
                player_list[self.index].body_list.append(wb)
        #absorb competitor's ball
        for other in player_list:
            if other.index == self.index:
                continue
            for cb in other.body_list[1:]:
                if(cb.pos - self.pos).length_squre < modelConst.explosion_radius**2:
                    player_list[self.index].body_list.append(wb)
                    other.body_list.pop()




