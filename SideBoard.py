from Block import *
from Button import TextButton
import pygame
import numpy as np
pygame.init()


class SideBoard:
    POSSIBLE_BLOCKS = [HorseLeft, HorseRight, TetrisBlock, Square, Stick, LeftTurn, RightTurn]
    N_NEXT_BLOCKS = 5

    def __init__(self, size_per_block, board):
        self.hold_block = None
        self.board = board

        self.next_blocks = [
            np.random.choice(self.POSSIBLE_BLOCKS)([2, 2], self) for _ in range(self.N_NEXT_BLOCKS)
        ]

        self.hold_button = TextButton((0, 0), "HOLD", 20, pygame.Color("white"))
        self.next_button = TextButton((0, 0), "NEXT", 20, pygame.Color("white"))

        self.left_top_position = (0, 0)
        self.size_per_block = size_per_block

    @staticmethod
    def is_valid_tetromino(tetromino):
        return True

    def get_next_block(self):
        next_block = self.next_blocks[0]
        self.next_blocks = self.next_blocks[1:] + [np.random.choice(self.POSSIBLE_BLOCKS)([2, 2], self)]
        next_block.board = self.board
        return next_block

    def set_hold_block(self, new_block):
        old_hold_block = self.hold_block
        self.hold_block = new_block
        self.hold_block.coordinate = [2, 2]
        if old_hold_block is not None:
            old_hold_block.board = self.board
            self.board.new_moving_tetromino(old_hold_block)
        else:
            self.board.moving_tetromino = None
        self.hold_block.board = self

    def coordinate_to_position(self, coordinate):
        return [self.left_top_position[0] + self.size_per_block * coordinate[0],
                self.left_top_position[1] + self.size_per_block * coordinate[1]]

    def draw(self, screen, right_top_position_1, left_top_position_2, size_square):
        self.hold_button.pos = (right_top_position_1[0] - 10 - self.hold_button.size[0], right_top_position_1[1])
        self.next_button.pos = (left_top_position_2[0] + 10 + self.next_button.size[0], left_top_position_2[1])

        self.hold_button.render(screen)
        self.next_button.render(screen)

        pos_hold = (right_top_position_1[0] - size_square, right_top_position_1[1] + self.hold_button.size[1])
        pygame.draw.rect(screen, pygame.Color("black"), pos_hold + (size_square, size_square))

        self.left_top_position = [right_top_position_1[0] - size_square, right_top_position_1[1]]
        if self.hold_block is not None:
            self.hold_block.draw(screen, self.size_per_block)

        pos_next = [left_top_position_2[0], left_top_position_2[1] + self.next_button.size[1]]

        for i in range(self.N_NEXT_BLOCKS):
            pos_next[1] = left_top_position_2[1] + self.next_button.size[1] + i * size_square
            self.left_top_position = pos_next
            self.next_blocks[i].draw(screen, self.size_per_block)
