import pygame
import utils
import globals
import level

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

class PowerupSystem(System): #maybe make projecticle and effect
    def check(self, entity):
        return entity.effect is not None

    def updateEntity(self, screen, inputStream, entity):
        #collection of power ups
        for otherEntity in globals.world.entities:
            if otherEntity is not entity and otherEntity.type == 'player' and entity.type != 'player':
                 if entity.position.rect.colliderect(otherEntity.position.rect):
                     #give effect component to the player
                    otherEntity.effect = entity.effect
                    globals.soundManager.playSound(entity.effect.sound) #switch sound and picture in utils later
                    globals.world.entities.remove(entity)

        #apply powerup effects for players
        if entity.type == 'player':
            entity.effect.apply(entity)
            entity.effect.timer -= 1

            #if effect has run out
            if entity.effect.timer < 0:

                #reset entity if appropriate
                if entity.effect.end:
                    entity.effect.end(entity)

                entity.effect = None #destroy the effect


class AnimationSystem(System):
    def check(self, entity):
        return entity.animations is not None

    def updateEntity(self, screen, inputStream, entity):
        # Debug current state

        if entity.state in entity.animations.animationList:
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
            if entity.intention.jump and entity.on_ground:  # Jump if on ground
                globals.soundManager.playSound('jump')
                entity.speed = -5

        # Horizontal movement
        new_x_rect = pygame.Rect(
            int(new_x),
            int(entity.position.rect.y),
            int(entity.position.rect.width),
            int(entity.position.rect.height))

        x_collision = False

        for platform in globals.world.platforms:
            if isinstance(platform, Platform):  # If it's a Platform object
                if platform.rect.colliderect(new_x_rect):  # Use the rect for collision
                    x_collision = True
                    break
            elif isinstance(platform, pygame.Rect):  # For legacy Rect platforms
                if platform.colliderect(new_x_rect):
                    x_collision = True
                    break

        if not x_collision:
            entity.position.rect.x = new_x

        # Vertical movement
        entity.speed += entity.acceleration
        new_y += entity.speed

        new_y_rect = pygame.Rect(
            int(entity.position.rect.x),
            int(new_y),
            int(entity.position.rect.width),
            int(entity.position.rect.height))

        y_collision = False
        entity.on_ground = False

        for platform in globals.world.platforms:
            if isinstance(platform, Platform):  # Check if it's a Platform object
                if platform.rect.colliderect(new_y_rect):  # Use the rect for collision
                    y_collision = True
                    entity.speed = 0
                    if platform.rect.y > new_y:  # Check if the width is greater than the player
                        entity.position.rect.y = platform.rect.y - entity.position.rect.height  # Stick player to platform
                        entity.on_ground = True
                    break
            elif isinstance(platform, pygame.Rect):  # Legacy platforms
                if platform.colliderect(new_y_rect):
                    y_collision = True
                    entity.speed = 0
                    if platform.y > new_y:
                        entity.position.rect.y = platform.y - entity.position.rect.height
                        entity.on_ground = True
                    break

        if not y_collision:
            entity.position.rect.y = int(new_y)

        # Handle falling timer
        if not entity.on_ground:
            entity.fallingTimer += 1  # Increment falling timer

            # Check if the entity has a `battle` component
            if entity.battle is not None and entity.fallingTimer >= 300:  # 5 seconds at 60 FPS
                entity.battle.lives -= 1  # Deduct a life
                entity.health.health = 200  # Reset health
                entity.position.rect.x = entity.position.initial.x  # Reset to initial position
                entity.position.rect.y = entity.position.initial.y

                if entity.battle.lives <= 0:  # Check if no lives are left
                    globals.world.entities.remove(entity)  # Remove entity from the game
                else:
                    entity.fallingTimer = 0  # Reset falling timer
        else:
            entity.fallingTimer = 0  # Reset falling timer when on the ground

        # Reset intentions
        if entity.intention is not None:
            entity.intention.moveLeft = False
            entity.intention.moveRight = False
            entity.intention.jump = False

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

        #b3 = melee
        if inputStream.keyboard.isKeyPressed(entity.input.b3):
            entity.intention.melee = True
        else:
            entity.intention.melee = False


