import globals
import engine
import utils
import pygame

class Level:
    def __init__(self, platforms=None, entities=None, winFunc=None, loseFunc=None, powerupSpawnPoints=None, winner=None,losers=None):
        self.platforms = platforms
        self.entities = entities
        self.winFunc = winFunc
        self.loseFunc = loseFunc
        self.powerUpSpawnPoints = powerupSpawnPoints
        self.winner = winner
        self.losers = losers
        self.hasStarted = False  # New flag

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
    # Check if any collectables are left
    collectables_remaining = any(entity.type == 'collectable' for entity in level.entities)

    # Check how many players are still alive
    alive_players = [entity for entity in level.entities if entity.type == 'player' and entity.battle.lives > 0]

    # Only trigger win logic after the game has started
    if not level.hasStarted:
        return False

    # Case 1: Single player starts game and collects all items
    if len(alive_players) == 1 and collectables_remaining:
        return False
    if len(alive_players) == 1 and not collectables_remaining:
        level.winner = alive_players[0]
        return True

    # Case 2: Multiplayer game - Win when only one player is left
    if len(alive_players) == 1 and level.hasStarted:
        level.winner = alive_players[0]
        level.losers = [entity for entity in level.entities if entity.type == 'player' and entity not in alive_players]
        return True

    # No win detected
    return False





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
                utils.makeChicken(350, 880),
                utils.makeBurger(400, 880),
                utils.makeTaco(600, 880),
                utils.makeStrawberryCake(700, 880),
                utils.makeSushi(830, 880),
                utils.makeEnemy(800, 880),
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
                utils.makeSushi(320, 680),
                utils.makeBurger(500, 750),
                utils.makeChicken(250, 650),

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
                utils.makeChicken(400, 800),  # Adjusted collectible height
                utils.makeTaco(475, 705),  # Adjusted to match the central platform
                utils.makeBurger(375, 660),  # Adjusted to match the left small platform
                utils.makeStrawberryCake(575, 660),  # Adjusted to match the right small platform
                utils.makeSushi(280, 895),


                # Decorative pink platforms
                utils.makePinkPlatform(275, 890),  # Pink platforms
                utils.makePinkPlatform((275 + 176), 890),
                utils.makePinkPlatform((275 + (176 * 2)), 890),
                utils.makePinkPlatform((275 + (176 * 3)), 890),

                utils.makeEnemy1(800, 735)
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

