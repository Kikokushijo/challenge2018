import time, random

from Events.Manager import *
from Model.StateMachine import *
from Model.GameObject.white_ball import White_Ball
from pygame.math import Vector2 as Vec
from Model.GameObject.bullet import Bullet
from Model.GameObject.head import Head
from Model.GameObject.item import Item, Explosive

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
        
        #self item
        ##explsion
        self.item_list = []
        
    def initialize(self):
        self.init_wb_list()
        self.init_player_list()
        self.init_body_list()
        self.init_bullet_list()
        self.init_item_list()

    def init_wb_list(self):
        #init wb list
        self.wb_list = []
        for i in range(modelConst.wb_init_num):
            self.wb_list.append(White_Ball(Vec(-2,-2)))
    #init item list
    def init_item_list(self):
        self.item_list = []
        for i in range(modelConst.item_init_num):
            self.item_list.append(Explosive())

    def init_player_list(self):
        self.player_list = []
        for i in range(modelConst.PlayerNum):
            self.player_list.append(Head(i,"player"+str(i)))
    def init_body_list(self):
        # No bodies at start of game
        pass
    def init_bullet_list(self):
        # No bullets at start of game
        self.bullet_list = []
    
    def create_ball(self):
        # update and see if create new ball
        if len(self.wb_list) < modelConst.wb_max_num and random.randint(0,modelConst.wb_born_period*viewConst.FramePerSec)==0:
            self.wb_list.append(White_Ball())
            
    def create_item(self):
        # update and see if create new item
        if len(self.item_list) < modelConst.item_max and random.randint(0,modelConst.item_born_period*viewConst.FramePerSec)==0:
            self.item_list.append(Explosive(self.evManager))
    
    def tick_update(self):
        #update bullets
        for i in range(len(self.bullet_list)-1,-1,-1):
            item = self.bullet_list[i]
            #update failed means the bullet should become a white ball
            if not item.update():
                self.wb_list.append(White_Ball(item.pos))
                self.bullet_list.pop(i)
        #update white balls
        if self.player_list[0].init_timer == -1:
            self.create_ball()
            self.create_item()
        #update heads
        alive = 0
        for item in self.player_list:
            if item.is_dash:
                for i in range(modelConst.dash_speed_multiplier):
                    killed = item.update(self.player_list,self.wb_list,self.bullet_list,self.item_list)
            else:
                killed = item.update(self.player_list,self.wb_list,self.bullet_list,self.item_list)
            if killed == 1:
                self.evManager.Post(Event_PlayerKilled(item.index,item.pos))
            if item.is_alive:
                alive += 1
        if alive == 1:
            self.evManager.Post(Event_GameOver())

    def notify(self, event):
        """
        Called by an event in the message queue. 
        """
        if isinstance(event, Event_EveryTick):
            cur_state = self.state.peek()
            if cur_state == STATE_PLAY:
                # every tick update
                self.tick_update() 
        elif isinstance(event, Event_MoveWayChange):
            cur_state = self.state.peek()
            if cur_state == STATE_PLAY:
                self.player_list[event.PlayerIndex].click(self.bullet_list)
        elif isinstance(event, Event_StateChange):
            # if event.state is None >> pop state.
            if event.state is None:
                # false if no more states are left
                if not self.state.pop():
                    self.evManager.Post(Event_Quit())
            elif event.state == STATE_RESTART:
                self.state.clear()
                self.state.push(STATE_MENU)
            else:
                # push a new state on the stack
                self.state.push(event.state)
        elif isinstance(event, Event_MoveWayChange):
            #modified in challenge 2018 
            #key board event
            """
            if keyboard is pressed, change the head_moving way
            """
            #print(event)
            self.player_list[event.PlayerIndex].click(self.bullet_list)
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

