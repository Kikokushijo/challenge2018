import pygame as pg
import pygame.gfxdraw as gfxdraw
import math

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
        self.tmpScoreFont = None

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
            self.renderObjects.append(renderObject.Explosion(event.PlayerIndex, event.pos, modelConst.explosive_radius, viewConst.explosionTime))
        elif isinstance(event, Event_PlayerKilled):
            self.renderObjects.append(renderObject.Explosion(event.PlayerIndex, event.pos, viewConst.killedExplosionRadius, viewConst.killedExplosionTime))
        elif isinstance(event, Event_TimeLimitExceed):
            pos = ((viewConst.ScreenSize[0] + viewConst.GameSize[0]) // 2, viewConst.GameSize[1] // 8 * (2 * event.PlayerIndex + 1))
            self.renderObjects.append(renderObject.TimeLimitExceedStamp(pos, viewConst.timeLimitExceedStampTime))
        elif isinstance(event, Event_SuddenDeath):
            pos = tuple([x // 2 for x in viewConst.GameSize])
            self.renderObjects.append(renderObject.MagicCircle(pos, viewConst.magicCircleGenerationTime))
        elif isinstance(event, Event_SkillCutIn):
            print(event)
            pos = tuple([x // 2 for x in viewConst.GameSize])
            self.renderObjects.append(renderObject.SkillCardCutIn(event.PlayerIndex, pos, viewConst.skillCardCutInTime, event.number))
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
        pg.init();
        pg.display.set_caption(viewConst.GameCaption)
        self.screen = pg.display.set_mode(viewConst.ScreenSize)
        self.clock = pg.time.Clock()
        self.smallfont = pg.font.Font(None, 40)
        self.teamNameFont = pg.font.Font(viewConst.teamNameFont, viewConst.teamNameFontSize)
        self.teamLengthFont = pg.font.Font(viewConst.teamLengthFont, viewConst.teamLengthFontSize)
        self.teamScoreFont = pg.font.Font(viewConst.teamScoreFont, viewConst.teamScoreFontSize)
        self.countDownFont = pg.font.Font(viewConst.countDownFont, viewConst.countDownFontSize)
        self.tmpScoreFont = pg.font.Font(viewConst.tmpScoreFont, viewConst.tmpScoreFontSize)

        self.renderObjects = []

        self.magicCircleImage = pg.image.load('View/Image/magicCircle.png').convert_alpha()
        self.cutInImage       = [(pg.image.load('View/Image/Darkviolet.png').convert_alpha(),
                                  pg.image.load('View/Image/Darkviolet_bw.png').convert_alpha()),
                                 (pg.image.load('View/Image/Royalblue.png').convert_alpha(),
                                  pg.image.load('View/Image/Royalblue_bw.png').convert_alpha()),
                                 (pg.image.load('View/Image/Saddlebrown.png').convert_alpha(),
                                  pg.image.load('View/Image/Saddlebrown_bw.png').convert_alpha())]
        self.cutInImageSmall = [tuple([pg.transform.scale(img1, viewConst.skillCardCutInPicSmallSize),
                                       pg.transform.scale(img2, viewConst.skillCardCutInPicSmallSize)])
                                      for img1, img2 in self.cutInImage]
        self.cutInImageTrans1      = [pg.image.load('View/Image/Darkviolet_trans1.png').convert_alpha(),
                                      pg.image.load('View/Image/Royalblue_trans1.png').convert_alpha(), 
                                      pg.image.load('View/Image/Saddlebrown_trans1.png').convert_alpha()]
        self.cutInImageTransSmall  = [pg.transform.scale(img, viewConst.skillCardCutInPicSmallSize)
                                      for img in self.cutInImageTrans1]

        self.cutInImageTrans2      = [pg.image.load('View/Image/Darkviolet_trans2.png').convert_alpha(),
                                      pg.image.load('View/Image/Royalblue_trans2.png').convert_alpha(),
                                      pg.image.load('View/Image/Saddlebrown_trans2.png').convert_alpha()]
        self.cutInImageTransLarge = [pg.transform.scale(img, viewConst.skillCardCutInPicLargeSize)
                                      for img in self.cutInImageTrans2]

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
            s.fill((0, 0, 0, 128), (0, 0, *viewConst.GameSize)); self.screen.blit(s, (0,0))

            # update surface
            pg.display.flip()

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
            teamName = self.teamNameFont.render(player.name, True, color)
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
            if self.model.have_scoreboard[i]:
                gfxdraw.filled_circle(self.screen, *(pos[i]), radius, player.color)
        # Team Player Lengths
        for i, player in enumerate(self.model.player_list):
            length = str(len(player.body_list)) if player.is_alive else '0'
            color = viewConst.teamLengthColor if self.model.have_scoreboard[i] else viewConst.Color_Black
            teamLength = self.teamLengthFont.render(length, True, color)
            self.blit_at_center(teamLength, pos[i])

    def drawGrav(self):
        color = (*self.model.player_list[self.model.grav_index].color, 32) if self.model.grav_index != -1 else viewConst.gravColor
        for g in modelConst.grav:
            pos = tuple(map(int, g[0]))
            radius = int(g[1] + modelConst.head_radius * 0.5)
            gfxdraw.filled_circle(self.screen, *pos,
                                  radius, color)
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
                                      int(body.radius), body.color)

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
            if bullet.is_flash and (bullet.age // viewConst.bulletFlickerCycle) % 2 == 0:
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
        self.blit_at_center(movingScoreSurface, pos)

    def drawSkillCardCutIn(self, cutin):
        print('draw skill card')
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
            cutInSurface.blit(self.cutInImageSmall[cutin.index][1],
                              (int(sizeSurface[0] * (3 / 32 + timeRatio / 2)), viewConst.GameSize[1] // 2 - viewConst.skillCardCutInPicSmallSize[1] - 25))
        
        elif viewConst.skillCardCutInTimesteps[3] >= cutin.time:
            # draw phrase 4
            if cutin.time >= viewConst.skillCardCutInTimesteps[4]:
                timeRatio = 1 - ((viewConst.skillCardCutInTimesteps[3] - cutin.time) / viewConst.skillCardCutInTimePhrases[3])
                cutInSurface.fill(viewConst.Color_White + (int(timeRatio * 255),))

            # draw phrase 5
            if cutin.time >= viewConst.skillCardCutInTimesteps[5]:
                timeRatio = ((viewConst.skillCardCutInTimesteps[3] - cutin.time) / (viewConst.skillCardCutInTimesteps[3] - viewConst.skillCardCutInTimesteps[5]))
                cutInSurface.blit(self.cutInImageTransSmall[cutin.index],
                                  (int(sizeSurface[0] * (3 / 32 + timeRatio / 64)), viewConst.GameSize[1] // 2 - viewConst.skillCardCutInPicSmallSize[1] - 25))            
                cutInSurface.blit(self.cutInImageTransLarge[cutin.index],
                                  (int(sizeSurface[0] * (16 / 32 - timeRatio / 32)), viewConst.GameSize[1] // 2 - viewConst.skillCardCutInPicLargeSize[1] - 25))

            elif viewConst.skillCardCutInTimesteps[5] >= cutin.time:
                timeRatio = ((viewConst.skillCardCutInTimesteps[5] - cutin.time) / viewConst.skillCardCutInTimePhrases[5])
                cutInSurface.blit(self.cutInImageTransSmall[cutin.index],
                                  (int(sizeSurface[0] * (7 / 64 + timeRatio * 4)), viewConst.GameSize[1] // 2 - viewConst.skillCardCutInPicSmallSize[1] - 25))            
                cutInSurface.blit(self.cutInImageTransLarge[cutin.index],
                                  (int(sizeSurface[0] * (15 / 32 - timeRatio * 4)), viewConst.GameSize[1] // 2 - viewConst.skillCardCutInPicLargeSize[1] - 25))


            # draw phrase 6
            # timeRatio = 


        self.blit_at_center(cutInSurface, cutin.pos)

    def drawThermometer(self, thermometer):
        # draw the bar
            lengthFactor = 1 - max(thermometer.time / thermometer.totaltime, 0)
            length = 600 * thermometer.value / 15 * lengthFactor
            pos = (thermometer.pos[0] - viewConst.thermometerBarWidth // 2, int(thermometer.pos[1] - length))
            self.screen.fill(thermometer.color, (pos[0], pos[1] - viewConst.thermometerBallSize, viewConst.thermometerBarWidth, int(length)))

        # draw the base (ball)
            gfxdraw.filled_circle(self.screen, *thermometer.pos,
                                  int(viewConst.thermometerBallSize * 1.05), viewConst.bgColor)
            gfxdraw.filled_circle(self.screen, *thermometer.pos,
                                  viewConst.thermometerBallSize, thermometer.color)
        # draw the score
            color = viewConst.Color_Snow
            teamScore = self.teamScoreFont.render(str(thermometer.value), True, color)
            self.blit_at_center(teamScore, thermometer.pos)

    def drawRenderObject(self):
        for instance in self.renderObjects:
            if isinstance(instance, renderObject.Explosion):
                self.drawExplosion(instance)
            elif isinstance(instance, renderObject.TimeLimitExceedStamp):
                self.drawTimeLimitExceedStamp(instance)
            elif isinstance(instance, renderObject.MagicCircle):
                self.drawMagicCircle(instance)
            elif isinstance(instance, renderObject.CountDown):
                self.drawCountDown(instance)
            elif isinstance(instance, renderObject.MovingScore):
                self.drawMovingScore(instance)
            elif isinstance(instance, renderObject.SkillCardCutIn):
                self.drawSkillCardCutIn(instance)
            elif isinstance(instance, renderObject.Thermometer):
                self.drawThermometer(instance)
            instance.update()

            if isinstance(instance, renderObject.SkillCardCutIn) and instance.time == 0:
                self.evManager.Post(Event_Skill(instance.index, instance.skill))

        self.renderObjects[:] = [x for x in self.renderObjects if x.immortal or x.time > 0]

    def render_play(self):
        """
        Render the game play.
        """
        if self.last_update != model.STATE_PLAY and self.last_update != model.STATE_STOP:
            self.renderObjects[:] = []
            pos = tuple([x // 2 for x in viewConst.GameSize])
            self.renderObjects.append(renderObject.CountDown(pos, 180))
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

    def render_endgame(self):
        if self.last_update != model.STATE_ENDGAME:
            self.last_update = model.STATE_ENDGAME
            self.renderObjects[:] = []
            movingScores = [renderObject.MovingScore(i, (viewConst.GameSize[0] // 8, viewConst.GameSize[1] // 8 * (2 * i + 1)), viewConst.scoreFlagEmergeTime) for i in range(modelConst.PlayerNum)]
            self.renderObjects.extend(movingScores)

        self.screen.fill(viewConst.bgColor, pg.Rect((0, 0), viewConst.GameSize))
        self.drawRenderObject()
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

        self.screen.fill(viewConst.bgColor, pg.Rect((0, 0), viewConst.GameSize))
        self.drawRenderObject()
        pg.display.flip()
