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
                engine.Platform(275, 900, 700, 50, globals.DARK_GRAY), # main platform
                engine.Platform(300, 950, 50, 400, globals.LIGHT_GRAY), #pillars
                engine.Platform(400, 950, 50, 400, globals.LIGHT_GRAY),
                engine.Platform(500, 950, 50, 400, globals.LIGHT_GRAY),
                engine.Platform(600, 950, 50, 400, globals.LIGHT_GRAY),
                engine.Platform(700, 950, 50, 400, globals.LIGHT_GRAY),
                engine.Platform(800, 950, 50, 400, globals.LIGHT_GRAY),
                engine.Platform(900, 950, 50, 400, globals.LIGHT_GRAY),
                engine.Platform(275, 800, 10, 100, globals.BLACK), #left wall
                engine.Platform(960, 800, 10, 100, globals.BLACK),  # right wall
                engine.Platform(-100, 1350, 4000, 10, globals.LIGHT_GRAY),  # lowest floor
                #engine.Platform(800, 950, 50, 400, globals.LIGHT_GRAY),
                #pygame.Rect(450, 250, 50, 50)
            ],
            entities=[
                utils.makeChicken(350, 250),
                #utils.makeSushi(250, 250),
                #utils.makeBurger(125, 200),
                #utils.makeStrawberryCake(200, 250),
                #utils.makeTaco(400, 250),
                #utils.makeEnemy(150, 268),
                utils.makeSpikeleft(280, 800),
                utils.makeSpikeleft(280, 825),
                utils.makeSpikeleft(280, 850),
                utils.makeSpikeleft(280, 875),
                utils.makeSpikeleft(280, 890),
                utils.makeSpikeright(950, 800),
                utils.makeSpikeright(950, 830),
                utils.makeSpikeright(950, 845),
                utils.makeSpikeright(950, 875),
                utils.makeSpikeright(950, 890),

                #utils.makePowerUp('invisible' ,400, 260)
            ],
            winFunc=wonLevel,
            loseFunc=lostLevel,

        )

    if levelNumber == 2:
        globals.world = Level(
            platforms=[
                # Tree Stem (Trunk)
                engine.Platform(350, 950, 100, 300, globals.BROWN),  # Main tree trunk base (shifted further down)
                engine.Platform(375, 750, 50, 200, globals.BROWN),  # Narrow upper trunk (shifted further down)

                # Main Branches (Green Platforms)

                engine.Platform(300, 700, 150, 30, globals.GREEN),  # Lower-left branch (shifted further down)
                engine.Platform(450, 700, 150, 30, globals.GREEN),  # Lower-right branch (shifted further down)

                # Additional Branches
                engine.Platform(200, 640, 100, 20, globals.GREEN),  # Far left branch (shifted further down)
                engine.Platform(550, 665, 100, 20, globals.GREEN),  # Far right branch (shifted further down)
                engine.Platform(375, 600, 50, 20, globals.GREEN),  # Center branch above trunk (shifted further down)

                # Leaves as Top Platforms
                engine.Platform(250, 600, 150, 30, globals.GREEN),  # Top-left leaves (shifted further down)
                engine.Platform(400, 600, 200, 30, globals.GREEN),  # Top-right leaves (shifted further down)

                # Small Platforms for Combat Movement
                engine.Platform(325, 540, 50, 20, globals.GREEN),
                # Tiny left branch for maneuvering (shifted further down)
                engine.Platform(425, 540, 50, 20, globals.GREEN),
                # Tiny right branch for maneuvering (shifted further down)

                # Hidden Tubes (Teleport Locations)
                #engine.Platform(200, 950, 26, 31, globals.BROWN),  # Teleport tube (left, shifted further down)
                engine.Platform(600, 950, 27, 32, globals.BROWN),  # Teleport tube (right, shifted further down)

                # Tube Exit Platforms
                engine.Platform(200, 500, 50, 20, globals.MUSTARD),  # Exit from left tube (shifted further down)
                engine.Platform(600, 500, 50, 20, globals.MUSTARD),  # Exit from right tube (shifted further down)
                engine.Platform(635, 470, 32, 27, globals.BROWN),  #pipe

                engine.Platform(137, 977, 32, 27, globals.BROWN),  # straight Pipe
                engine.Platform(130, 977, 32, 27, globals.BROWN),  # straight Pipe
                engine.Platform(105, 977, 30, 25, globals.BROWN),  # Pipe

            ],
        entities=[
                utils.makeTaco(160, 210),
                utils.makePipe(200, 950),
                utils.makePipeAngled(169, 982),
                utils.makePipeStraight(137,977),
                utils.makePipeStraight(105, 977),
                utils.makePipeAngled1(90, 977),
                utils.makePipeStraightUp(90, 1000),
                utils.makePipeStraightUp(90, 1032),
                utils.makePipeStraightUp(90, 1064),
                utils.makePipeStraightUp(90, 1096),
                utils.makePipeStraightUp(90, 1128),
                utils.makePipeStraightUp(90, 1160),
                utils.makePipeStraightUp(90, 1192),
                utils.makePipeStraightUp(90, (1192 + (32 * 1))),
                utils.makePipeStraightUp(90, (1192 + (32 * 2))),
                utils.makePipeStraightUp(90, (1192 + (32 * 3))),
                utils.makePipeStraightUp(90, (1192 + (32 * 4))),
                utils.makePipeStraightUp(90, (1192 + (32 * 5))),
                utils.makePipeStraightUp(90, (1192 + (32 * 6))),
                utils.makePipe1(640, 470), #top right pipe
                utils.makePipeStraight(667,470),
                utils.makePipeStraight(694, 470),
                utils.makePipeStraight(721, 470),
                utils.makePipeStraight(748, 470),
                utils.makePipeStraight(775, 470),
                utils.makePipeStraight(802, 470),
            ],
            winFunc=wonLevel,
            loseFunc=lostLevel,
        )

    if levelNumber == 3:
        globals.world = Level(
            platforms=[
                pygame.Rect(100, 300, 400, 50),
            ],
            entities=[
                utils.makeChicken(400, 50)
            ],
            winFunc=wonLevel,
            loseFunc=lostLevel
        )

    #add players
    for player in globals.players:
        globals.world.entities.append(player)

    #reset players
    for entity in globals.world.entities:
        entity.reset(entity)

