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

    def getNearestGravOnRoute(self):
        hPos = self.getMyHeadPos()
        hDir = self.getMyDir()
        min_dist = float('inf')
        min_gPos = None
        min_gRadius = None
        for gPos, gRadius in modelConst.grav:
            inner_product = (gPos - hPos).dot(hDir) 
            outer_product = abs((gPos - hPos).cross(hDir))
            if inner_product > 0 and outer_product > 0 and outer_product < modelConst.head_radius + gRadius:
                dist = (gPos - hPos).length_squared()
                if dist < min_dist:
                    min_dist = dist
                    min_pos = Vec(gPos)
                    min_gRadius = gRadius
        if min_gPos is None:
            return None
        return min_gPos, min_gRadius

    def getAllGravs(self):
        return [(Vec(gPos), gRadius) for gPos, gRadius in modelConst.grav]

    def getNearestPosToCenter(self):
        if not self.checkMeInGrav():
            return None
        gPos, gRadius = self.getMyGrav()
        hPos = self.getMyHeadPos()
        hDir = self.getMyDir()
        inner_product = (gPos - hPos).dot(hDir)
        return Vec(hPos + inner_product * (hDir))

    def getBallNumInRange(self, center, radius):
        count = 0
        for wb in self.model.wb_list:
            if wb.target == -1 and (wb.pos - center).length_squared() <= radius ** 2:
                count += 1
        return count

    def getOtherBulletNumInRange(self, center, radius):
        count = 0
        for bullet in self.model.bullet_list:
            if bullet.index == self.index:
                continue
            if (bullet.pos - center).length_squared() <= radius ** 2:
                count += 1
        return count

    def getAllBallsPos(self):
        return [Vec(wb.pos) for wb in self.model.wb_list if wb.target == -1]

    def getExplosivePos(self):
        return [Vec(item.pos) for item in self.model.Item_list if item.type == PROP_TYPE_EXPLOSIVE]

    def getMultibulletPos(self):
        return [Vec(item.pos) for item in self.model.Item_list if item.type == PROP_TYPE_MULTIBULLET]

    def getBigbulletPos(self):
        return [Vec(item.pos) for item in self.model.Item_list if item.type == PROP_TYPE_BIGBULLET]
    
    def canGetByExplosion(Epos):
        count = 0
        for wb in self.model.wb_list:
            if wb.target != -1:
                continue 
            if (wb.pos - Epos).length_squared() < (modelConst.explosion_radius + modelConst.wb_radius) ** 2:
                count += 1
        return count

    def canGetBySpin(self):
        if not self.checkMeInGrav():
            return None
        gPos, gRadius = self.getMyGrav()
        inRadius = self.model.player_list[self.index].circling_radius - modelConst.dash_radius
        outRadius = self.model.player_list[self.index].circling_radius + modelConst.dash_radius
        count = 0
        for wb in self.model.wb_list:
            if wb.target != -1:
                continue 
            if (wb.pos - gPos).length_squared() > inRadius ** 2 and (wb.pos - gPos).length_squared() < outRadius ** 2:
                count += 1
        return count

    def canGetOnRoute(self):
        hPos = self.getMyHeadPos()
        hDir = self.getMyDir()
        count  = 0
        for wb in self.model.wb_list:
            if wb.target != -1:
                continue 
            inner_product = (wb.pos - hPos).dot(hDir) 
            outer_product = abs((wb.pos - hPos).cross(hDir))
            if inner_product > 0 and outer_product > 0 and outer_product < modelConst.dash_radius:
                count += 1
        return count

    def getNearestballOnRoute(self):
        hPos = self.getMyHeadPos()
        hDir = self.getMyDir()
        min_pos = Vec(0, 0)
        min_dist = float('inf')
        for wb in self.model.wb_list:
            if wb.target != -1:
                continue 
            inner_product = (wb.pos - hPos).dot(hDir) 
            outer_product = abs((wb.pos - hPos).cross(hDir))
            if inner_product > 0 and outer_product > 0 and outer_product < modelConst.dash_radius:
                dist = (wb.pos - hPos).length_squared()
                if dist < min_dist:
                    min_dist = dist
                    min_pos = Vec(wb.pos)
        if min_pos == (0, 0):
            return None 
        return min_pos

    def headOnRoute(self):
        hPos = self.getMyHeadPos()
        hDir = self.getMyDir()
        pos_list = []
        for index, player in enumerate(self.model.player_list):
            if index == self.index or (not player.is_alive):
                continue
            inner_product = (player.pos - hPos).dot(hDir) 
            outer_product = abs((player.pos - hPos).cross(hDir))
            if inner_product > 0 and outer_product > 0 and outer_product < 2 * modelConst.head_radius:
                pos_list.append(Vec(player.pos))
        return pos_list

    def bodyOnRoute(self):
        hPos = self.getMyHeadPos()
        hDir = self.getMyDir()
        pos_list = []
        for index, player in enumerate(self.model.player_list):
            if index == self.index:
                continue
            for body in player.body_list:
                inner_product = (body.pos - hPos).dot(hDir) 
                outer_product = abs((body.pos - hPos).cross(hDir))
                if inner_product > 0 and outer_product > 0 and outer_product < modelConst.dash_radius:
                    pos_list.append(Vec(body.pos))
        return pos_list

    def collisionOnRoute(self, pos, radius):
        hPos = self.getMyHeadPos()
        hDir = self.getMyDir()
        inner_product = (pos - hPos).dot(hDir)
        outer_product = abs((pos - hPos).cross(hDir))
        return inner_product > 0 and outer_product > 0 and outer_product < modelConst.head_radius + radius


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
        if not self.checkMeInGrav():
            return None
        hPos = self.getMyHeadPos()
        for gPos, gRadius in modelConst.grav:
            if (hPos - gPos).length_squared() < gRadius ** 2:
                return gPos, gRadius

    def getDashPos(self):
        if not self.checkInvisible():
            return None
        hPos = self.getMyHeadPos()
        hDir = self.getMyDir()
        return Vec(hPos + modelConst.dash_speed * self.model.player_list[self.index].dash_timer * hDir)

    def checkMeInGrav(self):
        return self.model.player_list[self.index].is_ingrav

    def checkMeCircling(self):
        return self.model.player_list[self.index].is_circling

    def checkInvisible(self):
        return self.model.player_list[self.index].is_dash

    def getMyBulletPos(self):
        return [(Vec(bullet.pos), bullet.radius) for bullet in self.model.bullet_list if bullet.index == self.index]

    def getMyScore(self):
        return self.model.score_list[self.index]


    #player info
    def getPlayerHeadPos(self, player_id):
        if not self.model.player_list[player_id].is_alive:
            return None
        return Vec(self.model.player_list[player_id].pos)

    def getPlayerBodyPos(self, player_id):
        if not self.model.player_list[player_id].is_alive:
            return None
        return [Vec(body.pos) for index, body in enumerate(model.player_list[player_id].body_list) if index > 0]

    def getPlayerDir(self, player_id):
        if not self.model.player_list[player_id].is_alive:
            return None
        return Vec(self.model.player_list[player_id].direction)

    def checkPlayerInGrav(self, player_id):
        if not self.model.player_list[player_id].is_alive:
            return None
        return self.model.player_list[player_id].is_ingrav

    def checktPlayerInvisible(self, player_id):
        if not self.model.player_list[player_id].is_alive:
            return None
        return self.model.player_list[player_id].is_dash

    def getAllPlayerBulletPos(self):
        return [(bullet.index, Vec(bullet.pos), bullet.radius) for bullet in self.model.bullet_list if bullet.index != self.index]

    def getPlayerScore(self, player_id):
        if not self.model.player_list[player_id].is_alive:
            return None
        return self.model.score_list[player_id]
