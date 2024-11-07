import pygame
import utils
import globals

class System():
    def __init__(self):
        pass

    def check(self, entity):
        return True

    def update(self, screen=None, inputStream=None):
        for entity in globals.world.entities:
            if self.check(entity):
                self.updateEntity(screen, inputStream, entity)

    def updateEntity(self, screen, inputStream, entity):
        pass

class AnimationSystem(System):
    def check(self, entity):
        return entity.animations is not None

    def updateEntity(self, screen, inputStream, entity):
        entity.animations.animationList[entity.state].update()


class PhysicsSystem(System):
    def check(self, entity):
        return entity.position is not None

    def updateEntity(self, screen, inputStream, entity):

        new_x = entity.position.rect.x
        new_y = entity.position.rect.y


        if entity.intention is not None:
            if entity.intention.moveLeft:
                new_x -= 2
                entity.direction = 'left'
                entity.state = 'walking'
            if entity.intention.moveRight:
                new_x += 2
                entity.direction = 'right'
                entity.state = 'walking'
            if not entity.intention.moveLeft and not entity.intention.moveRight:
                entity.state = 'idle'
            if entity.intention.jump and entity.on_ground: #up if on ground
                entity.speed = -5

        #horizontal movement
        new_x_rect = pygame.Rect(
            int(new_x),
            int(entity.position.rect.y),
            int(entity.position.rect.width),
            int(entity.position.rect.height))

        x_collision = False

        #check against every platform
        for platform in globals.world.platforms:
            if platform.colliderect(new_x_rect):
                x_collision = True
                break

        if x_collision == False:
            entity.position.rect.x = new_x

        #vertical movement

        entity.speed += entity.acceleration
        new_y += entity.speed


        new_y_rect = pygame.Rect(
            int(entity.position.rect.x),
            int(new_y),
            int(entity.position.rect.width),
            int(entity.position.rect.height))

        y_collision = False
        entity.on_ground = False

        #check against every platform
        for platform in globals.world.platforms:
            if platform.colliderect(new_y_rect):
                # set x_collision to true
                y_collision = True
                entity.speed = 0
                if platform[1] > new_y: #check if the width is greater than the player
                    entity.position.rect.y = platform[1] - entity.position.rect.height #stick player to platform
                    entity.on_ground = True
                break

        if y_collision == False:
            entity.position.rect.y = int(new_y)

        #reset intentions
        if entity.intention is not None:
            entity.intention.moveLeft = False
            entity.intention.moveRight = False
            entity.intention.jump = False
            #entity.intention. = False
            #entity.intention. = False





class InputSystem(System):

    def check(self, entity):
        return entity.input is not None and entity.intention is not None

    def updateEntity(self, screen, inputStream, entity):

        #up = jump
        if inputStream.keyboard.isKeyDown(entity.input.up):
            entity.intention.jump = True
        else:
            entity.intention.jump = False

        #left = walk left
        if inputStream.keyboard.isKeyDown(entity.input.left):
            entity.intention.moveLeft = True
        else:
            entity.intention.moveLeft = False

        #right = move rihgt
        if inputStream.keyboard.isKeyDown(entity.input.right):
            entity.intention.moveRight = True
        else:
            entity.intention.moveRight = False

        #b1 = zoom out
        if inputStream.keyboard.isKeyDown(entity.input.b1):
            entity.intention.zoomOut = True
        else:
            entity.intention.zoomOut = False

        #b2 = zoom out
        if inputStream.keyboard.isKeyDown(entity.input.b2):
            entity.intention.zoomIn = True
        else:
            entity.intention.zoomIn = False

        print(entity.intention.moveRight)


class CollectionSystem(System):
    def check(self, entity):
        return entity.type == 'player' and entity.health is not None

    def updateEntity(self, screen, inputStream, entity):
        for otherEntity in globals.world.entities:
            if otherEntity is not entity and otherEntity.type == 'collectable':
                if entity.position.rect.colliderect(otherEntity.position.rect):
                    #entity.collectable.onCollide(entity, otherEntity)
                    globals.world.entities.remove(otherEntity)
                    entity.health.health += 20



class BattleSystem(System):
    def check(self, entity):
        return entity.type == 'player' and entity.battle is not None

    def updateEntity(self, screen, inputStream, entity):
        for otherEntity in globals.world.entities:
            if otherEntity is not entity and otherEntity.type == 'dangerous': #change to player to hurt each other
                if entity.position.rect.colliderect(otherEntity.position.rect):
                    #entity.battle.onCollide(entity, otherEntity)
                    entity.battle.lives -= 1
                    entity.position.rect.x = 200
                    entity.position.rect.y = 0
                    entity.speed = 0



class CameraSystem(System):


    def check(self, entity):
        return entity.camera is not None

    def updateEntity(self, screen, inputStream, entity):

        if entity.intention is not None:
            if entity.intention.zoomIn:
                entity.camera.zoomLevel += 0.01
            if entity.intention.zoomOut:
                if entity.camera.zoomLevel > 0:
                    entity.camera.zoomLevel -= 0.01

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

        screen.fill(globals.BLACK)

        #render platforms
        for p in globals.world.platforms:
            newPosRect = pygame.Rect(
                (p.x *  entity.camera.zoomLevel) + offsetX,
                (p.y *  entity.camera.zoomLevel) + offsetY,
                p.w *  entity.camera.zoomLevel,
                p.h *  entity.camera.zoomLevel)
            pygame.draw.rect(screen, globals.MUSTARD, newPosRect)

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

class Camera:
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



class Position:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

class Animations:
    def __init__(self):
        self.animationList = {}
    def add(self, state, animation):
        self.animationList[state] = animation



class Animation:
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

class Health: #score
    def __init__(self):
        self.health = 200

class Battle:
    def __init__(self):
        self.lives = 3

class Input:
    def __init__(self, up, down, left, right, b1, b2):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.b1 = b1
        self.b2 = b2

class Intention:
    def __init__(self):
        self.moveLeft = False
        self.moveRight = False
        self.jump = False
        self.zoomIn = False
        self.zoomOut = False


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
        self.speed = 0
        self.input = None
        self.intention = None
        self.on_ground = False
        self.acceleration = 0.2