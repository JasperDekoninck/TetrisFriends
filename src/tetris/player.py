from .board import Board
from .side_board import SideBoard
from .button import TextButton
from .constants import *
import time


class Player:
    def __init__(self, base_pos, size_per_block):
        self.pos = base_pos
        self.board = Board(self, size_per_block, base_pos)
        self.size_per_block = size_per_block
        self.size_square = 3 * self.size_per_block
        self.size_per_block_side_board = self.size_per_block - 10
        self.sideboard = SideBoard(self.size_per_block_side_board, self.board)
        self.death = False
        self.points = 0
        self.lines = 0
        self.pressed_times = 6 * [time.time()]
        self.time_between_movements = 0.13
        self.time_between_turns = 0.2
        self.points_message = TextButton([0, 0], "Points: {}".format(self.points), size=40,
                                         color_not_selected=pygame.Color("white"))
        self.points_message.pos = [self.pos[0], self.pos[1] - self.points_message.size[1] - 10]

    def get_next_tetromino(self):
        return self.sideboard.get_next_tetromino()

    def draw_points(self, screen):
        self.points_message.set_text("Points: {}".format(self.points))
        self.points_message.render(screen)

    def draw(self, screen):
        self.board.draw(screen)
        self.sideboard.draw(screen, self.size_square)
        self.draw_points(screen)

    def move_tetromino(self, left=False, right=False, down=False):
        if self.board.moving_tetromino is not None:
            if left and time.time() - self.pressed_times[0] > self.time_between_movements:
                self.pressed_times[0] = time.time()
                self.board.move(left=True)
            elif right and time.time() - self.pressed_times[1] > self.time_between_movements:
                self.pressed_times[1] = time.time()
                self.board.move(right=True)
            elif down and time.time() - self.pressed_times[2] > self.time_between_movements:
                self.pressed_times[2] = time.time()
                self.board.move(down=True)

    def turn_tetromino(self):
        if time.time() - self.pressed_times[3] > self.time_between_turns:
            self.board.turn()
            self.pressed_times[3] = time.time()

    def move_completely_down(self):
        if time.time() - self.pressed_times[4] > self.time_between_turns:
            self.pressed_times[4] = time.time()
            self.board.move_completely_down()

    def hold_block(self):
        if time.time() - self.pressed_times[5] > self.time_between_turns:
            self.pressed_times[5] = time.time()
            self.sideboard.set_hold_tetromino(self.board.moving_tetromino)

    def update(self, down=True):
        self.board.update(down)