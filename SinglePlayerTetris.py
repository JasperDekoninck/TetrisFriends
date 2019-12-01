from Player import Player
from Board import Board
import pygame
import time
pygame.init()


class SinglePlayerTetris:
    SIZE_PER_BLOCK = 20
    DOWN_PER_SECOND = 3

    def __init__(self, screen, screen_size):
        self.screen = screen
        self.screen_size = screen_size
        self.player = Player((self.screen_size[0] // 2 - Board.X_SIZE * self.SIZE_PER_BLOCK // 2, 100),
                             self.SIZE_PER_BLOCK)
        self.time_since_moving_down = time.time()

    def play(self):
        while True:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            if time.time() - self.time_since_moving_down > 1 / self.DOWN_PER_SECOND:
                self.player.update(down=True)
                self.time_since_moving_down = time.time()
            else:
                self.player.update(down=False)

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