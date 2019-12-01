from Block import *
import pygame
pygame.init()


class Board:

    X_SIZE = 10
    Y_SIZE = 20
    COLORS = {
        "darkest grey": (36, 36, 36),
        "darker grey": (43, 43, 43),
        "dark grey": (46, 46, 46),
        "light grey": (95, 105, 104)
    }

    def __init__(self, player, size_per_block, left_top_position):
        self.player = player
        self.size_per_block = size_per_block
        self.left_top_position = left_top_position
        self.moving_tetromino = None

        self.blocks_in_game = []

        self.board = [[0 for _ in range(self.X_SIZE)] for _ in range(self.Y_SIZE)]

    def is_valid_tetromino(self, tetromino):
        for co in tetromino.get_all_coordinates():
            if 0 > co[0] or co[0] > self.X_SIZE - 1 or 0 > co[1] or co[1] > self.Y_SIZE - 1 or \
                    (self.board[co[1]][co[0]] != 0 and self.board[co[1]][co[0]] != tetromino):
                return False
        return True

    def coordinate_to_position(self, coordinate):
        return [self.left_top_position[0] + self.size_per_block * coordinate[0],
                self.left_top_position[1] + self.size_per_block * coordinate[1]]

    def new_moving_tetromino(self, next_tetromino):
        self.moving_tetromino = next_tetromino
        self.moving_tetromino.coordinate = [int(self.X_SIZE / 2),
                                            -min([min(co) for co in self.moving_tetromino.shape])]

        if not self.is_valid_tetromino(self.moving_tetromino):
            self.player.death = True

    def regenerate_board(self):
        self.board = [[0 for _ in range(self.X_SIZE)] for _ in range(self.Y_SIZE)]
        for co in self.moving_tetromino.get_all_coordinates():
            self.board[co[1]][co[0]] = self.moving_tetromino

        for block in self.blocks_in_game:
            self.board[block.coordinate[1]][block.coordinate[0]] = block

    def move_down(self):
        if self.moving_tetromino.possible_to_move(down=True):
            self.moving_tetromino.move(down=True)
        else:
            for co in self.moving_tetromino.get_all_coordinates():
                self.blocks_in_game.append(SmallBlock(co, self.moving_tetromino.image, self))
            self.moving_tetromino = None

    def move(self, left=False, right=False, down=False):
        if self.moving_tetromino is not None and self.moving_tetromino.possible_to_move(left=left, right=right):
            self.moving_tetromino.move(left=left, right=right)

        if down:
            self.move_down()

    def remove_full_line(self):
        for i, line in enumerate(self.board):
            if all([isinstance(o, SmallBlock) for o in line]):
                for block in line:
                    self.blocks_in_game.remove(block)
                for block in self.blocks_in_game:
                    if block.coordinate[1] < i:
                        block.coordinate[1] += 1

    def update(self, down=True):
        if self.moving_tetromino is None:
            self.new_moving_tetromino(self.player.get_next_block())
        self.regenerate_board()
        if down:
            self.move_down()
        self.remove_full_line()

    def projection_coordinate(self):
        if self.moving_tetromino is None:
            return None

        coordinate_block = self.moving_tetromino.coordinate[:]
        for down_move in range(self.Y_SIZE):
            self.moving_tetromino.coordinate[1] += 1
            if not self.is_valid_tetromino(self.moving_tetromino):
                self.moving_tetromino.coordinate = coordinate_block
                return [coordinate_block[0], coordinate_block[1] + down_move]

        return None

    def move_completely_down(self):
        if self.moving_tetromino is not None:
            self.moving_tetromino.coordinate = self.projection_coordinate()

    def draw_projection(self, screen):
        if self.moving_tetromino is not None:
            old_coordinate = self.moving_tetromino.coordinate[:]
            self.moving_tetromino.coordinate = self.projection_coordinate()
            for coordinate in self.moving_tetromino.get_all_coordinates():
                position = self.coordinate_to_position(coordinate)
                pygame.draw.rect(screen, self.COLORS["light grey"],
                                 tuple(position) + (self.size_per_block, self.size_per_block), 2)

            self.moving_tetromino.coordinate = old_coordinate

    def draw_background(self, screen):
        for row in range(0, self.Y_SIZE * self.size_per_block, self.size_per_block):
            for col in range(0, self.X_SIZE * self.size_per_block, self.size_per_block):
                color = self.COLORS["dark grey"]
                if (row + col) // self.size_per_block % 2 == 0:
                    color = self.COLORS["darkest grey"]

                pygame.draw.rect(screen, color, (2 + self.left_top_position[0] + col,
                                                 2 + self.left_top_position[1] + row,
                                                 self.size_per_block - 2, self.size_per_block - 2))

    def draw(self, screen):
        pygame.draw.rect(screen, self.COLORS["darkest grey"], (self.left_top_position[0], self.left_top_position[1],
                                                               self.X_SIZE * self.size_per_block,
                                                               self.Y_SIZE * self.size_per_block))
        self.draw_background(screen)
        for block in self.blocks_in_game:
            block.draw(screen, self.size_per_block)

        if self.moving_tetromino is not None:
            self.moving_tetromino.draw(screen, self.size_per_block)

        self.draw_projection(screen)

