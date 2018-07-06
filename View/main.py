import pygame as pg
import pygame.gfxdraw as gfxdraw
import math

import Model.main as model
from Events.Manager import *

import Model.const       as modelConst
import View.const        as viewConst
import Controller.const  as ctrlConst
import Interface.const   as IfaConst
import View.teamName     as viewTeamName

class RenderObject:
    """
    Class for rendering special object.
    """
    def __init__(self, pos, time, immortal = True):
        self.pos = pos
        self.time = time
        self.totaltime = time
        self.immortal = immortal

    def update(self):
        self.time -= 1

class Explosion(RenderObject):
    """
    Class for rendering the explosion effect.
    """
    def __init__(self, index, pos, radius, time):
        super().__init__(pos, time, False)
        self.index = index
        self.radius = radius

class TimeLimitExceedStamp(RenderObject):
    """
    Class for censuring the dilatory mischiefs.
    """
    def __init__(self, pos, time):
        super().__init__(pos, time)

class MagicCircle(RenderObject):
    """
    Class for summon the Dark Bullet Death Deity.
    """
    def __init__(self, pos, time):
        super().__init__(pos, time)
        self.theta = 0.0

    def update(self):
        super().update()
        self.theta += 180 / self.totaltime if self.time > 0 else 0.1

class CountDown(RenderObject):
    """
    Class for count down.
    """
    def __init__(self, pos, time):
        super().__init__(pos, time, False)

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
        self.renderObjects = None

        self.teamNameFont = None
        self.teamLengthFont = None
        self.teamScoreFont = None
        self.countDownFont = None

        self.magicCircleImage = None

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
            elif cur_state == model.STATE_PLAY:
                self.render_play()
            elif cur_state == model.STATE_STOP:
                self.render_stop()
            elif cur_state == model.STATE_ENDGAME:
                self.render_endgame()
            elif cur_state == model.STATE_ENDMATCH:
                self.render_endmatch()

            self.display_fps()
            # limit the redraw speed to 60 frames per second
            self.clock.tick(viewConst.FramePerSec)
        elif isinstance(event, Event_TriggerExplosive):
            self.renderObjects.append(Explosion(event.PlayerIndex, event.pos, modelConst.explosive_radius, viewConst.explosionTime))
        elif isinstance(event, Event_PlayerKilled):
            self.renderObjects.append(Explosion(event.PlayerIndex, event.pos, viewConst.killedExplosionRadius, viewConst.killedExplosionTime))
        elif isinstance(event, Event_TimeLimitExceed):
            pos = ((viewConst.ScreenSize[0] + viewConst.GameSize[0]) // 2, viewConst.GameSize[1] // 8 * (2 * event.PlayerIndex + 1))
            self.renderObjects.append(TimeLimitExceedStamp(pos, viewConst.timeLimitExceedStampTime))
        elif isinstance(event, Event_SuddenDeath):
            pos = tuple([x // 2 for x in viewConst.GameSize])
            self.renderObjects.append(MagicCircle(pos, viewConst.magicCircleGenerationTime))
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
        self.teamNameFont = pg.font.Font(viewConst.teamNameFont, viewConst.teamNameFontSize)
        self.teamLengthFont = pg.font.Font(viewConst.teamLengthFont, viewConst.teamLengthFontSize)
        self.teamScoreFont = pg.font.Font(viewConst.teamScoreFont, viewConst.teamScoreFontSize)
        self.countDownFont = pg.font.Font(viewConst.countDownFont, viewConst.countDownFontSize)
        pos = tuple([x // 2 for x in viewConst.GameSize])
        self.renderObjects = [CountDown(pos, 180)]

        self.magicCircleImage = pg.image.load('View/Image/magicCircle.png').convert_alpha()

        self.is_initialized = True

    def blit_at_center(self, surface, position):
        center = tuple([int(pos - size // 2) for pos, size in zip(position, surface.get_size())])
        self.screen.blit(surface, center)

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

    def render_endgame(self):
        if self.last_update != model.STATE_ENDGAME:
            self.last_update = model.STATE_ENDGAME

            self.screen.fill(viewConst.bgColor, pg.Rect((0, 0), viewConst.GameSize))
            pg.display.flip()

    def render_endmatch(self):
        if self.last_update != model.STATE_ENDMATCH:
            self.last_update = model.STATE_ENDMATCH

    def drawScoreboard(self):
        # Frame
        gfxdraw.vline(self.screen, viewConst.GameSize[0], 0,
                      viewConst.GameSize[1], viewConst.sbColor)

        for i in range(1, modelConst.PlayerNum):
            gfxdraw.hline(self.screen, viewConst.GameSize[0],
                          viewConst.ScreenSize[0],
                          viewConst.GameSize[1] // modelConst.PlayerNum * i, viewConst.sbColor)
        # Team Names
        pos = [(viewConst.GameSize[0] + viewConst.GameSize[1] // modelConst.PlayerNum, viewConst.GameSize[1] // modelConst.PlayerNum * i + viewConst.GameSize[1] // (modelConst.PlayerNum * 8)) for i in range(modelConst.PlayerNum)]
        for i, player in enumerate(self.model.player_list):
            color = viewConst.aliveTeamColor if player.is_alive else viewConst.deadTeamColor
            teamName = self.teamNameFont.render(viewTeamName.teamName[i], True, color)
            self.screen.blit(teamName, pos[i])
        # Team Scores
        pos = [(x, y + viewConst.GameSize[1] // 32) for x, y in pos]
        for i, player in enumerate(self.model.player_list):
            color = viewConst.Color_Black
            teamScore = self.teamScoreFont.render(str(self.model.score_list[player.index]), True, color)
            self.screen.blit(teamScore, pos[i])
        # Team Balls
        pos = [(viewConst.GameSize[0] + viewConst.GameSize[1] // (modelConst.PlayerNum * 2), viewConst.GameSize[1] // (modelConst.PlayerNum * 2) * i) for i in range(1, modelConst.PlayerNum * 2, 2)]
        radius = int(viewConst.GameSize[1] // (modelConst.PlayerNum * 2) * 0.7)
        for i, player in enumerate(self.model.player_list):
            gfxdraw.filled_circle(self.screen, *(pos[i]),
                                  radius, player.color)
        # Team Player Lengths
        for i, player in enumerate(self.model.player_list):
            length = str(len(player.body_list)) if player.is_alive else '0'
            teamLength = self.teamLengthFont.render(length, True, viewConst.teamLengthColor)
            self.blit_at_center(teamLength, pos[i])

    def drawGrav(self):
        for g in modelConst.grav:
            pos = tuple(map(int, g[0]))
            radius = int(g[1] + modelConst.head_radius * 0.5)
            gfxdraw.filled_circle(self.screen, *pos,
                                  radius, viewConst.gravColor)
            gfxdraw.filled_circle(self.screen, *pos,
                                  int(radius * 0.07), viewConst.bgColor)

    def drawWhiteBall(self):
        for wb in self.model.wb_list:
            pos = tuple(map(int, wb.pos))
            radius = wb.radius
            if wb.age < viewConst.whiteBallGenerationTime:
                timeRatio = wb.age / viewConst.whiteBallGenerationTime
                if timeRatio < 0.75:
                    radius *= timeRatio * 2
                else:
                    radius *= -2 * timeRatio + 3
            gfxdraw.filled_circle(self.screen, *pos,
                                  int(radius), wb.color)

    def drawItem(self):
        for item in self.model.item_list:
            pos = tuple(map(int, item.pos))
            itemSurface = pg.Surface((int(2.2 * item.radius),) * 2, pg.SRCALPHA)
            center = tuple([x // 2 for x in itemSurface.get_size()])
            color = item.color
            if item.age < viewConst.itemGenerationTime:
                timeRatio = item.age / viewConst.itemGenerationTime
                color += (int(timeRatio * 255),)
            gfxdraw.filled_circle(itemSurface, *center,
                                  int(item.radius), color)
            gfxdraw.filled_circle(itemSurface, *center,
                                  int(item.radius * 0.7), (0, 0, 0, 0))
            self.blit_at_center(itemSurface, pos)

    def drawBody(self):
        for player in self.model.player_list:
            for body in player.body_list[1:]:
                pos = tuple(map(int, body.pos))
                gfxdraw.filled_circle(self.screen, *pos,
                                      int(body.radius), player.color)

    def drawHead(self):
        for player in self.model.player_list:
            if player.is_alive:
                pos = tuple(map(int, player.pos))
                color = player.color
                if player.is_dash:
                    color = tuple([int(i * 127 / 255 + 128) for i in color])
                gfxdraw.filled_circle(self.screen, *pos,
                                      int(player.radius), color)
                # draw triangle
                triRadius = player.radius * 0.7
                theta = math.atan2(player.direction.y, player.direction.x)

                relativeVertexStart = pg.math.Vector2(triRadius, 0).rotate(theta * 180 / math.pi)
                relativeVertices = [relativeVertexStart.rotate(i * 120) for i in range(3)]

                vertices = [player.pos + vertex for vertex in relativeVertices]
                intVertices = [int(x) for vertex in vertices for x in vertex]
                gfxdraw.filled_trigon(self.screen, *intVertices, viewConst.Color_Snow)

                if player.is_circling:
                    innerVertices = [player.pos + 0.6 * vertex for vertex in relativeVertices]
                    intInnerVertices = [int(x) for vertex in innerVertices for x in vertex]
                    gfxdraw.filled_trigon(self.screen, *intInnerVertices, color)

    def drawBullet(self):
        for bullet in self.model.bullet_list:
            color = bullet.color
            if (bullet.age // viewConst.bulletFlickerCycle) % 2 == 0:
                color = tuple([int(i * 127 / 255 + 128) for i in color])
            pos = tuple(map(int, bullet.pos))
            gfxdraw.filled_circle(self.screen, *pos,
                                  int(bullet.radius), color)

    def drawExplosion(self, explosion):
        color = self.model.player_list[explosion.index].color
        pos = tuple(map(int, explosion.pos))
        radius = explosion.radius
        timeRatio = explosion.time / explosion.totaltime

        explosionEffect = pg.Surface((int(2.1 * radius),) * 2, pg.SRCALPHA)
        center = tuple([x // 2 for x in explosionEffect.get_size()])
        gfxdraw.filled_circle(explosionEffect, *center,
                              int(1.1 * radius * (1 - timeRatio)), pg.Color(*color, int(192 * timeRatio)))
        self.blit_at_center(explosionEffect, pos)

    def drawTimeLimitExceedStamp(self, tle):
        pass

    def drawMagicCircle(self, magicCircle):
        scaleFactor = 0.3
        scaleFactor *= 1 - max(magicCircle.time / magicCircle.totaltime, 0)
        magicCircleEffect = pg.transform.rotozoom(self.magicCircleImage, magicCircle.theta, scaleFactor)
        self.blit_at_center(magicCircleEffect, magicCircle.pos)

    def drawCountDown(self, countdown):
        if countdown.time / countdown.totaltime > 2/3:
            color = viewConst.Color_Firebrick
            figure = 3
        elif countdown.time / countdown.totaltime > 1/3:
            color = viewConst.Color_Royalblue
            figure = 2
        else:
            color = viewConst.Color_Darkolivegreen
            figure = 1
        countDownFigure = self.countDownFont.render(str(figure), True, color)
        self.blit_at_center(countDownFigure, countdown.pos)

    def drawRenderObject(self):
        for renderObject in self.renderObjects:
            if isinstance(renderObject, Explosion):
                self.drawExplosion(renderObject)
            elif isinstance(renderObject, TimeLimitExceedStamp):
                self.drawTimeLimitExceedStamp(renderObject)
            elif isinstance(renderObject, MagicCircle):
                self.drawMagicCircle(renderObject)
            elif isinstance(renderObject, CountDown):
                self.drawCountDown(renderObject)
            renderObject.update()
        self.renderObjects[:] = [x for x in self.renderObjects if x.immortal or x.time > 0]

    def render_play(self):
        """
        Render the game play.
        """
        self.last_update = model.STATE_PLAY

        self.screen.fill(viewConst.bgColor)

        self.drawScoreboard()
        self.drawGrav()
        self.drawWhiteBall()
        self.drawItem()
        self.drawBody()
        self.drawHead()
        self.drawBullet()
        self.drawRenderObject()

        # To be decided: update merely the game window or the whole screen?
        pg.display.flip()
