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

class Explosion(object):
    """
    Object for rendering the explosion effect
    """
    def __init__(self, index, pos, radius, time):
        self.index = index
        self.pos = pos
        self.time = time
        self.totaltime = time
        self.radius = radius

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
        self.explosionEvent = []

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
        elif isinstance(event, Event_TriggerExplosive):
            self.explosionEvent.append(Explosion(event.PlayerIndex, event.pos, modelConst.explosive_radius, viewConst.explosionTime))
        elif isinstance(event, Event_PlayerKilled):
            self.explosionEvent.append(Explosion(event.PlayerIndex, event.pos, viewConst.killedExplosionRadius, viewConst.killedExplosionTime))
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
            itemSurface = pg.Surface((int(2.2 * item.radius), int(2.2 * item.radius)), SRCALPHA)
            Xsize, Ysize = itemSurface.get_size()
            draw.filled_circle(itemSurface, Xsize // 2, Ysize // 2, \
                               int(item.radius), item.color)
            draw.filled_circle(itemSurface, Xsize // 2, Ysize // 2, \
                               int(item.radius * 0.7), (0, 0, 0, 0))
            self.blit_at_center(itemSurface, pos)

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
                vertex1_relative = pg.math.Vector2(triRadius, 0).rotate(theta * 180 / math.pi)
                vertex2_relative = vertex1_relative.rotate(120)
                vertex3_relative = vertex1_relative.rotate(240)
                vertex1 = player.pos + vertex1_relative
                vertex2 = player.pos + vertex2_relative
                vertex3 = player.pos + vertex3_relative
                draw.filled_trigon(self.screen, int(vertex1[0]), int(vertex1[1]), int(vertex2[0]), int(vertex2[1]), int(vertex3[0]), int(vertex3[1]), viewConst.Color_Snow)
                if player.is_circling and player.is_ingrav:
                    inner_vertex1 = player.pos + 0.6 * vertex1_relative
                    inner_vertex2 = player.pos + 0.6 * vertex2_relative
                    inner_vertex3 = player.pos + 0.6 * vertex3_relative
                    draw.filled_trigon(self.screen, int(inner_vertex1[0]), int(inner_vertex1[1]), int(inner_vertex2[0]), int(inner_vertex2[1]), int(inner_vertex3[0]), int(inner_vertex3[1]), player.color)

        for bullet in self.model.bullet_list:
            color = self.model.player_list[bullet.index].color
            pos = (int(bullet.pos[0]), int(bullet.pos[1]))
            draw.filled_circle(self.screen, pos[0], pos[1], \
                               int(bullet.radius), color)

        for i in range(len(self.explosionEvent)-1,-1,-1):
            explosion = self.explosionEvent[i]
            if explosion.time > 0:
                explosion.time -= 1
                color = self.model.player_list[explosion.index].color
                pos = (int(explosion.pos[0]), int(explosion.pos[1]))
                radius = explosion.radius
                explosionEffect = pg.Surface((int(2.1 * radius), int(2.1 * radius)), SRCALPHA)
                Xsize, Ysize = explosionEffect.get_size()
                draw.filled_circle(explosionEffect, Xsize // 2, Ysize // 2, \
                                   int(1.1 * radius * (1 - explosion.time / explosion.totaltime)), Color(*color, int(192 * (explosion.time / explosion.totaltime))))
                self.blit_at_center(explosionEffect, pos)
            else:
                self.explosionEvent.pop(i)

        # update the scene
        # To be decided: update merely the game window or the whole screen?
        pg.display.flip()
