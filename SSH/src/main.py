#https://penzilla.itch.io/hooded-protagonist

import pygame
import engine
import utils
import level
import scene
import globals
import inputstream
import soundmanager


#init
pygame.init()
screen = pygame.display.set_mode((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))  # Create the display surface
pygame.display.set_caption("Super Smash Hombres")  # Set the window title
clock = pygame.time.Clock()

sceneManager = scene.SceneManager()
mainMenu = scene.MainMenuScene()
sceneManager.push(mainMenu)

inputStream = inputstream.InputStream()

globals.soundManager = soundmanager.SoundManager()

globals.player1 = utils.makePlayer(300, 0)
globals.player1.camera = engine.Camera(10, 10, 400, 400)
globals.player1.camera.setWorldPos(300, 0)
globals.player1.camera.trackEntity(globals.player1)
globals.player1.input = engine.Input(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_q, pygame.K_e)
globals.player1.physics = engine.PhysicsSystem()


isRunning = True
#game loop
while isRunning:

    #check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False


    inputStream.processInput()
    globals.soundManager.update()

    if sceneManager.isEmpty():
        isRunning = False

    sceneManager.input(inputStream)
    sceneManager.update(inputStream)
    sceneManager.draw(screen)

    #lives
    clock.tick(60)

pygame.quit()