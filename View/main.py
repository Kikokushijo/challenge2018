import pygame as pg
import pygame.gfxdraw as draw
from pygame.locals import *
import math

import Model.main as model
from Events.Manager import *

import Model.const       as modelConst
import View.const        as viewConst
import Controller.const  as ctrlConst
import Interface.const   as IfaConst

class GraphicalView(object):
    """
    Draws the model state onto the screen.
    """
    def __init__(self, evManager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model

        self.is_initialized = False
        self.screen = None
        self.clock = None
        self.smallfont = None

        self.last_update = 0
    
    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """
        if isinstance(event, Event_EveryTick) \
           and self.is_initialized:
            cur_state = self.model.state.peek()
            if cur_state == model.STATE_MENU:
                self.render_menu()
            if cur_state == model.STATE_PLAY:
                self.render_play()
            if cur_state == model.STATE_STOP:
                self.render_stop()

            self.display_fps()
            # limit the redraw speed to 30 frames per second
            self.clock.tick(viewConst.FramePerSec)
        elif isinstance(event, Event_Quit):
            # shut down the pygame graphics
            self.is_initialized = False
            pg.quit()
        elif isinstance(event, Event_Initialize) or\
             isinstance(event, Event_Restart):
            self.initialize()

    def display_fps(self):
        """Show the programs FPS in the window handle."""
        caption = "{} - FPS: {:.2f}".format(
            viewConst.GameCaption, self.clock.get_fps()
        )
        pg.display.set_caption(caption)

    def initialize(self):
        """
        Set up the pygame graphical display and loads graphical resources.
        """
        pg.init(); pg.font.init()
        pg.display.set_caption(viewConst.GameCaption)
        self.screen = pg.display.set_mode(viewConst.ScreenSize)
        self.clock = pg.time.Clock()
        self.smallfont = pg.font.Font(None, 40)

        self.is_initialized = True

    def blit_at_center(self, surface, position):
        (Xsize, Ysize) = surface.get_size()
        self.screen.blit(surface, (int(position[0]-Xsize/2), int(position[1]-Ysize/2)))

    # to be modified
    def render_menu(self):
        """
        Render the game menu.
        """
        if self.last_update != model.STATE_MENU:
            self.last_update = model.STATE_MENU

            # draw backgound
            self.screen.fill(viewConst.Color_Black)
            # write some word
            somewords = self.smallfont.render(
                        'You are in the Menu. Space to play. Esc exits.', 
                        True, (0, 255, 0))
            (SurfaceX, SurfaceY) = somewords.get_size()
            pos_x = (viewConst.ScreenSize[0] - SurfaceX)/2
            pos_y = (viewConst.ScreenSize[1] - SurfaceY)/2
            self.screen.blit(somewords, (pos_x, pos_y))
            # update surface
            pg.display.flip()
        
    # to be modified
    def render_stop(self):
        """
        Render the stop screen.
        """
        if self.last_update != model.STATE_STOP:
            self.last_update = model.STATE_STOP

            # draw backgound
            s = pg.Surface(viewConst.ScreenSize, pg.SRCALPHA)
            s.fill((0, 0, 0, 128)); self.screen.blit(s, (0,0))

            # write some word
            somewords = self.smallfont.render(
                        'stop the game. space, escape to return the game.', 
                        True, (0, 255, 0))
            (SurfaceX, SurfaceY) = somewords.get_size()
            pos_x = (viewConst.ScreenSize[0] - SurfaceX)/2
            pos_y = (viewConst.ScreenSize[1] - SurfaceY)/2
            self.screen.blit(somewords, (pos_x, pos_y))

            # update surface
            pg.display.flip()

    def render_play(self):
        """
        Render the game play.
        """
        self.last_update = model.STATE_PLAY

        self.screen.fill(viewConst.bgColor)

        # draw scoreboard
        draw.vline(self.screen, viewConst.GameSize[0], 0, \
                   viewConst.GameSize[1], viewConst.sbColor)

        for i in range(1, 4):
            draw.hline(self.screen, viewConst.GameSize[0], \
                       viewConst.ScreenSize[0], \
                       viewConst.GameSize[1] // 4 * i, viewConst.sbColor)

        for g in modelConst.grav:
            pos = (int(g[0][0]), int(g[0][1]))
            r = int(g[1] + modelConst.head_radius * 0.5)
            draw.filled_circle(self.screen, pos[0], pos[1], \
                               r, viewConst.gravColor)
            draw.filled_circle(self.screen, pos[0], pos[1], \
                               int(r * 0.07), viewConst.bgColor)

        for wb in self.model.wb_list:
            pos = (int(wb.pos[0]), int(wb.pos[1]))
            draw.filled_circle(self.screen, pos[0], pos[1], \
                               int(wb.radius), viewConst.wbColor)

        for item in self.model.item_list:
            pos = (int(item.pos[0]), int(item.pos[1]))
            draw.filled_circle(self.screen, pos[0], pos[1], \
                               int(item.radius), item.color)

        for player in self.model.player_list:
            for body in player.body_list[1:]:
                pos = (int(body.pos[0]), int(body.pos[1]))
                draw.filled_circle(self.screen, pos[0], pos[1], \
                                   int(body.radius), player.color)

        for player in self.model.player_list:
            if player.is_alive:
                pos = (int(player.pos[0]), int(player.pos[1]))
                draw.filled_circle(self.screen, pos[0], pos[1], \
                                   int(player.radius), player.color)
                triRadius = player.radius * 0.7
                theta = math.atan2(player.direction.y, player.direction.x)
                x1, y1 = triRadius, 0
                x2, y2 = -0.5 * triRadius, math.sqrt(3) / 2 * triRadius
                x3, y3 = x2, -y2
                x1, y1 = x1 * math.cos(theta) - y1 * math.sin(theta), x1 * math.sin(theta) + y1 * math.cos(theta)
                x2, y2 = x2 * math.cos(theta) - y2 * math.sin(theta), x2 * math.sin(theta) + y2 * math.cos(theta)
                x3, y3 = x3 * math.cos(theta) - y3 * math.sin(theta), x3 * math.sin(theta) + y3 * math.cos(theta)
                sx1, sy1 = int(x1 * 0.6 + player.pos[0]), int(y1 * 0.6 + player.pos[1])
                sx2, sy2 = int(x2 * 0.6 + player.pos[0]), int(y2 * 0.6 + player.pos[1])
                sx3, sy3 = int(x3 * 0.6 + player.pos[0]), int(y3 * 0.6 + player.pos[1])
                x1, y1 = int(x1 + player.pos[0]), int(y1 + player.pos[1])
                x2, y2 = int(x2 + player.pos[0]), int(y2 + player.pos[1])
                x3, y3 = int(x3 + player.pos[0]), int(y3 + player.pos[1])
                if player.is_circling and player.is_ingrav:
                    draw.filled_trigon(self.screen, x1, y1, x2, y2, x3, y3, viewConst.Color_Snow)
                    draw.filled_trigon(self.screen, sx1, sy1, sx2, sy2, sx3, sy3, player.color)
                else:
                    draw.filled_trigon(self.screen, x1, y1, x2, y2, x3, y3, viewConst.Color_Snow)

        for bullet in self.model.bullet_list:
            color = self.model.player_list[bullet.index].color
            pos = (int(bullet.pos[0]), int(bullet.pos[1]))
            draw.filled_circle(self.screen, pos[0], pos[1], \
                               int(bullet.radius), color)

        # update the scene
        # To be decided: update merely the game window or the whole screen?
        pg.display.flip()
