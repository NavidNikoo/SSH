#https://penzilla.itch.io/hooded-protagonist

import pygame
import engine
import utils

def drawText(t, x, y):
    text = font.render(t, x, y)
    text_rectangle = text.get_rect()
    text_rectangle.topleft = (x, y)
    screen.blit(text, text_rectangle)

# Define color constants for use in the GUI
#For custom colors, go to color picker on google and find the tuple and use it, make it a constant if you want
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (250, 250, 250)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
MUSTARD = (209, 206, 25)

# Set screen size parameters
SCREEN_WIDTH = 700  # Width of the application window
SCREEN_HEIGHT = 500  # Height of the application window

#init
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Create the display surface
pygame.display.set_caption("Super Smash Hombres")  # Set the window title
clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(), 24)

#game state = playing || win || lose
game_state = 'playing'

entities = []

#platforms
platforms = [
    pygame.Rect(100, 300, 400, 50),
    pygame.Rect(100, 250, 50, 50),
    pygame.Rect(450, 250, 50, 50)
]

#food
entities.append(utils.makeChicken(350, 250))
entities.append(utils.makeSushi(250, 250))
entities.append(utils.makeBurger(125, 200))
entities.append(utils.makeStrawberryCake(200, 250))
entities.append(utils.makeTaco(400, 250))

#enemies
entities.append(utils.makeEnemy(150, 268))

#players
player = utils.makePlayer(300, 0)
entities.append(player)


heart_image = pygame.image.load('assets/heart.png')
hearts = []

isRunning = True
player_speed = 0
player_acceleration = .2
lives = 3
health = 200

#game loop
while isRunning:

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



#####################################################################
    #UPDATE CODE
    if game_state == 'playing':

        for entity in entities:
            entity.animations.animationList[entity.state].update()

        new_player_rect = pygame.Rect(new_player_x, player.position.rect.y, player.position.rect.width, player.position.rect.height)
        x_collision = False

        #check against every platform
        for p in platforms:
            if p.colliderect(new_player_rect):
                x_collision = True
                break

        if x_collision == False:
            player.position.rect.x = new_player_x

        #vertical movement

        player_speed += player_acceleration
        new_player_y += player_speed


        new_player_rect = pygame.Rect(player.position.rect.x, new_player_y, player.position.rect.width, player.position.rect.height)
        y_collision = False
        player_on_ground = False

        #check against every platform
        for p in platforms:
            if p.colliderect(new_player_rect):
                # set x_collision to true
                y_collision = True
                player_speed = 0
                if p[1] > new_player_y: #check if the width is greater than the player
                    player.position.rect.y = p[1] - player.position.rect.height #stick player to platform
                    player_on_ground = True
                break

        if y_collision == False:
            player.position.rect.y = new_player_y

        # check against enemy and player collision
        player_rect = pygame.Rect(player.position.rect.x, player.position.rect.y, player.position.rect.width, player.position.rect.height)

        #collection system
        for entity in entities:
            if entity.type == 'collectable':
                if entity.position.rect.colliderect(player_rect):
                    entities.remove(entity)
                    health += 20
                if health <= 0:
                    lives -= 1

        #enemy system
        for entity in entities:
            if entity.type == 'dangerous':
                if entity.position.rect.colliderect(player_rect):
                    lives -= 1
                    player.position.rect.x = 200
                    player.position.rect.y = 0
                    player_speed = 0
                    if lives <= 0:
                        game_state = 'lose'

#####################################################################
    #DRAWING CODE

    screen.fill(DARK_GRAY) #background

    #platform
    for p in platforms:
        pygame.draw.rect(screen, MUSTARD, p)

    #draw system
    for entity in entities:
        s = entity.state
        a = entity.animations.animationList[s]
        if entity.direction == 'left':
            a.draw(screen, entity.position.rect.x, entity.position.rect.y, True, False)
        else:
            a.draw(screen, entity.position.rect.x, entity.position.rect.y, False, False)

    #player information display
    drawText('Health: ' + str(health), 10, 10)

    #lives
    for l in range(lives):
        screen.blit(heart_image, (200 + (l * 25), 0))


    if game_state == 'win':
        drawText('You win!', 50, 50)
        pass

    if game_state == 'lose':
        drawText('You Lose!', 50, 50)
        pass

        # present screen
    pygame.display.flip()

    #lives
    clock.tick(60)

pygame.quit()