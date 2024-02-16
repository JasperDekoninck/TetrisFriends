from .player import Player
from .constants import *
import pygame
import time
import numpy as np
pygame.init()


class SinglePlayerTetris:
    def __init__(self, screen, screen_size):
        self.screen = screen
        self.screen_size = screen_size
        self.player = Player((self.screen_size[0] // 2 - X_SIZE * SINGLEPLAYERCONSTANTS.SIZE_PER_BLOCK // 2, 100),
                             SINGLEPLAYERCONSTANTS.SIZE_PER_BLOCK)
        self.time_since_moving_down = time.time()

    def speed_up(self, lines):
        return np.log(lines / 5 + np.e)

    def reset(self):
        self.player = Player((self.screen_size[0] // 2 - X_SIZE * SINGLEPLAYERCONSTANTS.SIZE_PER_BLOCK // 2, 100),
                             SINGLEPLAYERCONSTANTS.SIZE_PER_BLOCK)

    def loop(self, *args):
        while True:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            if time.time() - self.time_since_moving_down > \
                    1 / (SINGLEPLAYERCONSTANTS.DOWN_PER_SECOND * self.speed_up(self.player.lines)):
                self.player.update(down=True)
                self.time_since_moving_down = time.time()

            if self.player.death:
                return "game over", self.player.points

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move_tetromino(left=True)
            elif keys[pygame.K_RIGHT]:
                self.player.move_tetromino(right=True)
            elif keys[pygame.K_DOWN]:
                self.player.move_tetromino(down=True)
            elif keys[pygame.K_UP]:
                self.player.turn_tetromino()
            elif keys[pygame.K_SPACE]:
                self.player.move_completely_down()
            elif keys[pygame.K_c]:
                self.player.hold_block()

            self.player.draw(self.screen)

            pygame.display.update()