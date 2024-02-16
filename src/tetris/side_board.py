from .tetronimo import *
from .button import TextButton
import pygame
import numpy as np
pygame.init()


class SideBoard:
    """
    Everything that has to do with things around the game board
    """
    # Place of tetrominos on specific index
    PLACE_TETROMINOS = [2, 2]

    def __init__(self, size_per_block, board):
        """
        :param size_per_block: size per block for the display of the upcoming tetrominos and the hold tetronimo
        :param board: Board, the board with which this SideBoard is associated
        """
        self.hold_tetromino = None
        self.board = board

        self.next_tetrominos = [
            np.random.choice(POSSIBLE_TETROMINOS)(self.PLACE_TETROMINOS, self) for _ in range(N_NEXT_TETROMINOS)
        ]

        self.hold_button = TextButton((0, 0), "HOLD", 30, pygame.Color("white"))
        self.next_button = TextButton((0, 0), "NEXT", 30, pygame.Color("white"))

        self.left_top_position = (0, 0)
        self.size_per_block = size_per_block

    @staticmethod
    def is_valid_tetromino(tetromino):
        """
        Checks whether or not a given tetromino is valid.
        Note: normally this function is not necessary.
        :param tetromino: A tetromino
        """
        return True

    def get_next_tetromino(self):
        """
        Returns the next tetromino on the list of next_tetrominos and adds a new one to them
        :return: Tetromino
        """
        next_block = self.next_tetrominos[0]
        self.next_tetrominos = self.next_tetrominos[1:] + [np.random.choice(POSSIBLE_TETROMINOS)([2, 2], self)]
        next_block.board = self.board
        return next_block

    def set_hold_tetromino(self, new_tetromino):
        """
        Sets the hold tetromino to the new tetromino and sets the moving tetromino of the board to the tetromino
        in hold.
        :param new_tetromino: Tetromino, the new tetromino to set in the hold tetromino
        """
        if new_tetromino is not None and new_tetromino.holdable:
            if self.hold_tetromino is not None:
                self.hold_tetromino.board = self.board
                self.board.new_moving_tetromino(self.hold_tetromino)
            else:
                self.board.moving_tetromino = None
            self.hold_tetromino = new_tetromino
            self.hold_tetromino.coordinate = self.PLACE_TETROMINOS

            self.hold_tetromino.board = self
            self.hold_tetromino.holdable = False

    def coordinate_to_position(self, coordinate):
        """
        Converts a coordinate ot a position on the screen.
        :param coordinate: Tuple of ints, The coordinate on the board
        :return: List of ints, The position on the screen
        """
        return [self.left_top_position[0] + self.size_per_block * coordinate[0],
                self.left_top_position[1] + self.size_per_block * coordinate[1]]

    def draw_hold_tetromino(self, screen, size_square):
        self.left_top_position = [self.board.left_top_position[0] - self.hold_button.size[0] - 10,
                                  self.board.left_top_position[1]]

        self.hold_button.render(screen, self.left_top_position)

        self.left_top_position[1] += self.hold_button.size[1] + 10
        pygame.draw.rect(screen, COLORS["darkest grey"], tuple(self.left_top_position) + (size_square, size_square))

        if self.hold_tetromino is not None:
            self.hold_tetromino.draw(screen, self.size_per_block)

    def draw_next_tetromino(self, screen, size_square):
        self.left_top_position = [self.board.left_top_position[0] + X_SIZE * self.board.size_per_block + 10,
                                  self.board.left_top_position[1]]

        self.next_button.render(screen, self.left_top_position)

        pos_next = [self.left_top_position[0], self.left_top_position[1] + self.next_button.size[1]]

        for i in range(N_NEXT_TETROMINOS):
            pos_next[1] = self.left_top_position[1] + size_square
            self.left_top_position = pos_next
            self.next_tetrominos[i].draw(screen, self.size_per_block)

    def draw(self, screen, size_square):
        """
        Draws the side board on screen
        :param screen: pygame screen, screen on which to display the side board
        :param size_square: The size of one square, the bounding box for one tetromino
        :return:
        """
        self.draw_hold_tetromino(screen, size_square)
        self.draw_next_tetromino(screen, size_square)
