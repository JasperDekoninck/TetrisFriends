import pygame
import os
pygame.init()

# IMAGE CONSTANTS
LIGHTBLUE_BLOCK = pygame.image.load(os.path.join("images", "lightblue.jpg"))
DARKBLUE_BLOCK = pygame.image.load(os.path.join("images", "darkblue.jpg"))
GREY_BLOCK = pygame.image.load(os.path.join("images", "grey.jpg"))
GREEN_BLOCK = pygame.image.load(os.path.join("images", "green.jpg"))
ORANGE_BLOCK = pygame.image.load(os.path.join("images", "orange.jpg"))
PURPLE_BLOCK = pygame.image.load(os.path.join("images", "purple.jpg"))
RED_BLOCK = pygame.image.load(os.path.join("images", "red.jpg"))
YELLOW_BLOCK = pygame.image.load(os.path.join("images", "yellow.jpg"))

# BOARD CONSTANTS
X_SIZE = 10
Y_SIZE = 20
COLORS = {
    "darkest grey": (36, 36, 36),
    "darker grey": (43, 43, 43),
    "dark grey": (46, 46, 46),
    "light grey": (95, 105, 104)
}

# SIDE BOARD CONSTANTS
N_NEXT_TETROMINOS = 5

class SINGLEPLAYERCONSTANTS:
    SIZE_PER_BLOCK = 20
    DOWN_PER_SECOND = 3