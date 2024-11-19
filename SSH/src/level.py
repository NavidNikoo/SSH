import globals
import engine
import utils
import pygame

class Level:
    def __init__(self, platforms=None, entities=None, winFunc=None, loseFunc=None, powerupSpawnPoints=None):
        self.platforms = platforms
        self.entities = entities
        self.winFunc = winFunc
        self.loseFunc = loseFunc
        self.powerUpSpawnPoints = powerupSpawnPoints

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
                #engine.Platform(-100, 1350, 4000, 10, globals.LIGHT_GRAY),  # lowest floor
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
                utils.makeGrayPlatform(275, 900),
                utils.makeGrayPlatform(275 + 176, 900),
                utils.makeGrayPlatform(275 + (176 * 2), 900),
                utils.makeGrayPlatform(275 + (176 * 3), 900),
                #utils.makePowerUp('health' ,400, 260)
            ],
            winFunc=wonLevel,
            loseFunc=lostLevel,
            #powerupSpawnPoints=[(400, 260), (300, 100)]

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


                engine.Platform(137, 977, 32, 27, globals.BROWN),  # straight Pipe
                engine.Platform(130, 977, 50, 27, globals.BROWN),  # straight Pipe
                engine.Platform(105, 977, 30, 25, globals.BROWN),  # Pipe

                engine.Platform(90, 977 , 32, 100, globals.BROWN),

            ],
        entities=[
                utils.makeTaco(160, 210),
                utils.makePipe(200, 950),
                utils.makePipeAngled(169, 982),
                utils.makePipeStraight(137,977),
                utils.makePipeStraight(105, 977),
                utils.makePipeAngled1(90, 977),
                utils.makePipeStraightUp(90, 1000),



            ],
            winFunc=wonLevel,
            loseFunc=lostLevel,
        )

    if levelNumber == 3:
        globals.world = Level(
            platforms=[
                # Main platform
                engine.Platform(275, 890, 700, 50, globals.DARK_GRAY),

                # Floating Platforms
                engine.Platform(375, 820, 150, 20, globals.PINK),  # Left floating platform
                engine.Platform(575, 820, 150, 20, globals.PINK),  # Right floating platform
                engine.Platform(475, 720, 150, 20, globals.PINK),  # Central floating platform

                # Smaller Floating Platforms
                engine.Platform(400, 670, 100, 15, globals.LIGHT_GRAY),  # Left small platform
                engine.Platform(550, 670, 100, 15, globals.LIGHT_GRAY),  # Right small platform

                # Intermediate Platforms
                engine.Platform(350, 760, 100, 15, globals.LIGHT_GRAY),  # Left intermediate platform
                engine.Platform(600, 760, 100, 15, globals.LIGHT_GRAY),  # Right intermediate platform
            ],
            entities=[
                # Adding collectibles for engagement
                utils.makeChicken(400, 40),  # Adjusted collectible height
                utils.makeTaco(475, 705),  # Adjusted to match the central platform
                utils.makeBurger(375, 660),  # Adjusted to match the left small platform
                utils.makeStrawberryCake(575, 660),  # Adjusted to match the right small platform

                # Decorative pink platforms
                utils.makePinkPlatform(275, 890),  # Pink platforms
                utils.makePinkPlatform((275 + 176), 890),
                utils.makePinkPlatform((275 + (176 * 2)), 890),
                utils.makePinkPlatform((275 + (176 * 3)), 890)
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

