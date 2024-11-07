#https://penzilla.itch.io/hooded-protagonist

import pygame
import engine
import utils
import level
import scene
import globals
import inputstream

#init
pygame.init()
screen = pygame.display.set_mode((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))  # Create the display surface
pygame.display.set_caption("Super Smash Hombres")  # Set the window title
clock = pygame.time.Clock()

#food
Chicken = utils.makeChicken(350, 250)
Sushi = utils.makeSushi(250, 250)
Burger = utils.makeBurger(125, 200)
StrawberryCake = utils.makeStrawberryCake(200, 250)
Taco = utils.makeTaco(400, 250)

#enemies
enemy = utils.makeEnemy(150, 268)
enemy.camera = engine.Camera(420, 10, 200, 200)
enemy.camera.setWorldPos(150, 250)

#playersx
player = utils.makePlayer(300, 0)
player.camera = engine.Camera(10, 10, 400, 400)
player.camera.setWorldPos(300, 0)
player.camera.trackEntity(player)
player.health = engine.Health()
player.battle = engine.Battle()
player.input = engine.Input(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_q, pygame.K_e)
player.intention = engine.Intention()
player.physics = engine.PhysicsSystem()
cameraSys = engine.CameraSystem()

#lose if players have no lives remaining
def lostLevel(level):

    # level isn't lost if any player has a life left
    for entity in level.entities:
        if entity.type == 'player':
              if entity.battle is not None:
                  if entity.battle.lives > 0:
                      return False

    #level is lost otherwise
    return True

#Temp win status: win if all collectables(food) are collected, will eventually change to when there is one man left standing
def wonLevel(level):
    #level isn't won if any collectables are left
    for entity in level.entities:
        if entity.type == 'collectable':
            return False

    #otherwise level is won
    return True

globals.levels[1] = level.Level(
    platforms=[
        pygame.Rect(100, 300, 400, 50),
        pygame.Rect(100, 250, 50, 50),
        pygame.Rect(450, 250, 50, 50)
    ],
    entities = [
        player, enemy, Chicken, Sushi, Burger, StrawberryCake, Taco
    ],
    winFunc=wonLevel,
    loseFunc=lostLevel
)

globals.levels[2] = level.Level(
    platforms=[
        pygame.Rect(100, 300, 400, 50),
    ],
    entities = [
        player, Taco
    ],
    winFunc=wonLevel,
    loseFunc=lostLevel
)

#set the current level

globals.world = globals.levels[1]

sceneManager = scene.SceneManager()
mainMenu = scene.MainMenuScene()
sceneManager.push(mainMenu)

inputStream = inputstream.InputStream()

isRunning = True

#game loop
while isRunning:

    #check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False


    inputStream.processInput()

    if sceneManager.isEmpty():
        isRunning = False

    sceneManager.input(inputStream)
    sceneManager.update(inputStream)
    sceneManager.draw(screen)

    #lives
    clock.tick(60)

pygame.quit()