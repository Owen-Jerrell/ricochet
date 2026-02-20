import random
import pygame
import sys
import math
import time
pygame.font.init()
#from scripts.entities import PhysicsEntity
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Ricochet")
        self.screen = pygame.display.set_mode((1280,720))
        self.clock = pygame.time.Clock()
        self.movement = [False, False]
        self.font = pygame.font.Font("DogicaPixel.ttf", 40)
        self.playfontBG = pygame.font.Font("DogicaPixel.ttf", 43)
        self.fontSmall = pygame.font.Font("DogicaPixel.ttf", 20)
        self.fontBG = pygame.font.Font("DogicaPixel.ttf", 41)
        self.fontSmallBG = pygame.font.Font("DogicaPixel.ttf", 21)
        self.fontQuit = pygame.font.Font("DogicaPixel.ttf", 30)
        self.noPowerTimer = True
        self.powerUp = pygame.image.load('speedDown.png')
        self.x = 0
        self.y = 0
        self.render = False
        self.timeCount = 0
        
    def spawnPowerUp(self):
        self.x = int(random.random() * 480) + 400
        self.y = int(random.random() * 480) + 30
        self.render = True
        self.timeCount += 1
        
    def runMenu(self):
        while True:
            self.screen.fill((195, 177, 225))
            playBgSize = self.playfontBG.size("Play")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and 640 - playBgSize[0] / 2 < pygame.mouse.get_pos()[0] < 640 + playBgSize[0] / 2 and 360 - playBgSize[1] / 2 < pygame.mouse.get_pos()[1] < 360 + playBgSize[1] / 2:
                    self.run()
                if event.type == pygame.MOUSEBUTTONDOWN and 640 - self.fontQuit.size("Quit")[0] / 2 < pygame.mouse.get_pos()[0] < 640 + self.fontQuit.size("Quit")[0] / 2 and 470 < pygame.mouse.get_pos()[1] < 470 + self.fontQuit.size("Quit")[1]:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0:
                        pygame.display.toggle_fullscreen()
            playBg = self.playfontBG.render("Play", True, (255,255,255))
            self.screen.blit(playBg, (640 - int(playBgSize[0] / 2), 360 - int(playBgSize[1] / 2)))
            play = self.font.render("Play", True, (0,0,0))
            playSize = self.font.size("Play")
            self.screen.blit(play, (640 - (playSize[0] / 2), 360 - (playSize[1] / 2)))
            quitText = self.fontQuit.render("Quit", True, (0,0,0))
            self.screen.blit(quitText, (640 - self.fontQuit.size("Quit")[0] / 2, 470))
            fullscreen = self.fontSmall.render("Press 0 to toggle fullscreen", True, (0,0,0))
            self.screen.blit(fullscreen, (5, 695))
            logo = pygame.image.load('ricochet.png')
            self.screen.blit(logo, (640 - logo.get_width() / 2, -10))
            pygame.display.update()
            self.clock.tick(60)
    def run(self):
        while True:
            self.screen.fill((195, 177, 225))
            doBreak = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0:
                        pygame.display.toggle_fullscreen()
                    else:
                        doBreak = True
            if doBreak:
                break
            pressBg = self.fontBG.render("Press a key to start", True, (255,255,255))
            pressSizeBg = self.fontBG.size("Press a key to start")
            self.screen.blit(pressBg, (640 - int(pressSizeBg[0] / 2), 260 - int(pressSizeBg[1] / 2)))
            press = self.font.render("Press a key to start", True, (0,0,0))
            pressSize = self.font.size("Press a key to start")
            self.screen.blit(press, (640 - int(pressSize[0] / 2), 260 - int(pressSize[1] / 2)))
            akey = pygame.image.load('a.png')
            self.screen.blit(akey, (740 - int(pressSizeBg[0] / 2), 460))
            ccw = pygame.image.load('ccw.png')
            self.screen.blit(ccw, (730 - int(pressSizeBg[0] / 2), 332))
            dkey = pygame.image.load('d.png')
            self.screen.blit(dkey, (440 + int(pressSizeBg[0] / 2), 460))
            cw = pygame.image.load('cw.png')
            self.screen.blit(cw, (430 + int(pressSizeBg[0] / 2), 332))
            pygame.display.update()
            self.clock.tick(60)
        ballPos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
        angle = 0
        dimensionDiff = (self.screen.get_width() - self.screen.get_height()) / 2
        playArea = pygame.Rect(dimensionDiff + 20, 20, self.screen.get_height() - 40, self.screen.get_height() - 40)
        a_press = False
        d_press = False
        collision = False
        arcSize = math.pi / 7
        radius = 340
        #powerUpSpawn = pygame.Rect(650 - (math.sin(math.pi / 4) * 170), 370 - (math.sin(math.pi / 4) * 170), math.sin(math.pi / 4) * 340 - 20, math.sin(math.pi / 4) * 340 - 20)
        center = pygame.Vector2(640, 360)
        ballVelAngle = random.random() * 2 * math.pi
        #print(f"{ballVelAngle}")
        ballVelMag = 1.5
        stage = 1
        bounceCount = 0
        powerCount = 0
        powerTimer = pygame.time.get_ticks() + 30000
        self.timeCount = 0
        #print(self.font.size("Stage 1"))
        while True:
            currentTime = pygame.time.get_ticks()
            if currentTime >= powerTimer:
                self.spawnPowerUp()
                powerTimer = pygame.time.get_ticks() + 30000
            self.screen.fill((195, 177, 225))
            if a_press:
                angle += math.pi / 48
            if d_press:
                angle -= math.pi / 48
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a or a_press:
                        angle += math.pi / 48
                        a_press = True
                    if event.key == pygame.K_d or d_press:
                        angle -= math.pi / 48
                        d_press = True
                    if event.key == pygame.K_0:
                        pygame.display.toggle_fullscreen()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        a_press = False
                    if event.key == pygame.K_d:
                        d_press = False
            angle %= 2 * math.pi
            prevBallPos = ballPos.copy()
            ballPos[0] += ballVelMag * math.cos(ballVelAngle)
            ballPos[1] -= ballVelMag * math.sin(ballVelAngle)
            prevDist = prevBallPos.distance_to(center)
            currDist = ballPos.distance_to(center)
            ringThickness = 12
            ballRadius = 10

            inner = radius - ringThickness - ballRadius
            outer = radius + ringThickness + ballRadius

            crossedRing = ((prevDist > outer and currDist <= outer) or (prevDist < inner and currDist >= inner))
            ball_angle = math.atan2(center.y - ballPos.y, ballPos.x - center.x) % (2*math.pi)

            start = angle % (2*math.pi)
            end = (angle + arcSize) % (2*math.pi)

            if start < end:
                insideArc = start <= ball_angle <= end
            else:
                insideArc = ball_angle >= start or ball_angle <= end
            if crossedRing and insideArc and not collision:
                offset = ballPos - center
                if offset.length_squared() != 0:
                    normal = offset.normalize()
                else:
                    normal = pygame.Vector2(1, 0)
                velocity = pygame.Vector2(math.cos(ballVelAngle), -math.sin(ballVelAngle))
                velocity.reflect_ip(normal)
                ballVelAngle = math.atan2(-velocity.y, velocity.x)
                ballVelAngle %= 2*math.pi
                variance = random.uniform(-math.pi/8, math.pi/8)
                ballVelAngle += variance
                if prevDist > radius:
                    ballPos = center + normal * outer
                else:
                    ballPos = center + normal * inner
                collision = True
                ballVelMag *= 1.05
                bounceCount += 1
                if bounceCount % 5 == 0 and stage <= 5:
                    stage += 1
                    ballVelMag *= 1.05
                elif bounceCount % 10 == 0 and stage <= 10:
                    stage += 1
                    ballVelMag *= 1.05
                elif bounceCount % 20 == 0:
                    stage += 1
                    ballVelMag *= 1.05
            else:
                collision = False
            pygame.draw.circle(self.screen, (255,255,255), ballPos, 10)
            pygame.draw.arc(self.screen, (255,255,255), playArea, angle, angle + (math.pi / 7), 10)
            #sampleText = self.font.render("Test", True, (0,0,0))
            #self.screen.blit(sampleText, (100,100))
            if self.render:
                self.screen.blit(self.powerUp, (self.x - 32, self.y - 32))
            if self.render and ballPos.distance_to((self.x, self.y)) < 42:
                self.render = False
                ballVelMag *= 0.8
                powerCount += 1

            if 980 < ballPos[0] or ballPos[0] < 300 or ballPos[1] < 20 or ballPos[1] > 700:
                self.screen.fill((205,0,0))
                self.render = False
                pygame.display.update()
                time.sleep(0.5)
                gameOver = self.font.render("Game Over", True, (0,0,0))
                self.screen.blit(gameOver,(477,40))
                #print(self.font.size("Game Over"))
                gameOver2 = self.fontSmall.render("Press any key to restart", True, (0,0,0))
                self.screen.blit(gameOver2,(442,95))
                barLength = self.fontSmall.size("Press any key to restart")[0]
                bar = pygame.Rect(640 - barLength / 2, 125, barLength, 10)
                pygame.draw.rect(self.screen, (0,0,0), bar)
                finalStage = self.fontSmall.render("Stage: " + str(stage) + " x 1000", True, (0,0,0))
                self.screen.blit(finalStage, (640 - barLength / 2, 140))
                bounces = self.fontSmall.render("Ricochets: " + str(bounceCount) + " x 10", True, (0,0,0))
                self.screen.blit(bounces, (640 - barLength / 2, 165))
                powers = self.fontSmall.render("Power ups activated: " + str(powerCount) + " x 100", True, (0,0,0))
                self.screen.blit(powers, (640 - barLength / 2, 190))
                timeMins = int(self.timeCount / 2)
                timeLasted = self.fontSmall.render("Time Lasted (min): " + str(timeMins) + " x 100", True, (0,0,0))
                self.screen.blit(timeLasted, (640 - barLength / 2, 215))
                score = stage * 1000 + bounceCount * 10 + powerCount * 100 + timeMins * 100
                scorePrint = self.font.render("Score: " + str(score), True, (0,0,0))
                self.screen.blit(scorePrint, (640 - barLength / 2, 300))
                home = self.fontSmall.render("Press esc to go to the home menu", True, (0,0,0))
                homeLength = self.fontSmall.size("Press esc to go to the home menu")[0]
                self.screen.blit(home, (640 - homeLength / 2, 690))
                pygame.display.update()
                doBreak = False
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_0:
                                pygame.display.toggle_fullscreen()
                            elif event.key == pygame.K_ESCAPE:
                                self.runMenu()
                            else:
                                doBreak = True   
                    if doBreak:
                        break
                self.run()
            stageCountBG = self.fontBG.render("Stage " + str(stage), True, (255,255,255))
            self.screen.blit(stageCountBG, (17,660))
            #print(self.fontBG.size("Stage " + str(stage)))
            stageCount = self.font.render("Stage " + str(stage), True, (0,0,0))
            self.screen.blit(stageCount, (20, 660))
            pygame.display.update()
            self.clock.tick(60)
    
Game().runMenu()