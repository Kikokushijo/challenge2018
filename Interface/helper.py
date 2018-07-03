import Model.const as modelConst
from pygame.math import Vector2 as Vec
"""
define Application Programming Interface(API) 
"""
class Helper(object):
    def __init__(self, model, index):
        self.model = model
        self.index = index
    
    #map info
    def getExplosionRadius(self):
        return modelConst.explosion_radius

    def getWhiteballRadius(self):
        return modelConst.wb_radius

    def getNearsetGrav(self):
        pos = self.model.player_list[self.index].pos
        min_value = float('inf')
        min_index = None
        for index, (gPos, gRadius) in enumerate(modelConst.grav):
            dist = (gPos - pos).magnitude() - gRadius
            if dist < min_value:
                min_value = dist
                min_index = index
        return min_index

    def getAllGravs(self):
        return [(Vec(gPos), gRadius) for gPos, gRadius in modelConst.grav]

    def getBallNumInRange(self, center, radius):
        count = 0
        for wb in self.model.wb_list:
            if (wb.pos - center).magnitude_squared() <= radius ** 2:
                count += 1
        return count

    def getAllBallsPos(self):
        return [Vec(wb.pos) for wb in self.model.wb_list]

    def getExplosionPos(self):
        return [Vec(item.pos) for item in self.model.Item_list]
    
    def canGetByExplosion(Epos):
        count = 0
        for wb in self.model.wb_list:
            if (wb.pos - Epos).magnitude_squared() < (modelConst.explosion_radius + modelConst.wb_radiu) ** 2:
                count += 1
        return count

    #me info
    def getMyIndex(self):
        return self.index

    def getMyHeadPos(self):
        return Vec(self.model.player_list[self.index].pos)

    def getMyDir(self):
        return Vec(self.model.player_list[self.index].direction)

    def checkMeInGrav(self):
        return self.model.player_list[self.index].is_ingrav

    def checkMeCircling(self):
        return self.model.player_list[self.index].is_circling

    def checkInvsible(self):
        return self.model.player_list[self.index].dash_timer > 0

    def getMyShotPos(self):
        return [Vec(bullet.pos) for bullet in self.model.bullet_list if bullet.index == self.index]


    #player info
    def getPlayerHeadPos(self, player_id):
        return Vec(self.model.player_list[player_id].pos)

    def getPlayerDir(self, player_id):
        return Vec(self.model.player_list[player_id].direction)

    def checkPlayerInGrav(self, player_id):
        return self.model.player_list[player_id].is_ingrav

    def checktPlayerInvisible(self, player_id):
        return self.model.player_list[player_id].dash_timer > 0

    def getPlayerShotPos(self, player_id):
        return [Vec(bullet.pos) for bullet in self.model.bullet_list if bullet.index == player_id]
