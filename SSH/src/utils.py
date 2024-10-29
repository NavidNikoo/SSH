import pygame
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
font = pygame.font.Font(pygame.font.get_default_font(), 24)


def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)

def drawText(screen, t, x, y, fg, alpha):
    text = font.render(t,True, fg)
    text_rectangle = text.get_rect()
    text_rectangle.topleft = (x, y)

    blit_alpha(screen, text, (x,y ), alpha)

    screen.blit(text, text_rectangle)

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





