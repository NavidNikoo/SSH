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
pygame.display.set_caption("Cool Coders Combat Royale")  # Set the window title
clock = pygame.time.Clock()

sceneManager = scene.SceneManager()
mainMenu = scene.MainMenuScene()
sceneManager.push(mainMenu)

inputStream = inputstream.InputStream()

globals.soundManager = soundmanager.SoundManager()

#create players
globals.player1 = utils.makePlayer(500, 200, "Samurai")
globals.player1.input = engine.Input(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_q, pygame.K_e, pygame.K_SPACE) #wasd, q zoom in, e zoom out, keyboard player

globals.player2 = utils.makePlayer2(550, 200, "Wind Hashashin") #Wind Assasin
globals.player2.input = engine.Input(pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l, pygame.K_u, pygame.K_o, pygame.K_0) #ijkl, u zoom in, o zoom out, controller player

globals.player3 = utils.makePlayer3(600, 200, "Ground Monk")
globals.player3.input = engine.Input(pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v, pygame.K_b, pygame.K_n, pygame.K_p) #zcxv, b zoom in, n zoom out, brian controller

globals.player4 = utils.makePlayer4(650, 200, "Ranger")
globals.player4.input = engine.Input(pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_m, pygame.K_z, pygame.K_h) #1324, m zoom in, z zoom out - A1-low: 3, A1-high: 4, A2 - Low: 1, A2-high: 2


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