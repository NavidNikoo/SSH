import globals
import engine
import utils
import pygame

class Level:
    def __init__(self, platforms=None, entities=None, winFunc=None, loseFunc=None):
        self.platforms = platforms
        self.entities = entities
        self.winFunc = winFunc
        self.loseFunc = loseFunc

    def isWon(self):
        if self.winFunc is None:
            return False
        return self.winFunc(self)

    def isLost(self):
        if self.loseFunc is None:
            return False
        return self.loseFunc(self)

def lostLevel(level):

    # level isn't lost if any player has a life left
    for entity in level.entities:
        if entity.type == 'player':
              if entity.battle is not None:
                  if entity.battle.lives > 0:
                      return False

    #level is lost otherwise
    return True

#Temp win status: win if all collectables(food) are collected, will eventually change to when there is one man left standing
def wonLevel(level):
    #level isn't won if any collectables are left
    for entity in level.entities:
        if entity.type == 'collectable':
            return False

    #otherwise level is won
    return True


def loadLevel(levelNumber):
    if levelNumber == 1:
        globals.world = Level(
            platforms = [
                pygame.Rect(100, 300, 400, 50),
                pygame.Rect(100, 250, 50, 50),
                pygame.Rect(450, 250, 50, 50)
            ],
            entities=[
                utils.makeChicken(350, 250),
                utils.makeSushi(250, 250),
                utils.makeBurger(125, 200),
                utils.makeStrawberryCake(200, 250),
                utils.makeTaco(400, 250),
                utils.makeEnemy(150, 268),
                globals.player1
            ],
            winFunc=wonLevel,
            loseFunc=lostLevel
        )
    if levelNumber == 2:
        globals.world = Level(
            platforms=[
                pygame.Rect(100, 300, 400, 50),
            ],
            entities=[
                utils.makeTaco(400, 250),
                globals.player1
            ],
            winFunc=wonLevel,
            loseFunc=lostLevel
        )

    #reset players
    for entity in globals.world.entities:
        entity.reset(entity)