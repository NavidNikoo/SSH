#https://penzilla.itch.io/hooded-protagonist

import pygame

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


#samurai
player_image = pygame.image.load('assets/samurai_0.png')
#players = []

#platforms
platforms = [
    pygame.Rect(100, 300, 400, 50),
    pygame.Rect(100, 250, 50, 50),
    pygame.Rect(450, 250, 50, 50)
]

#food image
food_image = pygame.image.load('assets/86_roastedchicken_dish.png')
food_image1 = pygame.image.load('assets/15_burger.png')
food = [
    pygame.Rect(200, 250, 32, 32),
    pygame.Rect(250, 250, 32, 32)
]


enemy_image = pygame.image.load('assets/hoodlum_1.png')
enemies = [
    pygame.Rect(150,268, 32, 32)

]

lives = 3
heart_image = pygame.image.load('assets/heart.png')
hearts = [

]

health = 200

isRunning = True
player_x = 300
player_y = 0

player_width = 22
player_height = 35

SPAWN_X = 200
SPAWN_Y = 0

new_player_x = player_x
new_player_y = player_y

player_speed = 0
player_acceleration = .2

player_direction = 'right'

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

        new_player_x = player_x
        new_player_y = player_y

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]: #left
            new_player_x -= 2
            player_direction = 'left'
        if keys[pygame.K_d]: #right
            new_player_x += 2
            player_direction = 'right'
        if keys[pygame.K_w] and player_on_ground: #up if on ground
            player_speed = -5


#####################################################################
    #UPDATE CODE
    if game_state == 'playing':

        new_player_rect = pygame.Rect(new_player_x, player_y, player_width, player_height)
        x_collision = False

        #check against every platform
        for p in platforms:
            if p.colliderect(new_player_rect):
                x_collision = True
                break

        if x_collision == False:
            player_x = new_player_x

        #vertical movement

        player_speed += player_acceleration
        new_player_y += player_speed


        new_player_rect = pygame.Rect(player_x, new_player_y, player_width, player_height)
        y_collision = False
        player_on_ground = False

        #check against every platform
        for p in platforms:
            if p.colliderect(new_player_rect):
                # set x_collision to true
                y_collision = True
                player_speed = 0
                if p[1] > new_player_y: #check if the width is greater than the player
                    player_y = p[1] - player_height #stick player to platform
                    player_on_ground = True
                break

        if y_collision == False:
            player_y = new_player_y


        #check against enemy and player collision
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for enemy in enemies:
            if enemy.colliderect(player_rect):
                lives -=1
                #reset player position
                player_x = SPAWN_X
                player_y = SPAWN_Y
                player_speed = 0
                #change the game state if no live remaining
                if lives <= 0:
                    game_state = 'lose'

        #see if any food has been eaten
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for meal in food:
            if meal.colliderect(player_rect):
                food.remove(meal)
                health += 20

        print(health)

#####################################################################
    #DRAWING CODE

    screen.fill(DARK_GRAY) #background



    #platform
    for p in platforms:
        pygame.draw.rect(screen, MUSTARD, p)

    #enemies
    for enemy in enemies:
        screen.blit(enemy_image, (enemy.x, enemy.y))

    #food
    for meal in food:
        screen.blit(food_image, (meal.x, meal.y))
        screen.blit(food_image1, (meal.x, meal.y))

    # player
    if player_direction == 'right':
        screen.blit(player_image, (player_x, player_y))
    elif player_direction == 'left':
        screen.blit(pygame.transform.flip(player_image, True, False), (player_x, player_y))

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