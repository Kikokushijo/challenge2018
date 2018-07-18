import pygame as pg
import pygame.gfxdraw as gfxdraw
import math, random
import sys

from itertools import zip_longest

import Model.main as model
from Events.Manager import *

import Model.const       as modelConst
import View.const        as viewConst
import View.renderObject as renderObject
import Controller.const  as ctrlConst
import Interface.const   as IfaConst

class GraphicalView(object):
    """
    Draws the model state onto the screen.
    """
    def __init__(self, evManager, model, cutin, ci_img=None):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model

        self.is_initialized = False
        self.screen = None
        self.renderSurface = None
        self.gameSurface = None
        self.clock = None
        self.renderObjects = None
        self.CIImg = ci_img if ci_img is not None else []

        # initialize pygame modules
        # pg.mixer.pre_init(44100, -16, 2, 2048);
        pg.init();
        # pg.mixer.quit();

        # initialize game window
        pg.display.set_caption(viewConst.GameCaption)
        self.screen = pg.display.set_mode(viewConst.ScreenSize)

        # load sounds and music
        # self.backgroundMusic = pg.mixer.Sound('View/Sound/bgm.ogg')
        # self.explosionSound = pg.mixer.Sound('View/Sound/explosion.ogg')
        # self.badExplosionSound = pg.mixer.Sound('View/Sound/explosion2.ogg')
        # self.dashSound = pg.mixer.Sound('View/Sound/dash.ogg')
        # self.meowSound = pg.mixer.Sound('View/Sound/meow.ogg')
        # self.rainbowSound = pg.mixer.Sound('View/Sound/rainbow.ogg')
        # self.magicCircleSound = pg.mixer.Sound('View/Sound/magicCircle.ogg')
        # self.resonanceSound = pg.mixer.Sound('View/Sound/resonance.ogg')
        # self.vibrationSound = pg.mixer.Sound('View/Sound/resonance2.ogg')
        # self.trueExplosionSound = pg.mixer.Sound('View/Sound/explosion3.ogg')

        # load fonts
        self.titleFont = pg.font.Font(viewConst.titleFont, viewConst.titleFontSize)
        self.titleSmallFont = pg.font.Font(viewConst.titleSmallFont, viewConst.titleSmallFontSize)
        self.teamNameFont = pg.font.Font(viewConst.teamNameFont, viewConst.teamNameFontSize)
        self.teamLengthFont = pg.font.Font(viewConst.teamLengthFont, viewConst.teamLengthFontSize)
        self.teamScoreFont = pg.font.Font(viewConst.teamScoreFont, viewConst.teamScoreFontSize)
        self.countDownFont = pg.font.Font(viewConst.countDownFont, viewConst.countDownFontSize)
        self.tmpScoreFont = pg.font.Font(viewConst.tmpScoreFont, viewConst.tmpScoreFontSize)

        # load images
        self.magicCircleImage = pg.image.load('View/Image/magicCircle.png').convert_alpha()
        self.rainbowImage = pg.transform.scale(pg.image.load('View/Image/rainbow.jpg').convert(), viewConst.GameSize)
        self.nyanCatImage = pg.transform.rotozoom(pg.image.load('View/Image/nyancat.png').convert_alpha(), 0, 0.5)
        self.nyanCatTailImage = pg.transform.rotozoom(pg.image.load('View/Image/nyancattail.png').convert_alpha(), 0, 0.5)

        self.defaultCutInImageNames  = ['Darkviolet', 'Royalblue', 'Saddlebrown', 'Darkolivegreen']
        self.existedImageNames = set([str(i) for i in range(1, 11)])
        self.cutInImageNames = []
        for custImg, dftImg in zip_longest(self.CIImg, self.defaultCutInImageNames):
            if custImg in self.existedImageNames:
                self.cutInImageNames.append(custImg)
            else:
                self.cutInImageNames.append(dftImg)

        # self.cutInImage       = [(pg.image.load('View/Image/Darkviolet.png').convert_alpha(),
        #                           pg.image.load('View/Image/Darkviolet_bw.png').convert_alpha()),
        #                          (pg.image.load('View/Image/Royalblue.png').convert_alpha(),
        #                           pg.image.load('View/Image/Royalblue_bw.png').convert_alpha()),
        #                          (pg.image.load('View/Image/Saddlebrown.png').convert_alpha(),
        #                           pg.image.load('View/Image/Saddlebrown_bw.png').convert_alpha())]

        self.cutInImage       = [(pg.image.load('View/Image/CutInImages/%s/%s.png' % (name, name)).convert_alpha(),
                                  pg.image.load('View/Image/CutInImages/%s/%s_bw.png' % (name, name))) for name in self.cutInImageNames]
        # self.cutInImageSmall = [tuple([pg.transform.scale(img1, viewConst.skillCardCutInPicSmallSize),
        #                                pg.transform.scale(img2, viewConst.skillCardCutInPicSmallSize)])
        #                               for img1, img2 in self.cutInImage]
        self.cutInImageSmall = []
        rangex, rangey = viewConst.skillCardCutInPicSmallSize
        for img1, img2 in self.cutInImage:
            x1, y1 = img1.get_size()
            x2, y2 = img2.get_size()
            self.cutInImageSmall.append((pg.transform.rotozoom(img1, 0, min(rangex/x1, rangey/y1)),
                                         pg.transform.rotozoom(img2, 0, min(rangex/x2, rangey/y2))))

        # self.cutInImageTrans1      = [pg.image.load('View/Image/Darkviolet_trans1.png').convert_alpha(),
        #                               pg.image.load('View/Image/Royalblue_trans1.png').convert_alpha(),
        #                               pg.image.load('View/Image/Saddlebrown_trans1.png').convert_alpha()]
        self.cutInImageTrans1      = [pg.image.load('View/Image/CutInImages/%s/%s_trans1.png' % (name, name)).convert_alpha()
                                      for name in self.cutInImageNames]


        # self.cutInImageTransSmall  = [pg.transform.scale(img, viewConst.skillCardCutInPicSmallSize)
        #                               for img in self.cutInImageTrans1]
        self.cutInImageTransSmall = []
        rangex, rangey = viewConst.skillCardCutInPicSmallSize
        for img in self.cutInImageTrans1:
            x, y = img.get_size()
            self.cutInImageTransSmall.append(pg.transform.rotozoom(img, 0, min(rangex/x, rangey/y)))

        # self.cutInImageTrans2      = [pg.image.load('View/Image/Darkviolet_trans2.png').convert_alpha(),
        #                               pg.image.load('View/Image/Royalblue_trans2.png').convert_alpha(),
        #                               pg.image.load('View/Image/Saddlebrown_trans2.png').convert_alpha()]
        self.cutInImageTrans2      = [pg.image.load('View/Image/CutInImages/%s/%s_trans2.png' % (name, name)).convert_alpha()
                                      for name in self.cutInImageNames]

        # self.cutInImageTransLarge = [pg.transform.scale(img, viewConst.skillCardCutInPicLargeSize)
        #                               for img in self.cutInImageTrans2]
        self.cutInImageTransLarge = []
        rangex, rangey = viewConst.skillCardCutInPicLargeSize
        for img in self.cutInImageTrans2:
            x, y = img.get_size()
            self.cutInImageTransLarge.append(pg.transform.rotozoom(img, 0, min(rangex/x, rangey/y)))

        self.last_update = 0

        self.has_cutin = cutin
        print('Init', cutin)
    
    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """
        if isinstance(event, Event_EveryTick) \
           and self.is_initialized:
            cur_state = self.model.state.peek()
            if cur_state == model.STATE_MENU:
                self.render_menu()
            elif cur_state == model.STATE_PLAY or cur_state == model.STATE_CUTIN:
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
            # self.explosionSound.play()
            self.renderObjects.append(renderObject.Explosion(event.PlayerIndex, event.pos, modelConst.explosive_radius, viewConst.explosionTime))
        elif isinstance(event, Event_PlayerKilled):
            # self.badExplosionSound.play()
            self.renderObjects.append(renderObject.Explosion(event.PlayerIndex, event.pos, viewConst.killedExplosionRadius, viewConst.killedExplosionTime))
        elif isinstance(event, Event_TimeLimitExceed):
            pos = ((viewConst.ScreenSize[0] + viewConst.GameSize[0]) // 2, viewConst.GameSize[1] // 8 * (2 * event.PlayerIndex + 1))
            self.renderObjects.append(renderObject.TimeLimitExceedStamp(pos, viewConst.timeLimitExceedStampTime))
        elif isinstance(event, Event_SuddenDeath):
            # self.magicCircleSound.play()
            pos = tuple([x // 2 for x in viewConst.GameSize])
            self.renderObjects.append(renderObject.MagicCircle(pos, viewConst.magicCircleGenerationTime))
        elif isinstance(event, Event_CutIn):
            pos = tuple([x // 2 for x in viewConst.GameSize])
            if self.has_cutin:
                # self.trueExplosionSound.play()
                if not str(self.CIImg[event.PlayerIndex]).isdigit():
                    # self.trueExplosionSound.play()
                    pass

                self.renderObjects.append(renderObject.SkillCardCutIn(event.PlayerIndex, pos, viewConst.skillCardCutInTime, event.number, isdisplay=True))
                if event.number == 6:
                    self.renderObjects.append(renderObject.Rainbow(event.PlayerIndex, (0, 0), 510, True))
                elif event.number == 7:
                    # self.resonanceSound.play()
                    self.renderObjects.append(renderObject.HyperdimensionalExplosion(event.PlayerIndex, self.model.player_list[event.PlayerIndex].pos, 450, True))
            else:
                self.renderObjects.append(renderObject.SkillCardCutIn(event.PlayerIndex, pos, 1, event.number, isdisplay=False))
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
        Set up the pygame graphical display.
        """
        self.renderSurface = pg.Surface(viewConst.ScreenSize)
        self.gameSurface = pg.Surface(viewConst.GameSize)

        self.renderObjects = []
        self.vibration = False

        self.clock = pg.time.Clock()

        # if not pg.mixer.get_busy():
        #     self.backgroundMusic.play(-1)

        self.is_initialized = True

    def blit_at_center(self, target, source, position):
        center = tuple([int(pos - size // 2) for pos, size in zip(position, source.get_size())])
        target.blit(source, center)

    def render_menu(self):
        """
        Render the game menu.
        """
        if self.last_update != model.STATE_MENU:
            self.last_update = model.STATE_MENU
            self.title_counter = 0

        self.screen.fill(viewConst.Color_Black)

        title_loop_counter = self.title_counter % 80
        if not title_loop_counter:
            self.darken_time = [random.randint(25, 35), random.randint(55, 65)]
        
        if self.title_counter <= 10:
            gray = (155 + int(self.title_counter / 10 * 100),) * 3
        elif self.darken_time[0] <= title_loop_counter <= self.darken_time[0] + 5:
            gray = ((155 + (title_loop_counter - self.darken_time[0]) / 5 * 100),) * 3
        elif self.darken_time[1] <= title_loop_counter <= self.darken_time[1] + 5:
            gray = ((155 + (title_loop_counter - self.darken_time[1]) / 5 * 100),) * 3
        else:
            gray = (255,) * 3


        words_1 = self.titleFont.render(
                    'QUANTUM', 
                    True, gray)
        words_2 = self.titleFont.render(
                    'VORTEX',
                    True, gray)

        words_3 = self.titleSmallFont.render(
                    'presented by 2018 NTU CSIE CAMP',
                    True, (255, 255, 255))

        (size_x_1, size_y_1) = words_1.get_size()
        (size_x_2, size_y_2) = words_2.get_size()
        (size_x_3, size_y_3) = words_3.get_size()
        pos_x_1 = (viewConst.ScreenSize[0] - size_x_1)/2
        pos_y_1 = (viewConst.ScreenSize[1] - size_y_1 - viewConst.titleFontSize - size_y_3)/2
        pos_x_2 = (viewConst.ScreenSize[0] - size_x_2)/2
        pos_y_2 = (viewConst.ScreenSize[1] - size_y_2 + viewConst.titleFontSize - size_y_3)/2
        pos_x_3 = (viewConst.ScreenSize[0] - size_x_3)/2
        pos_y_3 = (650 + size_y_3)

        self.screen.blit(words_1, (pos_x_1, pos_y_1))
        self.screen.blit(words_2, (pos_x_2, pos_y_2))
        self.screen.blit(words_3, (pos_x_3, pos_y_3))

        self.title_counter += 1

        # update surface
        pg.display.flip()
        
    def render_stop(self):
        """
        Render the stop screen.
        """
        if self.last_update != model.STATE_STOP:
            self.last_update = model.STATE_STOP

            self.stopCounter = 0

            # detect the edges of the current screen
            tempStopSurface = pg.transform.laplacian(self.screen)
            # make it monochrome
            self.stopSurface = pg.Surface(self.screen.get_size())
            pg.transform.threshold(self.stopSurface, tempStopSurface, viewConst.Color_Black, (0, 0, 0, 0), viewConst.Color_White)

            # draw backgound
            # s = pg.Surface(viewConst.ScreenSize, pg.SRCALPHA)
            # s.fill((0, 0, 0, 128), (0, 0, *viewConst.GameSize)); self.screen.blit(s, (0,0))

        self.stopCounter += 1
        self.screen.fill(viewConst.Color_Black)
        if self.stopCounter % 3 == 0:
            gray = (min(50 + int(205 * min(1, self.stopCounter / 240)) + random.randint(-40, 40), 255), ) * 3
            self.stopSurface.set_alpha(127 - gray[0] // 2.2)
            self.screen.blit(self.stopSurface, (0, 0))
            words = self.titleFont.render('PAUSE', True, gray)
            pos = [x // 2 for x in viewConst.ScreenSize]
            self.blit_at_center(self.screen, words, pos)
            pg.display.flip()

    def drawScoreboard(self):
        # Frame
        gfxdraw.vline(self.renderSurface, viewConst.GameSize[0], 0,
                      viewConst.GameSize[1], viewConst.sbColor)

        for i in range(1, modelConst.PlayerNum):
            gfxdraw.hline(self.renderSurface, viewConst.GameSize[0],
                          viewConst.ScreenSize[0],
                          viewConst.GameSize[1] // modelConst.PlayerNum * i, viewConst.sbColor)
        # Team Names
        pos = [(viewConst.GameSize[0] + viewConst.GameSize[1] // modelConst.PlayerNum, viewConst.GameSize[1] // modelConst.PlayerNum * i + viewConst.GameSize[1] // (modelConst.PlayerNum * 8)) for i in range(modelConst.PlayerNum)]
        for i, player in enumerate(self.model.player_list):
            color = viewConst.aliveTeamColor if player.is_alive else viewConst.deadTeamColor
            teamName = self.teamNameFont.render(player.name, True, color)
            self.renderSurface.blit(teamName, pos[i])
        # Team Scores
        pos = [(x, y + viewConst.GameSize[1] // 32) for x, y in pos]
        for i, player in enumerate(self.model.player_list):
            color = viewConst.Color_Black
            teamScore = self.teamScoreFont.render(str(self.model.score_list[player.index]), True, color)
            self.renderSurface.blit(teamScore, pos[i])
        # Team Balls
        pos = [(viewConst.GameSize[0] + viewConst.GameSize[1] // (modelConst.PlayerNum * 2), viewConst.GameSize[1] // (modelConst.PlayerNum * 2) * i) for i in range(1, modelConst.PlayerNum * 2, 2)]
        radius = int(viewConst.GameSize[1] // (modelConst.PlayerNum * 2) * 0.7)
        for i, player in enumerate(self.model.player_list):
            if self.model.have_scoreboard[i]:
                ballPos = tuple([x + random.randint(-5, 5) for x in pos[i]]) if self.model.bombtimer[i] != -1 else pos[i]
                if self.model.bombtimer[i] == modelConst.bombtime - 1:
                    pass
                    # self.vibrationSound.play()
                gfxdraw.filled_circle(self.renderSurface, *ballPos, radius, player.color)
        # Team Player Lengths
        for i, player in enumerate(self.model.player_list):
            length = str(len(player.body_list)) if player.is_alive else '0'
            color = viewConst.teamLengthColor if self.model.have_scoreboard[i] else viewConst.Color_Black
            teamLength = self.teamLengthFont.render(length, True, color)
            self.blit_at_center(self.renderSurface, teamLength, pos[i])

    def drawGrav(self):
        color = (*self.model.player_list[self.model.grav_index].color, 32) if self.model.grav_index != -1 else viewConst.gravColor
        #print(color)
        for g in modelConst.grav:
            pos = tuple(map(int, g[0]))
            radius = int(g[1] + modelConst.head_radius * 0.5)
            #print(color)
            gfxdraw.filled_circle(self.gameSurface, *pos,
                                  radius, color)
            gfxdraw.filled_circle(self.gameSurface, *pos,
                                  int(radius * 0.07), viewConst.bgColor)
            # gfxdraw.filled_circle(self.screen, *pos,
            #                      radius, (85,107,47,111))

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
            gfxdraw.filled_circle(self.gameSurface, *pos,
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
            self.blit_at_center(self.gameSurface, itemSurface, pos)

    def drawBody(self):
        for player in self.model.player_list:
            for body in player.body_list[1:]:
                pos = tuple(map(int, body.pos))
                gfxdraw.filled_circle(self.gameSurface, *pos,
                                      int(body.radius), body.color)

    def drawHead(self):
        for player in self.model.player_list:
            if player.is_alive:
                pos = tuple(map(int, player.pos))
                color = player.color
                if player.is_dash:
                    color = tuple([int(i * 127 / 255 + 128) for i in color])
                gfxdraw.filled_circle(self.gameSurface, *pos,
                                      int(player.radius), color)
                # draw triangle
                triRadius = player.radius * 0.7
                theta = math.atan2(player.direction.y, player.direction.x)

                relativeVertexStart = pg.math.Vector2(triRadius, 0).rotate(theta * 180 / math.pi)
                relativeVertices = [relativeVertexStart.rotate(i * 120) for i in range(3)]

                vertices = [player.pos + vertex for vertex in relativeVertices]
                intVertices = [int(x) for vertex in vertices for x in vertex]
                gfxdraw.filled_trigon(self.gameSurface, *intVertices, viewConst.Color_Snow)

                if player.is_circling:
                    innerVertices = [player.pos + 0.6 * vertex for vertex in relativeVertices]
                    intInnerVertices = [int(x) for vertex in innerVertices for x in vertex]
                    gfxdraw.filled_trigon(self.gameSurface, *intInnerVertices, color)

    def drawBullet(self):
        for bullet in self.model.bullet_list:
            color = bullet.color
            if bullet.is_flash and (bullet.age // viewConst.bulletFlickerCycle) % 2 == 0:
                color = tuple([int(i * 127 / 255 + 128) for i in color])
            pos = tuple(map(int, bullet.pos))
            gfxdraw.filled_circle(self.gameSurface, *pos,
                                  int(bullet.radius), color)
            gfxdraw.filled_circle(self.renderSurface, *pos,
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
        self.blit_at_center(self.gameSurface, explosionEffect, pos)

    def drawTimeLimitExceedStamp(self, tle):
        pass

    def drawMagicCircle(self, magicCircle):
        scaleFactor = 0.3
        scaleFactor *= 1 - max(magicCircle.time / magicCircle.totaltime, 0)
        magicCircleEffect = pg.transform.rotozoom(self.magicCircleImage, magicCircle.theta, scaleFactor)
        self.blit_at_center(self.gameSurface, magicCircleEffect, magicCircle.pos)

    def drawCountDown(self, countdown):
        timeRatio = countdown.time / countdown.totaltime
        if timeRatio > 3/4:
            color = viewConst.Color_Firebrick
            figure = 3
        elif timeRatio > 2/4:
            color = viewConst.Color_Royalblue
            figure = 2
        elif timeRatio > 1/4:
            color = viewConst.Color_Darkolivegreen
            figure = 1
        elif timeRatio > 23/127:
            color = viewConst.Color_Orangered
            figure = "GO!"
        else:
            return
        countDownFigure = self.countDownFont.render(str(figure), True, color)
        self.blit_at_center(self.gameSurface, countDownFigure, countdown.pos)

    def drawMovingScore(self, movingscore):
        movingScoreSurface = pg.Surface((viewConst.GameSize[0] * 3 // 16 * 2, viewConst.GameSize[1] * 3 // 16))
        timeRatio = max(movingscore.time / movingscore.totaltime, 0)
        color = self.model.player_list[movingscore.index].color
        movingScoreSurface.fill(color)

        tmpScoreFigure = self.tmpScoreFont.render('+' + str(self.model.tmp_score_list[movingscore.index]), True, viewConst.Color_Snow)
        sizeSurface = movingScoreSurface.get_size()
        sizeFigure = tmpScoreFigure.get_size()
        center = (sizeSurface[0] - sizeFigure[0] * 2, (sizeSurface[1] - sizeFigure[1]) // 2)
        movingScoreSurface.blit(tmpScoreFigure, center)

        movingScoreSurface.fill(viewConst.Color_Gold, (sizeSurface[0] - 38, 0, 7, sizeSurface[1]))
        movingScoreSurface.fill(viewConst.Color_Gold, (sizeSurface[0] - 18, 0, 7, sizeSurface[1]))

        movingScoreSurface.set_alpha(int(255 * (1 - timeRatio)))
        pos = (movingscore.pos[0] + viewConst.GameSize[0] // 16 * (1 - timeRatio), movingscore.pos[1])
        self.blit_at_center(self.gameSurface, movingScoreSurface, pos)

    def drawSkillCardCutIn(self, cutin):

        # print(cutin.isdisplay)
        if not cutin.isdisplay:
            return

        # print('draw skill card')
        cutInSurface = pg.Surface((viewConst.GameSize[0], viewConst.GameSize[1] // 2), pg.SRCALPHA)
        cutInSurface.fill(viewConst.Color_Silver)
        sizeSurface = cutInSurface.get_size()
        
        if viewConst.skillCardCutInTime >= cutin.time >= viewConst.skillCardCutInTimesteps[3]:
            # draw phrase 1
            timeRatioSlow = min((viewConst.skillCardCutInTime - cutin.time) / viewConst.skillCardCutInTimePhrases[0], 1)
            timeRatioFast = min(1, timeRatioSlow + 0.20)
            pg.draw.rect(cutInSurface, viewConst.Color_Black, (0, 10, int(timeRatioSlow * sizeSurface[0]), 10), 0)
            pg.draw.rect(cutInSurface, viewConst.Color_Black, (0, sizeSurface[1]-20, int(timeRatioFast * sizeSurface[0]), 10), 0)
            
            # draw phrase 2
            timeRatioSlow = min((viewConst.skillCardCutInTimesteps[1] - cutin.time) / viewConst.skillCardCutInTimePhrases[1], 1)
            timeRatioFast = min(1, timeRatioSlow + 0.20)
            pg.draw.rect(cutInSurface, viewConst.Color_Black, (sizeSurface[0] - int(timeRatioSlow * sizeSurface[0]), 5, int(timeRatioSlow * sizeSurface[0]), 20), 0)
            pg.draw.rect(cutInSurface, viewConst.Color_Black, (sizeSurface[0] - int(timeRatioFast * sizeSurface[0]), sizeSurface[1]-25, int(timeRatioFast * sizeSurface[0]), 20), 0)
        else:
            # draw phrase 4 / 5 white lines
            pg.draw.rect(cutInSurface, viewConst.Color_White + (80, ), (0, 5, sizeSurface[0], 20), 0)
            pg.draw.rect(cutInSurface, viewConst.Color_White + (80, ), (0, sizeSurface[1]-25, sizeSurface[0], 20), 0)


        if viewConst.skillCardCutInTimesteps[2] >= cutin.time >= viewConst.skillCardCutInTimesteps[3]:
            # draw phrase 3
            timeRatio = 1 - ((viewConst.skillCardCutInTimesteps[2] - cutin.time) / viewConst.skillCardCutInTimePhrases[2])
            imgx, imgy = self.cutInImageSmall[cutin.index][1].get_size()
            cutInSurface.blit(self.cutInImageSmall[cutin.index][1],
                              (int(sizeSurface[0] * (8 / 32 + timeRatio / 2) - imgx // 2), viewConst.GameSize[1] // 2 - imgy - 25))
        
        elif viewConst.skillCardCutInTimesteps[3] >= cutin.time:
            # draw phrase 4
            if cutin.time >= viewConst.skillCardCutInTimesteps[4]:
                timeRatio = 1 - ((viewConst.skillCardCutInTimesteps[3] - cutin.time) / viewConst.skillCardCutInTimePhrases[3])
                cutInSurface.fill(viewConst.Color_White + (int(timeRatio * 255),), special_flags=pg.BLEND_RGBA_ADD)

            # draw phrase 5
            if cutin.time >= viewConst.skillCardCutInTimesteps[5]:
                timeRatio = ((viewConst.skillCardCutInTimesteps[3] - cutin.time) / (viewConst.skillCardCutInTimesteps[3] - viewConst.skillCardCutInTimesteps[5]))
                imgxs, imgys = self.cutInImageTransSmall[cutin.index].get_size()
                imgxl, imgyl = self.cutInImageTransLarge[cutin.index].get_size()
                cutInSurface.blit(self.cutInImageTransSmall[cutin.index],
                                  (int(sizeSurface[0] * (8 / 32 + timeRatio / 64) - imgxs // 2), viewConst.GameSize[1] // 2 - imgys - 25))            
                cutInSurface.blit(self.cutInImageTransLarge[cutin.index],
                                  (int(sizeSurface[0] * (21 / 32 - timeRatio / 32) - imgxl // 2), viewConst.GameSize[1] // 2 - imgyl - 25))

            elif viewConst.skillCardCutInTimesteps[5] >= cutin.time:
                timeRatio = ((viewConst.skillCardCutInTimesteps[5] - cutin.time) / viewConst.skillCardCutInTimePhrases[5])
                imgxs, imgys = self.cutInImageTransSmall[cutin.index].get_size()
                imgxl, imgyl = self.cutInImageTransLarge[cutin.index].get_size()
                cutInSurface.blit(self.cutInImageTransSmall[cutin.index],
                                  (int(sizeSurface[0] * (17 / 64 + timeRatio * 4) - imgxs // 2), viewConst.GameSize[1] // 2 - imgys - 25))            
                cutInSurface.blit(self.cutInImageTransLarge[cutin.index],
                                  (int(sizeSurface[0] * (20 / 32 - timeRatio * 4) - imgxl // 2), viewConst.GameSize[1] // 2 - imgyl - 25))

        self.blit_at_center(self.gameSurface, cutInSurface, cutin.pos)

    def drawThermometer(self, thermometer):
        # draw the bar
            lengthFactor = 1 - max(thermometer.time / thermometer.totaltime, 0)
            length = 600 * thermometer.value / 15 * lengthFactor
            pos = (thermometer.pos[0] - viewConst.thermometerBarWidth // 2, int(thermometer.pos[1] - length))
            self.gameSurface.fill(thermometer.color, (pos[0], pos[1] - viewConst.thermometerBallSize, viewConst.thermometerBarWidth, int(length)))

        # draw the base (ball)
            gfxdraw.filled_circle(self.gameSurface, *thermometer.pos,
                                  int(viewConst.thermometerBallSize * 1.05), viewConst.bgColor)
            gfxdraw.filled_circle(self.gameSurface, *thermometer.pos,
                                  viewConst.thermometerBallSize, thermometer.color)
        # draw the score
            color = viewConst.Color_Snow
            teamScore = self.teamScoreFont.render(str(thermometer.value), True, color)
            self.blit_at_center(self.gameSurface, teamScore, thermometer.pos)

    def drawIridescence(self, iridescence):
        timeRatio = iridescence.time / iridescence.totaltime
        if not iridescence.reverse:
            timeRatio = 1 - timeRatio
        self.rainbowImage.set_alpha(int(255 * timeRatio))
        self.gameSurface.blit(self.rainbowImage, (0, 0))

    def drawUndulation(self, undulation):
        timeRatio = undulation.time / undulation.totaltime
        if not undulation.reverse:
            timeRatio = 1 - timeRatio
        timeRatio *= 2 * math.pi * undulation.frequency

        tempGameSurface = pg.Surface(viewConst.GameSize)
        tempGameSurface.fill(viewConst.bgColor)
        xblocks = range(0, 800, 40)
        yblocks = range(0, 800, 40)
        for x in xblocks:
            xpos = x + undulation.amplitude * math.sin(timeRatio) * math.sin(x / 760 * undulation.quantumNumber * 2 * math.pi)
            for y in yblocks:
                ypos = y + undulation.amplitude * math.sin(timeRatio) * math.sin(y / 760 * undulation.quantumNumber * 2 * math.pi)
                tempGameSurface.blit(self.gameSurface, (x, y), (xpos, ypos, 40, 40))
        self.gameSurface = tempGameSurface

    def drawNyancat(self, nyancat):
        timeRatio = 1 - nyancat.time / nyancat.totaltime
        pos = (int(2400 * timeRatio) - 400 + nyancat.pos[0], nyancat.pos[1])
        self.blit_at_center(self.gameSurface, self.nyanCatImage, pos)
        for i in range(3):
            if pos[0] <= 0:
                break
            pos = (pos[0] - self.nyanCatTailImage.get_size()[0], pos[1])
            self.blit_at_center(self.gameSurface, self.nyanCatTailImage, pos)

    def drawRainbow(self, rainbow):
        if not rainbow.isdisplay:
            return
        time = rainbow.totaltime - rainbow.time
        # phase 0
        if time == 120:
            ypos = random.sample([i for i in range(100, 700 + 1, 100)], 5)
            # self.meowSound.play()
            # self.rainbowSound.play()
            for i in range(5):
                pos = (random.randint(-400, 0), ypos[i])
                self.renderObjects.append(renderObject.Nyancat(pos, 180))
        # phase 1
        if time == 120 + 90:
            self.renderObjects.append(renderObject.Iridescence((0, 0), 240))
            self.renderObjects.append(renderObject.Undulation((0, 0), 240, 20, 1, 1))
        # phase 2
        if time == 120 + 90 + 230:
            self.renderObjects.append(renderObject.Iridescence((0, 0), 60, True))
            self.renderObjects.append(renderObject.Undulation((0, 0), 60, 20, 0.25, 1, True))

    def drawHyperdimensionalExplosion(self, hyperdimensionalExplosion):
        if not hyperdimensionalExplosion.isdisplay:
            return
        time = hyperdimensionalExplosion.totaltime - hyperdimensionalExplosion.time
        radius = min((time - 120) / 240 * 800 * 1.45, 800 * 1.45)
        pos = tuple(map(int, hyperdimensionalExplosion.pos))
        color = (*self.model.player_list[hyperdimensionalExplosion.index].color, 48)
        def waveFunc(p, r):
            r1 = pg.math.Vector2(pos)
            r2 = pg.math.Vector2(p)
            r3 = r2 - r1
            # if r3.length() < r and r > 0:
            #     r3 *= math.sin(r3.length() / r * math.pi / 2)
            #     newPos = r1 + r3
            #     return tuple(map(int, newPos))
            if 0 < r - r3.length() < 80 and r3.length() > 0:
                r4 = r3
                r4.scale_to_length(r)
                r3 += 0.9 * (r4 - r3) * math.sin((r - r3.length()) / 80 * math.pi / 2)
                newPos = r1 + r3
                return tuple(map(int, newPos))
            else:
                return p
        # phase 1
        if 120 <= time <= 120 + 240:
            self.vibration = True
            gfxdraw.filled_circle(self.gameSurface, *pos, int(radius), color)

            tempGameSurface = pg.Surface(viewConst.GameSize)
            tempGameSurface.fill(viewConst.bgColor)
            xblocks = range(0, 800, 10)
            yblocks = range(0, 800, 10)
            for x in xblocks:
                for y in yblocks:
                    pos2 = waveFunc((x, y), radius + 15)
                    tempGameSurface.blit(self.gameSurface, (x, y), (*pos2, 10, 10))
            self.gameSurface = tempGameSurface
        # phase 2
        elif 120 + 240 <= time <= 120 + 240 + 30:
            self.vibration = False
            gfxdraw.filled_circle(self.gameSurface, *pos, int(radius), color)
        # phase 3
        elif 120 + 240 + 30 <= time:
            color = (color[0], color[1], color[2], int(color[3] * (1 - (time - 120 - 240 - 30) / 60)))
            gfxdraw.filled_circle(self.gameSurface, *pos, int(radius), color)

    def drawRenderObject(self):

        renderOrder = ['Explosion',
                       'TimeLimitExceedStamp',
                       'MagicCircle',
                       'CountDown',
                       'MovingScore',
                       'Thermometer',
                       'Iridescence',
                       'Undulation',
                       'Nyancat',
                       'Rainbow',
                       'HyperdimensionalExplosion',
                       'SkillCardCutIn']
        renderOrderMap = {name : i for i, name in enumerate(renderOrder)}
        sortedRenderObjects = [[] for i in range(len(renderOrder))]
        for x in self.renderObjects:
            sortedRenderObjects[renderOrderMap[type(x).__name__]].append(x)
        for i, renderObjects in enumerate(sortedRenderObjects):
            drawMethod = getattr(self, 'draw' + renderOrder[i])
            for instance in renderObjects:

                drawMethod(instance)
                instance.update()

                if isinstance(instance, renderObject.SkillCardCutIn) and (instance.skill not in [6, 7] or not self.has_cutin) and instance.time <= 0:
                    self.evManager.Post(Event_Skill(instance.index, instance.skill))
                elif isinstance(instance, renderObject.Rainbow) and instance.totaltime - instance.time == 120 + 320:
                    self.evManager.Post(Event_Skill(instance.index, 6))
                elif isinstance(instance, renderObject.HyperdimensionalExplosion) and instance.totaltime - instance.time == 120 + 240 + 30:
                    self.evManager.Post(Event_Skill(instance.index, 7))

        self.renderObjects[:] = [x for x in self.renderObjects if x.immortal or x.time > 0]

    def render_play(self):
        """
        Render the game play.
        """
        if self.last_update != model.STATE_PLAY and self.last_update != model.STATE_STOP:
            self.renderObjects[:] = []
            pos = tuple([x // 2 for x in viewConst.GameSize])
            self.renderObjects.append(renderObject.CountDown(pos, 240))
        self.last_update = model.STATE_PLAY

        self.screen.fill(viewConst.Color_Black)
        self.renderSurface.fill(viewConst.bgColor)
        self.gameSurface.fill(viewConst.bgColor)

        self.drawScoreboard()
        self.drawGrav()
        self.drawWhiteBall()
        self.drawItem()
        self.drawBody()
        self.drawHead()
        self.drawBullet()
        self.drawRenderObject()

        if self.vibration:
            shift = tuple([random.randint(-10, 10) for i in [127, 127]])
            self.renderSurface.blit(self.gameSurface, shift)
        else:
            self.renderSurface.blit(self.gameSurface, (0, 0))
        self.screen.blit(self.renderSurface, (0, 0))

        pg.display.flip()

    def render_endgame(self):
        if self.last_update != model.STATE_ENDGAME:
            self.last_update = model.STATE_ENDGAME
            self.renderObjects[:] = []
            movingScores = [renderObject.MovingScore(i, (viewConst.GameSize[0] // 8, viewConst.GameSize[1] // 8 * (2 * i + 1)), viewConst.scoreFlagEmergeTime) for i in range(modelConst.PlayerNum)]
            self.renderObjects.extend(movingScores)

        self.screen.fill(viewConst.Color_Black)
        self.renderSurface.fill(viewConst.bgColor)
        self.gameSurface.fill(viewConst.bgColor)

        self.drawScoreboard()
        self.drawRenderObject()

        self.renderSurface.blit(self.gameSurface, (0, 0))
        self.screen.blit(self.renderSurface, (0, 0))
        pg.display.flip()

    def render_endmatch(self):
        if self.last_update != model.STATE_ENDMATCH:
            self.last_update = model.STATE_ENDMATCH
            self.renderObjects[:] = []
            scores = []
            for i in range(modelConst.PlayerNum):
                scores.append((i, self.model.score_list[i]))
            scores.sort(key=lambda x:x[1], reverse=True)
            thermometers = [renderObject.Thermometer(score[0], (viewConst.GameSize[0] // 8 * (2 * i + 1), viewConst.GameSize[1] // 8 * 7), viewConst.thermometerEmergeTime, self.model.player_list[score[0]].color, score[1]) for i, score in enumerate(scores)]
            self.renderObjects.extend(thermometers)

        self.screen.fill(viewConst.Color_Black)
        self.renderSurface.fill(viewConst.bgColor)
        self.gameSurface.fill(viewConst.bgColor)

        self.drawScoreboard()
        self.drawRenderObject()

        self.renderSurface.blit(self.gameSurface, (0, 0))
        self.screen.blit(self.renderSurface, (0, 0))
        pg.display.flip()
