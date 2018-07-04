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

        self.headIcon = None
        self.headIcon2 = None

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

        self.headIcon = pg.image.load('View/Image/headIcon.png').convert_alpha()
        self.headIcon = pg.transform.scale(self.headIcon, (int(modelConst.head_radius * 1.3), \
                         int(modelConst.head_radius * 1.3)))
        self.headIcon2 = pg.image.load('View/Image/headIcon2.png').convert_alpha()
        self.headIcon2 = pg.transform.scale(self.headIcon2, (int(modelConst.head_radius * 1.3), \
                         int(modelConst.head_radius * 1.3)))

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

        for player in self.model.player_list:
            for body in player.body_list[1:]:
                pos = (int(body.pos[0]), int(body.pos[1]))
                draw.filled_circle(self.screen, pos[0], pos[1], \
                                   int(body.radius), player.color)

        for player in self.model.player_list:
            if player.is_alive:
                pos = (int(player.pos[0]), int(player.pos[1]))
                playerImage = pg.Surface((2 * int(player.radius), 2 * int(player.radius)), SRCALPHA)
                draw.filled_circle(playerImage, int(player.radius), int(player.radius), \
                                   int(player.radius), player.color)
                if not player.is_dash:
                    if player.is_circling:
                        (Xsize, Ysize) = self.headIcon.get_size()
                        playerImage.blit(self.headIcon, (int(player.radius - Xsize/2), int(player.radius - Ysize/2)))
                    else:
                        (Xsize, Ysize) = self.headIcon2.get_size()
                        playerImage.blit(self.headIcon2, (int(player.radius - Xsize/2), int(player.radius - Ysize/2)))
                    playerImage = pg.transform.rotate(playerImage, (player.theta - math.pi/2) * 180.0 / math.pi)
                else:
                    maxDashTime = modelConst.max_dash_time * modelConst.dash_speed_multiplier
                    if not maxDashTime // 4 < player.dash_timer < maxDashTime // 4 * 3:
                        (Xsize, Ysize) = self.headIcon2.get_size()
                        playerImage.blit(self.headIcon2, (int(player.radius - Xsize/2), int(player.radius - Ysize/2)))
                    scalingFactor = abs(math.cos(player.dash_timer / maxDashTime * 2 * math.pi))
                    playerImage = pg.transform.scale(playerImage, (2 * int(player.radius * scalingFactor), 2 * int(player.radius)))
                    if scalingFactor > 0.1:
                        playerImage = pg.transform.rotate(playerImage, (player.theta - math.pi/2) * 180.0 / math.pi)
                self.blit_at_center(playerImage, pos)

        for bullet in self.model.bullet_list:
            color = self.model.player_list[bullet.index].color
            pos = (int(bullet.pos[0]), int(bullet.pos[1]))
            draw.filled_circle(self.screen, pos[0], pos[1], \
                               int(bullet.radius), color)

        # update the scene
        # To be decided: update merely the game window or the whole screen?
        pg.display.flip()
