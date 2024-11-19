import soundmanager

#Define color constants for use in the GUI
#For custom colors, go to color picker on google and find the tuple and use it, make it a constant if you want
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)
BROWN = (150, 75, 0)  # A common shade of brown
WHITE = (250, 250, 250)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
MUSTARD = (209, 206, 25)

player1 = None
player2 = None
player3 = None
player4 = None
players = []

# Set screen size parameters
SCREEN_WIDTH = 830  # Width of the application window
SCREEN_HEIGHT = 830  # Height of the application window

world = None

maxLevel = 3
lastCompletedLevel = 1
currentLevel = 1


soundManager = soundmanager.SoundManager()
