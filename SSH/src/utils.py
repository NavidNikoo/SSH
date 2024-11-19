import pygame
import globals
import engine

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

pygame.font.init()

def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)

def drawText(screen, t, x, y, fg, alpha, font_size=24):
    font = pygame.font.Font(pygame.font.get_default_font(), font_size)
    text = font.render(t, True, fg)
    text_rectangle = text.get_rect()
    text_rectangle.topleft = (x, y)

    blit_alpha(screen, text, (x,y ), alpha)

    screen.blit(text, text_rectangle)


def setHealth(entity):
    if entity.battle:
        entity.battle.lives = 3

def setInvisible(entity):
    if entity.animations:
        entity.animations.alpha = 50

def endInvisible(entity):
    if entity.animations:
        entity.animations.alpha = 255

powerups = ['health', 'invisible']

powerupImages =  {
    'health' : [pygame.image.load('assets/81_pizza.png')], #life reset to 3, change from pizza to something else later
    'invisible' : [pygame.image.load('assets/invisPotion.png')]
}

powerupSounds = {
    'health' : 'eat',
    'invisible' : 'invis'
}

powerupApply = {
    'health' : setHealth,
    'invisible' : setInvisible

}

powerupEnd = {
    'health' : None,
    'invisible' : endInvisible
}

powerupEffectTimer = {
    'health' : 0,
    'invisible' : 200
}

projectile_image = pygame.image.load('assets/bullet.png')
def makeProjectile(x, y, direction, speed=5, damage=20):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 10, 10)  # Adjust size as needed
    entity.speed = speed
    entity.direction = direction
    entity.type = 'projectile'
    entity.damage = damage

    entity.animations.add('idle', engine.Animation([projectile_image]))

    return entity



def makePowerUp(type, x, y): #more like make effect, will eventually change food systems
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 40, 40)
    entityAnimation = engine.Animation([powerupImages[type]])
    entity.animations.add('idle', entityAnimation)
    entity.effect = engine.Effect(powerupApply[type],
                                  powerupEffectTimer[type],
                                  powerupSounds[type],
                                  powerupEnd[type])
    return entity


heart_image = pygame.image.load('assets/heart.png')

Chicken = pygame.image.load('assets/86_roastedchicken_dish.png')
def makeChicken(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 32, 32)

    entityAnimation = engine.Animation([Chicken])

    entity.animations.add('idle', entityAnimation)
    entity.type = 'collectable'
    return entity

Burger = pygame.image.load('assets/15_burger.png')

def makeBurger(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 32, 32)

    entityAnimation = engine.Animation([Burger])

    entity.animations.add('idle', entityAnimation)
    entity.type = 'collectable'
    return entity

StrawberryCake = pygame.image.load('assets/91_strawberrycake_dish.png')
def makeStrawberryCake(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 32, 32)

    entityAnimation = engine.Animation([StrawberryCake])

    entity.animations.add('idle', entityAnimation)
    entity.type = 'collectable'
    return entity

Taco = pygame.image.load('assets/99_taco.png')
def makeTaco(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 32, 32)

    entityAnimation = engine.Animation([Taco])

    entity.animations.add('idle', entityAnimation)
    entity.type = 'collectable'
    return entity

Sushi = pygame.image.load('assets/97_sushi.png')
def makeSushi(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 32, 32)

    entityAnimation = engine.Animation([Sushi])
    entity.animations.add('idle', entityAnimation)
    entity.type = 'collectable'
    return entity

enemy0 = pygame.image.load('assets/hoodlum_1.png')
def makeEnemy(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 32, 32)

    entityAnimation = engine.Animation([enemy0])
    entity.animations.add('idle', entityAnimation)
    entity.type = 'dangerous'
    return entity

################################################################################################################################################
spike0 = pygame.image.load('assets/spikeleft.png')
def makeSpikeleft(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 32, 32)

    entityAnimation = engine.Animation([spike0])
    entity.animations.add('idle', entityAnimation)
    entity.type = 'dangerous'
    return entity

spike1 = pygame.image.load('assets/spikeright.png')
def makeSpikeright(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 32, 32)

    entityAnimation = engine.Animation([spike1])
    entity.animations.add('idle', entityAnimation)
    entity.type = 'dangerous'
    return entity

################################################################################################################################################
pipe = pygame.image.load('assets/pipe.png')
def makePipe(x, y, target_pipe=None):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 32, 32)
    entityAnimation = engine.Animation([pipe])
    entity.animations.add('idle', entityAnimation)
    entity.type = 'teleport'
    entity.target_pipe = target_pipe  # Assign target pipe
    return entity

pipe1 = pygame.image.load('assets/pipe1.png')

def makePipe1(x, y, target_pipe=None):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 32, 32)
    entityAnimation = engine.Animation([pipe1])
    entity.animations.add('idle', entityAnimation)
    entity.type = 'teleport'
    entity.target_pipe = target_pipe  # Assign target pipe
    return entity


pipe90d = pygame.image.load('assets/pipeAngled.png')

def makePipeAngled(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 32, 32)

    entityAnimation = engine.Animation([pipe90d])
    entity.animations.add('idle', entityAnimation)
    entity.type = 'design'
    return entity

pipe90d1 = pygame.image.load('assets/pipeAngled1.png')

def makePipeAngled1(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 32, 32)

    entityAnimation = engine.Animation([pipe90d1])
    entity.animations.add('idle', entityAnimation)
    entity.type = 'design'
    return entity

pipeStraight = pygame.image.load('assets/pipeStraight.png')

def makePipeStraight(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 32, 32)

    entityAnimation = engine.Animation([pipeStraight])
    entity.animations.add('idle', entityAnimation)
    entity.type = 'design'
    return entity

pipeStraightUp = pygame.image.load('assets/pipeStraightUp.png')

