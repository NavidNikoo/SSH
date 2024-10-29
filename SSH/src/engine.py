import pygame
import utils
import globals

class System():
    def __init__(self):
        pass

    def check(self, entity):
        return True

    def update(self, screen):
        for entity in globals.world.entities:
            if self.check(entity):
                self.updateEntity(screen, entity)

    def updateEntity(self, screen, entity, world):
        pass

MUSTARD = (209, 206, 25)
BLACK = (0, 0, 0)
class CameraSystem(System):
    def __init__(self):
        super().__init__()

    def check(self, entity):
        return entity.camera is not None

    def updateEntity(self, screen, entity):

        #set clipping rectangle
        cameraRect = entity.camera.rect
        clipRect = pygame.Rect(cameraRect.x, cameraRect.y, cameraRect.w, cameraRect.h)
        screen.set_clip(clipRect)

        #update camera if tracking an entity
        if entity.camera.entityToTrack is not None:

            trackedEntity = entity.camera.entityToTrack

            currentX = entity.camera.worldX
            currentY = entity.camera.worldY

            targetX = trackedEntity.position.rect.x + trackedEntity.position.rect.w/2
            targetY = trackedEntity.position.rect.y + trackedEntity.position.rect.h/2

            entity.camera.worldX = (currentX * .98) + (targetX * 0.02)
            entity.camera.worldY = (currentY * .98) + (targetY * 0.02)

        #calculate offsets
        offsetX = cameraRect.x + cameraRect.w/2 - (entity.camera.worldX *  entity.camera.zoomLevel)
        offsetY = cameraRect.y + cameraRect.h/2 - (entity.camera.worldY *  entity.camera.zoomLevel)

        screen.fill(BLACK)

        #render platforms
        for p in globals.world.platforms:
            newPosRect = pygame.Rect(
                (p.x *  entity.camera.zoomLevel) + offsetX,
                (p.y *  entity.camera.zoomLevel) + offsetY,
                p.w *  entity.camera.zoomLevel,
                p.h *  entity.camera.zoomLevel)
            pygame.draw.rect(screen, MUSTARD, newPosRect)

        # render entities
        for e in globals.world.entities:
            s = e.state
            a = e.animations.animationList[s]
            a.draw(screen,
                   (e.position.rect.x * entity.camera.zoomLevel) + offsetX,
                   (e.position.rect.y * entity.camera.zoomLevel) + offsetY,
                   e.direction == 'left',
                   False,
                   entity.camera.zoomLevel)

        # entity HUD
        # player health display
        if entity.health is not None:
            utils.drawText(screen, 'Health: ' + str(entity.health.health), entity.camera.rect.x + 10, entity.camera.rect.x + 50, globals.WHITE, 255)

        # lives
        if entity.battle is not None:
            for l in range(entity.battle.lives):
                screen.blit(utils.heart_image, (entity.camera.rect.x + 0 + (l * 25), entity.camera.rect.y + 0))


        screen.set_clip(None)

class Camera():
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.worldX = 0
        self.worldY = 0
        self.entityToTrack = None
        self.zoomLevel = 1

    def setWorldPos(self, x, y):
        self.worldX = x
        self.worldY = y

    def trackEntity(self, e):
        self.entityToTrack = e



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
        self.animationSpeed = 7
    def update(self):
        #increment time
        self.animationTimer += 1
        #if timer gets too high..
        if self.animationTimer >= self.animationSpeed:
            self.animationTimer = 0 #reset timer
            self.imageIndex += 1 #increment the current img
            if self.imageIndex > len(self.imageList) - 1:
                self.imageIndex = 0
                #loop back to the first img once index gets too high
    def draw(self, screen ,x, y, flipX, flipY, zoomLevel):
        image = self.imageList[self.imageIndex]
        newWidth = int(image.get_rect().w * zoomLevel)
        newHeight = int(image.get_rect().h * zoomLevel)
        screen.blit(pygame.transform.scale(pygame.transform.flip(image, flipX, flipY), (newWidth, newHeight)), (x, y))

class Health(): #score
    def __init__(self):
        self.health = 200

class Battle():
    def __init__(self):
        self.lives = 3

class Entity:
    def __init__(self):
        self.state = 'idle'
        self.type = 'normal'
        self.position = None
        self.animations = Animations()
        self.direction = 'right'
        self.camera = None
        self.health = None
        self.battle = None