class CollectionSystem(System):
    def check(self, entity):
        return entity.type == 'player' and entity.health is not None

    def updateEntity(self, screen, inputStream, entity):
        for otherEntity in globals.world.entities:
            if otherEntity is not entity and otherEntity.type == 'collectable':
                if entity.position.rect.colliderect(otherEntity.position.rect):
                    #entity.collectable.onCollide(entity, otherEntity)
                    globals.soundManager.playSound('eat')
                    globals.world.entities.remove(otherEntity)
                    entity.health.health += 20

class BattleSystem(System):
    def check(self, entity):
        return entity.type == 'player' and entity.battle is not None

    def updateEntity(self, screen, inputStream, entity):

        # Handle collisions with dangerous entities (e.g., projectiles)
        for otherEntity in globals.world.entities:
            if otherEntity is not entity and otherEntity.type == 'teleport':
                if entity.position.rect.colliderect(otherEntity.position.rect):
                    entity.position.rect.x = entity.position.initial.x  # Reset position
                    entity.position.rect.y = entity.position.initial.y

        # Handle collisions with dangerous entities (e.g., projectiles)
        for otherEntity in globals.world.entities:
            if otherEntity is not entity and otherEntity.type == 'dangerous':
                if entity.position.rect.colliderect(otherEntity.position.rect):
                    entity.health.health -= 20
                    if entity.direction == 'right':
                        entity.position.rect.x -= 20
                    else:
                        entity.position.rect.x += 20

        # Handle collisions with dangerous entities (e.g., projectiles)
        for otherEntity in globals.world.entities:
            if otherEntity is not entity and otherEntity.type == 'dangerous':
                if entity.position.rect.colliderect(otherEntity.position.rect):
                    entity.health.health -= 20
                    if entity.direction == 'right':
                        entity.position.rect.x -= 20
                    else:
                        entity.position.rect.x += 20

                if entity.health.health <= 0:
                    entity.battle.lives -= 1  # Decrement lives
                    entity.health.health = 200  # Reset health for the next life (if applicable)
                    entity.position.rect.x = entity.position.initial.x  # Reset position
                    entity.position.rect.y = entity.position.initial.y

                    if entity.battle.lives <= 0:  # Check if no lives are left
                        globals.world.entities.remove(entity)  # Remove entity from the game

        # Handle attacks
        current_time = pygame.time.get_ticks()

        # If currently attacking, ensure state is locked to 'melee'
        if entity.is_attacking:
            # Wait until the animation completes before resetting state
            if entity.intention.melee and (current_time - entity.attack_timer >= entity.attack_cooldown):
                entity.state = 'idle'  # Return to idle state
                entity.is_attacking = False
            return  # Skip further processing while attacking

        # Check if the player is attempting to attack
        if entity.intention.melee and (current_time - entity.attack_timer >= entity.attack_cooldown):
            entity.is_attacking = True
            entity.attack_timer = current_time
            entity.state = 'melee'  # Set state to melee for animation

            # Create attack hitbox
            attack_x = entity.position.rect.x + (
                entity.attack_range if entity.direction == 'right' else -entity.attack_range)
            attack_y = entity.position.rect.y
            attack_hitbox = pygame.Rect(
                attack_x, attack_y, entity.attack_range, entity.position.rect.height
            )

            # Debugging: Draw hitbox and log details
            #print(f"Attack Hitbox: {attack_hitbox}")

            # Check for collisions with other players
            for otherEntity in globals.world.entities:
                if otherEntity is not entity and otherEntity.type == 'player':  # PvP attack
                    if attack_hitbox.colliderect(otherEntity.position.rect):
                        # Apply damage
                        otherEntity.health.health -= entity.attack_damage
                        #print(f"{entity} hit {otherEntity}! Health left: {otherEntity.health.health}")

                        # Apply knockback
                        if entity.direction == 'right':
                            otherEntity.position.rect.x += 20
                        else:
                            otherEntity.position.rect.x -= 20

                        # Handle death
                        if otherEntity.health.health <= 0:
                            #print(f"{otherEntity} has been eliminated!")
                            globals.world.entities.remove(otherEntity)

