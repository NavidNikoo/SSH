import pygame
import engine

Chicken = pygame.image.load('assets/86_roastedchicken_dish.png')
Burger = pygame.image.load('assets/15_burger.png')
StrawberryCake = pygame.image.load('assets/91_strawberrycake_dish.png')
Taco = pygame.image.load('assets/99_taco.png')
Sushi = pygame.image.load('assets/97_sushi.png')

def makeChicken(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 32, 32)

    entityAnimation = engine.Animation([Chicken])

    entity.animations.add('idle', entityAnimation)
    entity.type = 'collectable'
    return entity

def makeBurger(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 32, 32)

    entityAnimation = engine.Animation([Burger])

    entity.animations.add('idle', entityAnimation)
    entity.type = 'collectable'
    return entity

def makeStrawberryCake(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 32, 32)

    entityAnimation = engine.Animation([StrawberryCake])

    entity.animations.add('idle', entityAnimation)
    entity.type = 'collectable'
    return entity

def makeTaco(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 32, 32)

    entityAnimation = engine.Animation([Taco])

    entity.animations.add('idle', entityAnimation)
    entity.type = 'collectable'
    return entity

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

SamuraiIdle1 = pygame.image.load('assets/samuraiIdle_1.png')
SamuraiIdle2 = pygame.image.load('assets/samuraiIdle_2.png')
SamuraiIdle3 = pygame.image.load('assets/samuraiIdle_3.png')
SamuraiIdle4 = pygame.image.load('assets/samuraiIdle_4.png')
SamuraiIdle5 = pygame.image.load('assets/samuraiIdle_5.png')

SamuraiRun1 = pygame.image.load('assets/samuraiRun_1.png')
SamuraiRun2 = pygame.image.load('assets/samuraiRun_2.png')
SamuraiRun3 = pygame.image.load('assets/samuraiRun_3.png')
SamuraiRun4 = pygame.image.load('assets/samuraiRun_4.png')
SamuraiRun5 = pygame.image.load('assets/samuraiRun_5.png')
SamuraiRun6 = pygame.image.load('assets/samuraiRun_6.png')
SamuraiRun7 = pygame.image.load('assets/samuraiRun_7.png')
SamuraiRun8 = pygame.image.load('assets/samuraiRun_8.png')

def makePlayer(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 22, 35)
    entityIdleAnimation = engine.Animation([SamuraiIdle1, SamuraiIdle2, SamuraiIdle3, SamuraiIdle4, SamuraiIdle5])
    entityRunAnimation = engine.Animation([SamuraiRun1, SamuraiRun2, SamuraiRun3, SamuraiRun4, SamuraiRun5, SamuraiRun6, SamuraiRun7, SamuraiRun8])
    entity.animations.add('idle', entityIdleAnimation)
    entity.animations.add('walking', entityRunAnimation)
    entity.type = 'player'
    return entity