def makePipeStraightUp(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 32, 32)

    entityAnimation = engine.Animation([pipeStraightUp])
    entity.animations.add('idle', entityAnimation)
    entity.type = 'design'
    return entity

platform3 = pygame.image.load('assets/platform3.png')

def makePinkPlatform(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 32, 32)

    entityAnimation = engine.Animation([platform3])
    entity.animations.add('idle', entityAnimation)
    entity.type = 'design'
    return entity


platform4 = pygame.image.load('assets/platform4.png')

def makeGrayPlatform(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 32, 32)

    entityAnimation = engine.Animation([platform4])
    entity.animations.add('idle', entityAnimation)
    entity.type = 'design'
    return entity

################################################################################################################################################




#level select
samuraiPlaying = pygame.image.load('assets/samuraiPlaying.png')
samuraiNotPlaying = pygame.image.load('assets/samuraiNotPlaying.png')

#Idle
SamuraiIdle1 = pygame.image.load('assets/samuraiIdle_1.png')
SamuraiIdle2 = pygame.image.load('assets/samuraiIdle_2.png')
SamuraiIdle3 = pygame.image.load('assets/samuraiIdle_3.png')
SamuraiIdle4 = pygame.image.load('assets/samuraiIdle_4.png')
SamuraiIdle5 = pygame.image.load('assets/samuraiIdle_5.png')

#Run
SamuraiRun1 = pygame.image.load('assets/samuraiRun_1.png')
SamuraiRun2 = pygame.image.load('assets/samuraiRun_2.png')
SamuraiRun3 = pygame.image.load('assets/samuraiRun_3.png')
SamuraiRun4 = pygame.image.load('assets/samuraiRun_4.png')
SamuraiRun5 = pygame.image.load('assets/samuraiRun_5.png')
SamuraiRun6 = pygame.image.load('assets/samuraiRun_6.png')
SamuraiRun7 = pygame.image.load('assets/samuraiRun_7.png')
SamuraiRun8 = pygame.image.load('assets/samuraiRun_8.png')

SamuraiMelee1 = pygame.image.load('assets/SamuraiMelee1.png')
SamuraiMelee2 = pygame.image.load('assets/SamuraiMelee2.png')
SamuraiMelee3 = pygame.image.load('assets/SamuraiMelee3.png')
SamuraiMelee4 = pygame.image.load('assets/SamuraiMelee4.png')
SamuraiMelee5 = pygame.image.load('assets/SamuraiMelee5.png')

def setPlayerCameras():

    #1 player game
    if len(globals.players) == 1:

        p = globals.players[0]
        p.camera = engine.Camera(10, 10, 810, 810)
        p.camera.setWorldPos(p.position.initial.x, p.position.initial.y)
        p.camera.trackEntity(p)

    #2 player game
    if len(globals.players) == 2:

        p1 = globals.players[0]
        p1.camera = engine.Camera(10, 10, 400, 810)
        p1.camera.setWorldPos(p1.position.initial.x, p1.position.initial.y)
        p1.camera.trackEntity(p1)

        p2 = globals.players[1]
        p2.camera = engine.Camera(420, 10, 400, 810)
        p2.camera.setWorldPos(p2.position.initial.x, p2.position.initial.y)
        p2.camera.trackEntity(p2)

    #3 or 4 player game
    if len(globals.players) >= 3:

        p1 = globals.players[0]
        p1.camera = engine.Camera(10, 10, 400, 400)
        p1.camera.setWorldPos(p1.position.initial.x, p1.position.initial.y)
        p1.camera.trackEntity(p1)

        p2 = globals.players[1]
        p2.camera = engine.Camera(420, 10, 400, 400)
        p2.camera.setWorldPos(p2.position.initial.x, p2.position.initial.y)
        p2.camera.trackEntity(p2)

        p3 = globals.players[2]
        p3.camera = engine.Camera(10, 420, 400, 400)
        p3.camera.setWorldPos(p3.position.initial.x, p3.position.initial.y)
        p3.camera.trackEntity(p3)

        if len(globals.players) == 4:
            p4 = globals.players[3]
            p4.camera = engine.Camera(420, 420, 400, 400)
            p4.camera.setWorldPos(p4.position.initial.x, p4.position.initial.y)
            p4.camera.trackEntity(p4)


def resetPlayer(entity):
    entity.health.health = 200
    entity.battle.lives = 3
    entity.position.rect.x = entity.position.initial.x
    entity.position.rect.y = entity.position.initial.y
    entity.speed = 0
    entity.acceleration= 0.2
    entity.camera.setWorldPos(entity.position.initial.x, entity.position.initial.y)
    entity.direction = 'right'
    entity.animations.alpha = 255
    entity.effect = None

def makePlayer(x, y): #makeSamurai
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 22, 35)
    entityIdleAnimation = engine.Animation([SamuraiIdle1, SamuraiIdle2, SamuraiIdle3, SamuraiIdle4, SamuraiIdle5])
    entityRunAnimation = engine.Animation([SamuraiRun1, SamuraiRun2, SamuraiRun3, SamuraiRun4, SamuraiRun5, SamuraiRun6, SamuraiRun7, SamuraiRun8])
    entityAttackAnimation = engine.Animation([SamuraiMelee1, SamuraiMelee2, SamuraiMelee3, SamuraiMelee4, SamuraiMelee5])
    entity.animations.add('idle', entityIdleAnimation)
    entity.animations.add('walking', entityRunAnimation)
    entity.animations.add('melee', entityAttackAnimation)
    entity.health = engine.Health()
    entity.battle = engine.Battle()
    entity.intention = engine.Intention()
    entity.acceleration = 0.2
    entity.type = 'player'
    entity.reset = resetPlayer
    return entity

#makeSorcerer
