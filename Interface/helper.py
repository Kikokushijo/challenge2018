import Model.const as modelConst
from pygame.math import Vector2 as Vec
"""
define Application Programming Interface(API) 
"""

def Vectotuple1(v):
    return (v.x, v.y)

def Vectotuple2(v_list):
    return [(v.x, v.y) for v in v_list]

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
            if self.collisionOnRoute(hPos, modelConst.head_radius, hDir, gPos, gRadius):
                dist = (gPos - hPos).length_squared()
                if dist < min_dist:
                    min_dist = dist
                    min_pos = Vec(gPos)
                    min_gRadius = gRadius
        if min_gPos is None:
            return None
        return Vectotuple1(min_gPos), min_gRadius

    def getAllGravs(self):
        return [(Vectotuple1(Vec(gPos)), gRadius) for gPos, gRadius in modelConst.grav]

    def getNearestPosToCenter(self):
        if not self.checkMeInGrav():
            return None
        gPos, gRadius = self.getMyGrav()
        hPos = self.getMyHeadPos()
        hDir = self.getMyDir()
        inner_product = (gPos - hPos).dot(hDir)
        return Vectotuple1(Vec(hPos + inner_product * (hDir)))

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
        return Vectotuple2([Vec(wb.pos) for wb in self.model.wb_list if wb.target == -1])

    def getExplosivePos(self):
        return Vectotuple2([Vec(item.pos) for item in self.model.Item_list if item.type == PROP_TYPE_EXPLOSIVE])

    def getMultibulletPos(self):
        return Vectotuple2([Vec(item.pos) for item in self.model.Item_list if item.type == PROP_TYPE_MULTIBULLET])

    def getBigbulletPos(self):
        return Vectotuple2([Vec(item.pos) for item in self.model.Item_list if item.type == PROP_TYPE_BIGBULLET])
    
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
            if self.collisionOnRoute(hPos, modelConst.head_radius, hDir, wb.pos, modelConst.wb_radius):
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
            if self.collisionOnRoute(hPos, modelConst.head_radius, hDir, wb.pos, modelConst.wb_radius):
                dist = (wb.pos - hPos).length_squared()
                if dist < min_dist:
                    min_dist = dist
                    min_pos = Vec(wb.pos)
        if min_pos == (0, 0):
            return None 
        return Vectotuple1(min_pos)

    def headOnRoute(self):
        hPos = self.getMyHeadPos()
        hDir = self.getMyDir()
        pos_list = []
        for index, player in enumerate(self.model.player_list):
            if index == self.index or (not player.is_alive):
                continue
            if self.collisionOnRoute(hPos, modelConst.head_radius, hDir, player.pos, modelConst.head_radius):
                pos_list.append(Vec(player.pos))
        return Vectotuple2(pos_list)

    def bodyOnRoute(self):
        hPos = self.getMyHeadPos()
        hDir = self.getMyDir()
        pos_list = []
        for index, player in enumerate(self.model.player_list):
            if index == self.index:
                continue
            for body in player.body_list:
                if self.collisionOnRoute(hPos, modelConst.head_radius, hDir, body.pos, modelConst.body_radius):
                    pos_list.append(Vec(body.pos))
        return Vectotuple2(pos_list)

    def collisionOnRoute(self, pos1, radius1, _dir, pos2, radius2):
        Pos1 = Vec(pos1)
        Pos2 = Vec(pos2)
        Dir = Vec(_dir)
        inner_product = (Pos2 - Pos1).dot(Dir)
        outer_product = abs((Pos2 - Pos1).cross(Dir))
        return inner_product > 0 and outer_product > 0 and outer_product < radius1 + radius2


    #me info
    def getMyIndex(self):
        return self.index

    def getMyHeadPos(self):
        return Vectotuple1(Vec(self.model.player_list[self.index].pos))

    def getMyBodyPos(self):
        return Vectotuple2([Vec(body.pos) for index, body in enumerate(model.player_list[self.index].body_list) if index > 0])

    def getMyDir(self):
        return Vectotuple1(Vec(self.model.player_list[self.index].direction))

    def getMyGrav(self):
        if not self.checkMeInGrav():
            return None
        hPos = self.getMyHeadPos()
        for gPos, gRadius in modelConst.grav:
            if (hPos - gPos).length_squared() < gRadius ** 2:
                return Vectotuple1(gPos), gRadius

    def getDashPos(self):
        if not self.checkInvisible():
            return None
        hPos = self.getMyHeadPos()
        hDir = self.getMyDir()
        return Vectotuple1(Vec(hPos + modelConst.dash_speed * self.model.player_list[self.index].dash_timer * hDir))

    def checkMeInGrav(self):
        return self.model.player_list[self.index].is_ingrav

    def checkMeCircling(self):
        return self.model.player_list[self.index].is_circling

    def checkInvisible(self):
        return self.model.player_list[self.index].is_dash

    def getMyBulletPos(self):
        return Vectotuple2([(Vec(bullet.pos), bullet.radius) for bullet in self.model.bullet_list if bullet.index == self.index])

    def getMyScore(self):
        return self.model.score_list[self.index]


    #player info
    def getPlayerHeadPos(self, player_id):
        if not self.model.player_list[player_id].is_alive:
            return None
        return Vectotuple1(Vec(self.model.player_list[player_id].pos))

    def getPlayerBodyPos(self, player_id):
        if not self.model.player_list[player_id].is_alive:
            return None
        return Vectotuple2([Vec(body.pos) for index, body in enumerate(model.player_list[player_id].body_list) if index > 0])

    def getPlayerDir(self, player_id):
        if not self.model.player_list[player_id].is_alive:
            return None
        return Vectotuple1(Vec(self.model.player_list[player_id].direction))

    def checkPlayerInGrav(self, player_id):
        if not self.model.player_list[player_id].is_alive:
            return None
        return self.model.player_list[player_id].is_ingrav

    def checktPlayerInvisible(self, player_id):
        if not self.model.player_list[player_id].is_alive:
            return None
        return self.model.player_list[player_id].is_dash

    def getAllPlayerBulletPos(self):
        return [(bullet.index, Vectotuple1(Vec(bullet.pos)), bullet.radius) for bullet in self.model.bullet_list if bullet.index != self.index]

    def getPlayerScore(self, player_id):
        if not self.model.player_list[player_id].is_alive:
            return None
        return self.model.score_list[player_id]
