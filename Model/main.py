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
        self.wb_list=[]

    def Initialize(self):
        self.init_wb_list()

    def init_wb_list(self):
        #init wb list
        for i in range(modelConst.wb_init_num):
            self.wb_list.append(White_Ball())

    def create_ball(self):
        # update and see if create new ball
        if len(self.wb_list) < modelConst.wb_max_num and random.randint(0,modelConst.wb_born_period*viewConst.FramePerSec)==0:
            self.wb_list.append(White_Ball())
    
    def UpdateObjects(self):
        self.create_ball()
