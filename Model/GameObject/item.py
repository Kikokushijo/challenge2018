import Model.const as mc
import View.const as viewConst
from Model.GameObject.utils import Vec

import random
class Item(object):
    def __init__(self):
        self.type = None
        self.status = False
        self.pos = Vec(random.randint(0, viewConst.ScreenSize[0]), random.randint(0, viewConst.ScreenSize[0]))


