import pygame
import sys


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

#menu loop
run = True
while run:
    screen.fill((52, 78, 91))
    
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()



