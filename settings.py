# Game options/Settings
TITLE = 'Jumpy !'
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'
HS_FILE = 'highscore.txt'
SPRITESHEET = 'spritesheet_jumper.png'
SCALE = 0.5
VOLUME = 0.1

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.8
PLAYER_JUMP = 20

# Game properties
BOOST_POWER = 60
POW_SPAWN_PCT = 7
MOB_FREQ = 5000
PLAYER_LAYER = 1
PLATFORM_LAYER = 2
CLOUD_LAYER = 0
POWERUP_LAYER = 1
MOB_LAYER = 2

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 60),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4),
                 (125, HEIGHT - 350),
                 (350, 200),
                 (175, 100)]

# Define usefull colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 25)
YELLOW = (255, 255, 0)
# LIGHTBLUE = (0, 155, 155)
LIGHTBLUE = (51, 153, 255)
BGCOLOR = LIGHTBLUE
