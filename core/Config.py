import math
import pygame

######################################
## ALL CONSTANT VARIABLES ARE BELOW ##
######################################

# Windows
WIN_WIDTH = 1920
WIN_HEIGHT = 1080
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
FRAME_RATE = 60

# Tiles
TILE_SIZE = 15
TILE_COLOR = (220, 220, 170)
TILE_HEIGHT_UNIT = 60

# Noise
NOISE_SEED = 5
NOISE_SCALE = 100.0
NOISE_OCTAVES = 6
NOISE_PERSISTENCE = 0.5
NOISE_LACUNARITY = 2.0

# Light
MIN_LIGHT_INTENSITY = 0.2
MAX_LIGHT_INTENSITY = 1
LIGHT_TRANSITION_RANGE = math.pi / 0.6 # The transition range of light
LIGHT_POS = (960, -5000)
DAY_PERIOD = 0.5 # minute