import pygame
import utils
import globals
import engine

#####################################################################

class Scene:
    def __init__(self):
        pass

    def onEnter(self):
        pass

    def onExit(self):
        pass

    def input(self, sm):
        pass

    def update(self, sm):
        pass

    def draw(self, sm, screen):
        pass

#####################################################################

class MainMenuScene(Scene):

    def input(self, sm): #sm = SceneManager
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            sm.push(FadeTransitionScene([self], [LevelSelectScene()]))
        if keys[pygame.K_z]:
            sm.pop()

    def draw(self, sm, screen):
        screen.fill(globals.DARK_GRAY)
        utils.drawText(screen, 'Main Menu. [Return = Levels, Z=quit]', 50, 50, globals.WHITE, 255)

#####################################################################

class LevelSelectScene(Scene):

    def input(self, sm):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            globals.world = globals.levels[1]
            #set level to 1
            sm.push(FadeTransitionScene([self], [GameScene()]))
        if keys[pygame.K_2]:
            #set level to 2
            globals.world = globals.levels[2]
            sm.push(FadeTransitionScene([self], [GameScene()]))
        if keys[pygame.K_ESCAPE]:
            sm.pop()
            sm.push(FadeTransitionScene([self], []))


    def update(self, sm):
        pass

    def draw(self, sm, screen):
        screen.fill(globals.DARK_GRAY)
        utils.drawText(screen, 'Level Select [1/2 = Level, esc=quit]', 50, 50, globals.WHITE, 255)

#####################################################################

class GameScene(Scene):

    def __init__(self):
        self.cameraSystem = engine.CameraSystem()

    def input(self, sm):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            sm.pop()
            sm.push(FadeTransitionScene([self], []))
        if globals.world.isWon():
            sm.push(WinScene())
        if globals.world.isLost():
            sm.push(LoseScene())

    def update(self, sm):
        pass



    def draw(self, sm, screen):
        screen.fill(globals.DARK_GRAY)
        self.cameraSystem.update(screen)

#####################################################################

class WinScene(Scene):

    def __init__(self):
        self.alpha = 0

    def update(self, sm):
        self.alpha = min(255, self.alpha + 1)

    def input(self, sm):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_x]:
            sm.set([FadeTransitionScene([GameScene(), self], [MainMenuScene(), LevelSelectScene()])])

    def draw(self, sm, screen):
        if len(sm.scenes) > 1:
            sm.scenes[-2].draw(sm, screen)

        bgSurf = pygame.Surface((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
        bgSurf.fill((globals.BLACK))
        utils.blit_alpha(screen, bgSurf, (0, 0), self.alpha * 0.7)

        utils.drawText(screen, 'You win! press x', 50, 50, globals.WHITE, self.alpha)


class LoseScene(Scene):

    def __init__(self):
        self.alpha = 0

    def update(self, sm):
        self.alpha = min(255, self.alpha + 1)

    def input(self, sm):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_x]:
            sm.set([FadeTransitionScene([GameScene(), self], [MainMenuScene(), LevelSelectScene()])])

    def draw(self, sm, screen):
        if len(sm.scenes) > 1:
            sm.scenes[-2].draw(sm, screen)

        # draw a transparent bg
        bgSurf = pygame.Surface((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
        bgSurf.fill((globals.BLACK))
        utils.blit_alpha(screen, bgSurf, (0, 0), self.alpha * 0.7)


        utils.drawText(screen, 'You lose! press x', 50, 50, globals.WHITE, 255)

#####################################################################

class TransitionScene(Scene):
        def __init__(self, fromScenes, toScenes):
            self.currentPercentage = 0
            self.fromScenes = fromScenes
            self.toScenes = toScenes

        def update(self, sm):
            self.currentPercentage += 2
            if self.currentPercentage >= 100:
                sm.pop()
                for s in self.toScenes:
                    sm.push(s)

#####################################################################

class FadeTransitionScene(TransitionScene):
    def draw(self, sm, screen):
        if self.currentPercentage < 50:
            for s in self.fromScenes:
                s.draw(sm, screen)
        else:
            if len(self.toScenes) == 0:
                if len(sm.scenes) > 1:
                    sm.scenes[-2].draw(sm, screen)
            else:
                for s in self.toScenes:
                    s.draw(sm, screen)

        #fade overlay
        # 0 = transparent, 255 = opaque
        # 0% = 0
        # 50% = 255
        # 100% = 0

        overlay = pygame.Surface((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
        alpha = int(abs(255 - ((255 / 50) * self.currentPercentage)))
        overlay.set_alpha(255 - alpha)
        overlay.fill(globals.BLACK)
        screen.blit(overlay, (0,0))


#####################################################################

class SceneManager:

    def __init__(self):
        self.scenes = []

    def isEmpty(self):
        return len(self.scenes) == 0

    def enterScene(self):
        if len(self.scenes) > 0:
            self.scenes[-1].onEnter()

    def exitScene(self):
        if len(self.scenes) > 0:
            self.scenes[-1].onExit()

    def input(self):
        if len(self.scenes) > 0:
            self.scenes[-1].input(self)

    def update(self):
        if len(self.scenes) > 0:
            self.scenes[-1].update(self)

    def draw(self, screen):
        if len(self.scenes) > 0:
            self.scenes[-1].draw(self, screen)

        #present screen
        pygame.display.flip()


    def push(self, scene):
        self.exitScene()
        self.scenes.append(scene)
        self.enterScene()

    def pop(self):
        self.exitScene()
        self.scenes.pop()
        self.enterScene()

    def set(self, scenes):
        # pop all scenes
        while len(self.scenes) > 0:
            self.pop()
        for s in scenes:
            self.push(s) #add new scene