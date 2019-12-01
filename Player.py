from Board import Board
from SideBoard import SideBoard
import time


class Player:
    def __init__(self, base_pos, size_per_block):
        self.pos = base_pos
        self.board = Board(self, size_per_block, base_pos)
        self.size_per_block = size_per_block
        self.size_square = 3 * self.size_per_block
        self.size_per_block_side_board = self.size_per_block - 5
        self.sideboard = SideBoard(self.size_per_block_side_board, self.board)
        self.death = False
        self.points = 0
        self.pressed_times = 6 * [time.time()]
        self.time_between_movements = 0.13
        self.time_between_turns = 0.2


    def get_next_block(self):
        return self.sideboard.get_next_block()

    def draw(self, screen):
        self.board.draw(screen)
        self.sideboard.draw(screen, self.pos, (self.pos[0] + self.board.X_SIZE * self.size_per_block, self.pos[1]),
                            self.size_square)

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
            self.board.moving_tetromino.turn()
            self.pressed_times[3] = time.time()

    def move_completely_down(self):
        if time.time() - self.pressed_times[4] > self.time_between_turns:
            self.pressed_times[4] = time.time()
            self.board.move_completely_down()

    def hold_block(self):
        if time.time() - self.pressed_times[5] > self.time_between_turns:
            self.pressed_times[5] = time.time()
            self.sideboard.set_hold_block(self.board.moving_tetromino)
            if self.board.moving_tetromino is None:
                self.board.moving_tetromino = self.get_next_block()

    def update(self, down=True):
        self.board.update(down)
