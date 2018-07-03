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

    def getNearsetPosToCenter(self):
        if not checkMeInGrav(self):
            return None
        gPos, gRadius = getMyGrav(self)
        hPos = getMyHeadPos(self)
        hDir = getMyDir(self)
        inner_product = (gPos - hPos).dot(hDir)
        return Vec(hPos + inner_product * (hDir))

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

    def canGetBySpin(self):
        if not checkMeInGrav(self):
            return None
        gPos, gRadius = getMyGrav(self)
        inRadius = self.model.player_list[self.index].circling_radius - modelConst.dash_redius
        outRadius = self.model.player_list[self.index].circling_radius + modelConst.dash_redius
        count = 0
        for wb in self.model.wb_list:
            if (wb.pos - gPos).magnitude_squared() > inRadius ** 2 and (wb.pos - gPos).magnitude_squared() < outRadius ** 2:
                count += 1
        return count

    def canGetOnRoute(self):
        hPos = getMyHeadPos(self)
        hDir = getMyDir(self)
        count  = 0
        for wb in self.model.wb_list:
            inner_product = (wb.pos - hPos).dot(hDir) 
            outer_product = abs((wb.pos - hPos).cross(hDir))
            if inner_product > 0 and outer_product > 0 and outer_product < modelConst.dash_redius:
                count += 1
        return count

    def getNearestballOnRoute(self):
        hPos = getMyHeadPos(self)
        hDir = getMyDir(self)
        min_pos = Vec(0, 0)
        min_dist = float('inf')
        for wb in self.model.wb_list:
            inner_product = (wb.pos - hPos).dot(hDir) 
            outer_product = abs((wb.pos - hPos).cross(hDir))
            if inner_product > 0 and outer_product > 0 and outer_product < modelConst.dash_redius:
                dist = (wb.pos - hPos).magnitude_squared()
                if dist < min_dist:
                    min_dist = dist
                    min_pos = Vec(wb.pos)
        return min_pos

    def headOnRoute(self):
        hPos = getMyHeadPos(self)
        hDir = getMyDir(self)
        list = []
        for index, player in enumerate(self.model.player_list):
            if index == self.index:
                continue
            inner_product = (player.pos - hPos).dot(hDir) 
            outer_product = abs((player.pos - hPos).cross(hDir))
            if inner_product > 0 and outer_product > 0 and outer_product < 2 * modelConst.head_redius:
                list.append()
        return list

    def bodyOnRoute(self):
        hPos = getMyHeadPos(self)
        hDir = getMyDir(self)
        list = []
        for index, player in enumerate(self.model.player_list):
            if index == self.index:
                continue
            for body in player.body_list:
                inner_product = (body.pos - hPos).dot(hDir) 
                outer_product = abs((body.pos - hPos).cross(hDir))
                if inner_product > 0 and outer_product > 0 and outer_product < modelConst.dash_redius:
                    list.append()
        return list


    #me info
    def getMyIndex(self):
        return self.index

    def getMyHeadPos(self):
        return Vec(self.model.player_list[self.index].pos)

    def getMyBodyPos(self):
        return [Vec(body.pos) for index, body in enumerate(model.player_list[self.index].body_list) if index > 0]

    def getMyDir(self):
        return Vec(self.model.player_list[self.index].direction)

    def getMyGrav(self):
        if not checkMeInGrav(self):
            return None
        hPos = getMyHeadPos(self)
        for gPos, gRadius in modelConst.grav:
            if (hPos - gPos).magnitude_squared() < gRadius ** 2:
                return gPos, gRadius

    def getDashPos(self):
        if not checkInvsible(self):
            return None
        hPos = getMyHeadPos(self)
        hDir = getMyDir(self)
        return Vec(hPos + dash_speed * self.model.player_list[self.index].dash_timer * hDir)

    def checkMeInGrav(self):
        return self.model.player_list[self.index].is_ingrav

    def checkMeCircling(self):
        return self.model.player_list[self.index].is_circling

    def checkInvsible(self):
        return self.model.player_list[self.index].is_dash

    def getMyShotPos(self):
        return [Vec(bullet.pos) for bullet in self.model.bullet_list if bullet.index == self.index]


    #player info
    def getPlayerHeadPos(self, player_id):
        return Vec(self.model.player_list[player_id].pos)

    def getPlayerBodyPos(self, player_id):
        return [Vec(body.pos) for index, body in enumerate(model.player_list[player_id].body_list) if index > 0]

    def getPlayerDir(self, player_id):
        return Vec(self.model.player_list[player_id].direction)

    def checkPlayerInGrav(self, player_id):
        return self.model.player_list[player_id].is_ingrav

    def checktPlayerInvisible(self, player_id):
        return self.model.player_list[player_id].is_dash

    def checktPlayerInvisible(self, player_id):
        return self.model.player_list[player_id].dash_timer > 0

    def getPlayerShotPos(self, player_id):
        return [Vec(bullet.pos) for bullet in self.model.bullet_list if bullet.index == player_id]
