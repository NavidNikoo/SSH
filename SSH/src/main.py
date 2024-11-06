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

#game state = playing || win || lose
game_state = 'playing'

#platforms

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
player_speed = 0
player_acceleration = .2


#game loop
while isRunning:


    inputStream.processInput()

    if sceneManager.isEmpty():
        isRunning = False

    sceneManager.input(inputStream)
    sceneManager.update(inputStream)
    sceneManager.draw(screen)

    #INPUT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

#####################################################################
    #player input
    # horizontal movement
    if game_state == 'playing':

        new_player_x = player.position.rect.x
        new_player_y = player.position.rect.y

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]: #left
            new_player_x -= 2
            player.direction = 'left'
            player.state = 'walking'
        if keys[pygame.K_d]: #right
            new_player_x += 2
            player.direction = 'right'
            player.state = 'walking'
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            player.state = 'idle'
        if keys[pygame.K_w] and player_on_ground: #up if on ground
            player_speed = -5


        #control zoom level of the player camera
        #zoom out
        if keys[pygame.K_q]:
            if player.camera.zoomLevel > 0:
                player.camera.zoomLevel -= 0.01
        if keys[pygame.K_e]:
            player.camera.zoomLevel += 0.01



#####################################################################
    #UPDATE CODE
    if game_state == 'playing':

        for entity in globals.world.entities:
            entity.animations.animationList[entity.state].update()

        new_player_rect = pygame.Rect(new_player_x, player.position.rect.y, player.position.rect.width, player.position.rect.height)
        x_collision = False

        #check against every platform
        for p in globals.world.platforms:
            if p.colliderect(new_player_rect):
                x_collision = True
                break

        if x_collision == False:
            player.position.rect.x = new_player_x

        #vertical movement

        player_speed += player_acceleration
        new_player_y += player_speed


        new_player_rect = pygame.Rect(int(player.position.rect.x), int(new_player_y), player.position.rect.width, player.position.rect.height)
        y_collision = False
        player_on_ground = False

        #check against every platform
        for p in globals.world.platforms:
            if p.colliderect(new_player_rect):
                # set x_collision to true
                y_collision = True
                player_speed = 0
                if p[1] > new_player_y: #check if the width is greater than the player
                    player.position.rect.y = p[1] - player.position.rect.height #stick player to platform
                    player_on_ground = True
                break

        if y_collision == False:
            player.position.rect.y = int(new_player_y)

        # check against enemy and player collision
        player_rect = pygame.Rect(int(player.position.rect.x), int(player.position.rect.y), player.position.rect.width, player.position.rect.height)

        #collection system
        for entity in globals.world.entities:
            if entity.type == 'collectable':
                if entity.position.rect.colliderect(player_rect):
                    globals.world.entities.remove(entity)
                    player.health.health += 20
                if player.health.health <= 0:
                    player.battle.lives -= 1


        #enemy system
        for entity in globals.world.entities:
            if entity.type == 'dangerous':
                if entity.position.rect.colliderect(player_rect):
                    player.battle.lives -= 1
                    player.position.rect.x = 200
                    player.position.rect.y = 0
                    player_speed = 0

#####################################################################

    #lives
    clock.tick(60)

pygame.quit()