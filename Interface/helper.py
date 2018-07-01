import Model.const as modelConst
from Model.gameObjects.utils import Vec   
"""
define Application Programming Interface(API) 
"""
class Helper(object):
    def __init__(self, model, index):
        self.model = model
        self.index = index
    
    #map info
    def getNearsetGrav(self):
        pos = self.model.Head.player[self.index].pos
        min_value = float('inf')
        min_index = None
        for index, (gPos, gRadius) in enumerate(modelConst.grav):
            dist = (gPos - pos).mag() - gRadius
            if dist < min_value:
                min_value = dist
                min_index = index
        return min_index

    def getAllGravs(self):
        return [(Vec(gPos), gRadius) for gPos, gRadius in modelConst.grav]


    #me info
    def getMyIndex(self):
        return self.index

    def getMyHeadPos(self):
        return Vec(self.model.Head.player[self.index].pos)

    def getMyDir(self):
        return Vec(self.model.Head.player[self.index].direction)

    def checkMeInGrav(self):
        return self.model.Head.player[self.index].is_incircle

    def checkMeCircling(self):
        if not checkMeInGrav(self):
            return None

        return self.model.Head.player[self.index].is_circling

    def checkInvsible(self):
        return self.model.Head.player[self.index].dash_timer > 0


    #player info
    def getPlayerHeadPos(self, player_id):
        return Vec(self.model.Head.player[player_id].pos)

    def getPlayerDir(self, player_id):
        return Vec(self.model.Head.player[player_id].direction)

    def checkPlayerInGrav(self, player_id):
        return self.model.Head.player[player_id].is_incircle

    def checktPlayerInvisible(self, player_id)
        return self.model.Head.player[player_id].dash_timer > 0





