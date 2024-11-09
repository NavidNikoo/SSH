import pygame
import utils
import globals
import engine
import UI
import level
#####################################################################

class Scene:
    def __init__(self):
        pass

    def onEnter(self):
        pass

    def onExit(self):
        pass

    def input(self, sm, inputStream):
        pass

    def update(self, sm, inputStream):
        pass

    def draw(self, sm, screen):
        pass

#####################################################################

class MainMenuScene(Scene):

    def __init__(self):
        self.enter = UI.ButtonUI(pygame.K_RETURN, '[Enter = next]', 50, 200)
        self.esc = UI.ButtonUI(pygame.K_ESCAPE, '[Esq = quit]', 50, 300)

    def onEnter(self):

        globals.soundManager.playMusicFade('menu')


    def input(self, sm, inputStream): #sm = SceneManager

        if inputStream.keyboard.isKeyPressed(pygame.K_RETURN):
            sm.push(FadeTransitionScene([self], [LevelSelectScene()]))
        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.pop()

    def update(self, sm, inputStream):
        self.enter.update(inputStream)
        self.esc.update(inputStream)


    def draw(self, sm, screen):
        screen.fill(globals.DARK_GRAY)
        utils.drawText(screen, 'Main Menu', 50, 50, globals.WHITE, 255)
        self.enter.draw(screen)
        self.esc.draw(screen)

#####################################################################

class LevelSelectScene(Scene):

    def __init__(self):
        self.level1 = UI.ButtonUI(pygame.K_1, '[Level 1]', 50, 200)
        self.level2 = UI.ButtonUI(pygame.K_2, '[Level 2]', 50, 300)
        self.esc = UI.ButtonUI(pygame.K_ESCAPE, '[Esq = quit]', 50, 400)

    def update(self, sm, inputStream):
        self.level1.update(inputStream)
        self.level2.update(inputStream)
        self.esc.update(inputStream)


    def input(self, sm, inputStream):

        if inputStream.keyboard.isKeyPressed(pygame.K_1):
            level.loadLevel(1)
            sm.push(FadeTransitionScene([self], [GameScene()]))
        if inputStream.keyboard.isKeyPressed(pygame.K_2):
            level.loadLevel(2)
            sm.push(FadeTransitionScene([self], [GameScene()]))
        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.pop()
            sm.push(FadeTransitionScene([self], []))

    def draw(self, sm, screen):
        screen.fill(globals.DARK_GRAY)
        utils.drawText(screen, 'Level Select [1/2 = Level, esc=quit]', 50, 50, globals.WHITE, 255)
        self.level1.draw(screen)
        self.level2.draw(screen)
        self.esc.draw(screen)

#####################################################################

class GameScene(Scene):

    def __init__(self):
        self.cameraSystem = engine.CameraSystem()
        self.collectionSystem = engine.CollectionSystem()
        self.battleSystem = engine.BattleSystem()
        self.inputSystem = engine.InputSystem()
        self.physicsSystem = engine.PhysicsSystem()
        self.animationSystem = engine.AnimationSystem()


    def onEnter(self):
        globals.soundManager.playMusicFade('game')

    def input(self, sm, inputStream):

        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.pop()
            sm.push(FadeTransitionScene([self], []))
        if globals.world.isWon():
            sm.push(WinScene())
        if globals.world.isLost():
            sm.push(LoseScene())

    def update(self, sm, inputStream):
        self.inputSystem.update(inputStream=inputStream)
        self.collectionSystem.update()
        self.battleSystem.update()
        self.physicsSystem.update()
        self.animationSystem.update()

    def draw(self, sm, screen):
        screen.fill(globals.DARK_GRAY)
        self.cameraSystem.update(screen)

#####################################################################

class WinScene(Scene):

    def __init__(self):
        self.alpha = 0
        self.esc = UI.ButtonUI(pygame.K_ESCAPE, '[Esq = quit]', 50, 200)


    def update(self, sm, inputStream):
        self.alpha = min(255, self.alpha + 10)
        self.esc.update(inputStream)

    def input(self, sm, inputStream):

        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.set([FadeTransitionScene([GameScene(), self], [MainMenuScene(), LevelSelectScene()])])

    def draw(self, sm, screen):
        if len(sm.scenes) > 1:
            sm.scenes[-2].draw(sm, screen)

        bgSurf = pygame.Surface((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
        bgSurf.fill((globals.BLACK))
        utils.blit_alpha(screen, bgSurf, (0, 0), self.alpha * 0.7)

        utils.drawText(screen, 'You win!', 50, 50, globals.WHITE, self.alpha)
        self.esc.draw(screen, alpha=self.alpha)


class LoseScene(Scene):

    def __init__(self):
        self.alpha = 0
        self.esc = UI.ButtonUI(pygame.K_ESCAPE, '[Esq = quit]', 50, 200)


    def update(self, sm, inputStream):
        self.alpha = min(255, self.alpha + 10)
        self.esc.update(inputStream)

    def input(self, sm, inputStream):

        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.set([FadeTransitionScene([GameScene(), self], [MainMenuScene(), LevelSelectScene()])])

    def draw(self, sm, screen):
        if len(sm.scenes) > 1:
            sm.scenes[-2].draw(sm, screen)

        # draw a transparent bg
        bgSurf = pygame.Surface((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
        bgSurf.fill((globals.BLACK))
        utils.blit_alpha(screen, bgSurf, (0, 0), self.alpha * 0.7)


        utils.drawText(screen, 'You lose!', 50, 50, globals.WHITE, 255)
        self.esc.draw(screen, alpha=self.alpha)

#####################################################################

class TransitionScene(Scene):
        def __init__(self, fromScenes, toScenes):
            self.currentPercentage = 0
            self.fromScenes = fromScenes
            self.toScenes = toScenes

        def update(self, sm, inputStream):
            self.currentPercentage += 2
            if self.currentPercentage >= 100:
                sm.pop()
                for s in self.toScenes:
                    sm.push(s)

            for scene in self.fromScenes:
                scene.update(sm, inputStream)
            if len(self.toScenes) > 0:
                for scene in self.toScenes:
                    scene.update(sm, inputStream)
            else:
                if len(sm.scenes)> 1:
                    sm.scenes[-2].update(sm, inputStream)

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

    def input(self, inputStream):
        if len(self.scenes) > 0:
            self.scenes[-1].input(self, inputStream)

    def update(self, inputStream):
        if len(self.scenes) > 0:
            self.scenes[-1].update(self, inputStream)

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