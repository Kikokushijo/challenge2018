import time, random

from Events.Manager import *
from Model.StateMachine import *
from Model.GameObject.white_ball import *

import Model.const       as modelConst
import View.const        as viewConst
import Controller.const  as ctrlConst
import Interface.const   as IfaConst

class GameEngine(object):
    """
    Tracks the game state.
    """
    def __init__(self, evManager, AINames):
        self.Player = []
        self.wb_list = []
        self.bullet_list = []
        
    def initialize(self):
        self.init_wb_list()
		self.init_Player()
		self.init_bullet_list()

    def init_wb_list(self):
        #init wb list
        for i in range(modelConst.wb_init_num):
            self.wb_list.append(White_Ball())
    def init_head_list(self):
        pass
    def init_bullet_list(self):
        pass
    
    def create_ball(self):
        # update and see if create new ball
        if len(self.wb_list) < modelConst.wb_max_num and random.randint(0,modelConst.wb_born_period*viewConst.FramePerSec)==0:
            self.wb_list.append(White_Ball())
    
    def update_objects(self):
        self.create_ball()
        
        for i, item in enumerate(self.bullet_list):
            #update failed means the bullet should become a white ball
            if not item.update():
                self.wb_list.append(White_Ball(item.pos))
                del self.bullet_list[i]
