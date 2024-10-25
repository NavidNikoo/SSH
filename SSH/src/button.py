import pygame


class button:
    def __init__(self, posx, posy, width, height, text, font, color, text_color):
        self.rect = pygame.Rect(posx, posy, width, height)
        self.color = color
        self.text_color = text_color
        self.text = font.render.get_rect(center=self.rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text, self.text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        else:
            return False
        