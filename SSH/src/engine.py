import pygame

class Position():
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

class Animations():
    def __init__(self):
        self.animationList = {}
    def add(self, state, animation):
        self.animationList[state] = animation



class Animation():
    def __init__(self, imageList):
        self.imageList = imageList
        self.imageIndex = 0
        self.animationTimer = 0
        self.animationSpeed = 10
    def update(self):
        #increment time
        self.animationTimer += 1
        #if timer gets too high..
        if self.animationTimer >+ self.animationSpeed:
            self.animationTimer = 0 #reset timer
            self.imageIndex += 1 #increment the current img
            if self.imageIndex > len(self.imageList) - 1:
                self.imageIndex = 0
                #loop back to the first img once index gets too high
    def draw(self, screen ,x, y, flipX, flipY):
        screen.blit(pygame.transform.flip(self.imageList[self.imageIndex], flipX, flipY), (x, y))

class Entity:
    def __init__(self):
        self.state = 'idle'
        self.type = 'normal'
        self.position = None
        self.animations = None



