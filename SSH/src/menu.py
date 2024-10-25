import pygame
import sys
import button
import main


pygame.init

#creating Game Window
Screen_width = 800
Screen_height = 600

screen = pygame.display.set_mode((Screen_width, Screen_height))
pygame.display.set_caption("SuperSmashHombres")

#game variables
game_start = False

#defining colours
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#button properties
font = pygame.font.Font(None, 36)
start_button = button.button(posx = 220, posy = 190, width = 200, height = 50, text = "Start", font = font, 
               color=(70,130,180), text_color = (255, 255, 255))
HowToPlay_button = button.button(posx = 220, posy = 190, width = 200, height = 50, text = "How To Play", font = font, 
                color=(70,130,180), text_color = (255, 255, 255))
Quit_button = button.button(posx = 220, posy = 190, width = 200, height = 50, text = "Quit", font = font, 
              color=(70,130,180), text_color = (255, 255, 255))

#menu loop
run = True
while run:
    screen.fill((52, 78, 91))
    if game_start == True:
        pass
    start_button.draw(screen)
    HowToPlay_button.draw(screen)
    Quit_button.draw(screen)

    #event handler
    for event in pygame.event.get():
        if start_button.is_clicked(event):
            main.game_state = "playing"
            main.screen
        if Quit_button.is_clicked(event):
            run = False
    pygame.display.update()

pygame.quit()
sys.exit()


