import time, random

from Events.Manager import *
from Model.StateMachine import *
from Model.GameObject.white_ball import White_Ball
from Model.GameObject.bullet import Bullet
from Model.GameObject.head import Head

import Model.const       as modelConst
import View.const        as viewConst
import Controller.const  as ctrlConst
import Interface.const   as IfaConst

class GameEngine(object):
    """
    Tracks the game state.
    """
    def __init__(self, evManager, AINames):
        self.evManager = evManager
        evManager.RegisterListener(self)

        self.running = False
        self.state = StateMachine()
        self.AINames = AINames
        # self.players = []
        self.TurnTo = 0

        self.player_list = []
        self.wb_list = []
        self.bullet_list = []
        
    def initialize(self):
        self.init_wb_list()
        self.init_player_list()
        self.init_bullet_list()

    def init_wb_list(self):
        #init wb list
        for i in range(modelConst.wb_init_num):
            self.wb_list.append(White_Ball())

    def init_player_list(self):
        pass

    def init_bullet_list(self):
        pass
    
    def create_ball(self):
        # update and see if create new ball
        if len(self.wb_list) < modelConst.wb_max_num and random.randint(0,modelConst.wb_born_period*viewConst.FramePerSec)==0:
            self.wb_list.append(White_Ball())
    
    def tick_update(self):
        self.create_ball()
        
        for i, item in enumerate(self.bullet_list):
            #update failed means the bullet should become a white ball
            if not item.update():
                self.wb_list.append(White_Ball(item.pos))
                del self.bullet_list[i]
        for i, item in enumerate(self.bullet_list):
            pass


    def notify(self, event):
        """
        Called by an event in the message queue. 
        """
        if isinstance(event, Event_EveryTick):
            cur_state = self.state.peek()
            if cur_state == STATE_PLAY:
                # every tick update
                self.tick_update() 





        elif isinstance(event, Event_StateChange):
            # if event.state is None >> pop state.
            if event.state == None:
                # false if no more states are left
                if not self.state.pop():
                    self.evManager.Post(Event_Quit())
            elif event.state == STATE_RESTART:
                self.state.clear()
                self.state.push(STATE_MENU)
            else:
                # push a new state on the stack
                self.state.push(event.state)

        elif isinstance(event, Event_Move):
            #key board event
            self.SetPlayerDirection(event.PlayerIndex, event.Direction)







        elif isinstance(event, Event_Quit):
            self.running = False


        elif isinstance(event, Event_Initialize) or \
             isinstance(event, Event_Restart):
            self.initialize()


    def run(self):
        """
        Starts the game engine loop.

        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify(). 
        """
        self.running = True
        self.evManager.Post(Event_Initialize())
        self.state.push(STATE_MENU)
        while self.running:
            newTick = Event_EveryTick()
            self.evManager.Post(newTick)

