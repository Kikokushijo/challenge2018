import Model.const as modelConst

"""
define Application Programming Interface(API) 
"""
class Helper(object):
    def __init__(self, model, index):
        self.model = model
        self.index = index

    def getNearsetCircle(self):
        pos = self.model.Head.player[self.index].pos
        min_value = float('inf')
        min_index = None
        for index, (gPos, gRadius) in enumerate(modelConst.grav):
            dist = (gPos - pos).mag() - gRadius
            if dist < min_value:
                min_value = dist
                min_index = index
        return min_index