class CameraSystem(System):

    def check(self, entity):
        return entity.camera is not None

    def updateEntity(self, screen, inputStream, entity):
        if entity.intention is not None:
            if entity.intention.zoomIn:  # b1
                entity.camera.zoomLevel += 0.01
            if entity.intention.zoomOut:  # b2
                if entity.camera.zoomLevel >= 1:
                    entity.camera.zoomLevel -= 0.01

        # Set clipping rectangle
        cameraRect = entity.camera.rect
        clipRect = pygame.Rect(cameraRect.x, cameraRect.y, cameraRect.w, cameraRect.h)
        screen.set_clip(clipRect)

        # Update camera if tracking an entity
        if entity.camera.entityToTrack is not None:
            trackedEntity = entity.camera.entityToTrack
            currentX = entity.camera.worldX
            currentY = entity.camera.worldY

            targetX = trackedEntity.position.rect.x + trackedEntity.position.rect.w / 2
            targetY = trackedEntity.position.rect.y + trackedEntity.position.rect.h / 2

            entity.camera.worldX = (currentX * 0.98) + (targetX * 0.02)
            entity.camera.worldY = (currentY * 0.98) + (targetY * 0.02)

        # Calculate offsets
        offsetX = cameraRect.x + cameraRect.w / 2 - (entity.camera.worldX * entity.camera.zoomLevel)
        offsetY = cameraRect.y + cameraRect.h / 2 - (entity.camera.worldY * entity.camera.zoomLevel)

        # Change backgrounds

        # Render background specific to the camera
        if globals.currentLevel == 1:
            background1 = pygame.image.load('assets/BG.png')
            bg_width, bg_height = background1.get_size()

            # Calculate camera viewport dimensions
            camera_width = entity.camera.rect.w
            camera_height = entity.camera.rect.h

            # Calculate the portion of the background to display
            bg_x = int(entity.camera.worldX * entity.camera.zoomLevel - camera_width / 2)
            bg_y = int(entity.camera.worldY * entity.camera.zoomLevel - camera_height / 2)

            # Clamp background position to within the image bounds
            bg_x = max(0, min(bg_x, bg_width - camera_width))
            bg_y = max(0, min(bg_y, bg_height - camera_height))

            # Create a subsurface of the background for the current camera
            cropped_background = background1.subsurface(pygame.Rect(bg_x, bg_y, camera_width, camera_height))

            # Scale the cropped background to fit the camera's zoom level
            scaled_background = pygame.transform.scale(
                cropped_background,
                (int(camera_width), int(camera_height))
            )

            # Draw the scaled background on the camera's viewport
            screen.blit(scaled_background, (entity.camera.rect.x, entity.camera.rect.y))

        if globals.currentLevel == 2:
            background2 = pygame.image.load('assets/BG2.png')
            bg_width, bg_height = background2.get_size()

            # Calculate camera viewport dimensions
            camera_width = entity.camera.rect.w
            camera_height = entity.camera.rect.h

            # Calculate the portion of the background to display
            bg_x = int(entity.camera.worldX * entity.camera.zoomLevel - camera_width / 2)
            bg_y = int(entity.camera.worldY * entity.camera.zoomLevel - camera_height / 2)

            # Clamp background position to within the image bounds
            bg_x = max(0, min(bg_x, bg_width - camera_width))
            bg_y = max(0, min(bg_y, bg_height - camera_height))

            # Create a subsurface of the background for the current camera
            cropped_background = background2.subsurface(pygame.Rect(bg_x, bg_y, camera_width, camera_height))

            # Scale the cropped background to fit the camera's zoom level
            scaled_background = pygame.transform.scale(
                cropped_background,
                (int(camera_width), int(camera_height))
            )

            # Draw the scaled background on the camera's viewport
            screen.blit(scaled_background, (entity.camera.rect.x, entity.camera.rect.y))

            # Draw the scaled background on the camera's viewport
            screen.blit(scaled_background, (entity.camera.rect.x, entity.camera.rect.y))

        if globals.currentLevel == 3:
            background3 = pygame.image.load('assets/BG3.png')
            bg_width, bg_height = background3.get_size()

            # Calculate camera viewport dimensions
            camera_width = entity.camera.rect.w
            camera_height = entity.camera.rect.h

            # Calculate the portion of the background to display
            bg_x = int(entity.camera.worldX * entity.camera.zoomLevel - camera_width / 2)
            bg_y = int(entity.camera.worldY * entity.camera.zoomLevel - camera_height / 2)

            # Clamp background position to within the image bounds
            bg_x = max(0, min(bg_x, bg_width - camera_width))
            bg_y = max(0, min(bg_y, bg_height - camera_height))

            # Create a subsurface of the background for the current camera
            cropped_background = background3.subsurface(pygame.Rect(bg_x, bg_y, camera_width, camera_height))

            # Scale the cropped background to fit the camera's zoom level
            scaled_background = pygame.transform.scale(
                cropped_background,
                (int(camera_width), int(camera_height))
            )

            # Draw the scaled background on the camera's viewport
            screen.blit(scaled_background, (entity.camera.rect.x, entity.camera.rect.y))

        # Render platforms
        for p in globals.world.platforms:
            if isinstance(p, Platform):  # Check if it's a Platform object
                # Adjust position for camera offset and zoom
                adjusted_rect = pygame.Rect(
                    (p.rect.x * entity.camera.zoomLevel) + offsetX,
                    (p.rect.y * entity.camera.zoomLevel) + offsetY,
                    p.rect.width * entity.camera.zoomLevel,
                    p.rect.height * entity.camera.zoomLevel,
                )
                pygame.draw.rect(screen, p.color, adjusted_rect)
            else:
                # Fallback for legacy Rect platforms (if any)
                pygame.draw.rect(screen, globals.MUSTARD, p)

        # Render entities and health bars/text
        for e in globals.world.entities:
            # Render entity animation
            s = e.state
            a = e.animations.animationList[s]
            a.draw(screen,
                   (e.position.rect.x * entity.camera.zoomLevel) + offsetX,
                   (e.position.rect.y * entity.camera.zoomLevel) + offsetY,
                   e.direction == 'left',
                   False,
                   entity.camera.zoomLevel)


        # Player HUD (player-specific health and lives)
        if entity.health is not None:
            utils.drawText(screen, 'Health: ' + str(entity.health.health), entity.camera.rect.x + 10,
                           entity.camera.rect.y + 50, globals.WHITE, 255)

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
        self.initial = pygame.Rect(x, y, w, h)

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
    def __init__(self, up, down, left, right, b1, b2, b3):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.b1 = b1 #currently zoom in and zoom out, can replace this with attacks and make b3 and b4 attacks or vice versa
        self.b2 = b2
        self.b3 = b3




class Platform:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)  # The geometry of the platform
        self.color = color  # The color to draw the platform

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)  # Use the color to draw the rectangle



class Intention:
    def __init__(self):
        self.moveLeft = False
        self.moveRight = False
        self.jump = False
        self.zoomIn = False
        self.zoomOut = False
        self.melee = False
        self.shoot = False
        #self.projectile = False

class Effect:
    def __init__(self, apply, timer, sound, end):
        self.apply = apply
        self.timer = timer
        self.sound = sound
        self.end = end

def resetEntity(entity):
    pass

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
        self.acceleration = 0
        self.reset = resetEntity
        self.effect = None
        self.fallingTimer = 0  # Timer to track how long the entity is falling
        self.is_attacking = False
        self.attack_timer = 0  # Time remaining before the next attack
        self.attack_cooldown = 500  # Cooldown time in milliseconds
        self.attack_damage = 10
        self.attack_range = 50
        self.target_pipe = None

