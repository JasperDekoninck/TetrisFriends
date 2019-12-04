from Tetromino import *
from CONSTANTS import *


class Board:
    """
    Controls the main tetris board of a player.
    """
    def __init__(self, player, size_per_block, left_top_position):
        """
        :param player: Player, player to which this board is associated
        :param size_per_block: Int, size for each block fo a tetromino
        :param left_top_position: Tuple of ints, Top left position of the board
        """
        self.player = player
        self.size_per_block = size_per_block
        self.left_top_position = left_top_position

        # The tetronimo that is moving
        self.moving_tetromino = None

        # List of all the blocks that are already down
        self.blocks_in_game = []

        # The entire board, containing all the information
        # 0: Nothing at this coordinate
        # Positive id: Moving tetromino at this coordinate
        # Negative id: Block at this coordinate
        self.board = [[0 for _ in range(X_SIZE)] for _ in range(Y_SIZE)]

    def is_valid_tetromino(self, tetromino):
        """
        Checks whether or not the given tetromino can be on the board
        :param tetromino: The tetromino that needs to be checked
        :return: Boolean, indicating whether or not the given tetromino is valid
        """
        for co in tetromino.get_all_coordinates():
            if 0 > co[0] or co[0] > X_SIZE - 1 or 0 > co[1] or co[1] > Y_SIZE - 1 or \
                    (self.board[co[1]][co[0]] != 0 and self.board[co[1]][co[0]] != tetromino.id):
                return False
        return True

    def coordinate_to_position(self, coordinate):
        """
        Converts a coordinate ot a position on the screen.
        :param coordinate: Tuple of ints, The coordinate on the board
        :return: List of ints, The position on the screen
        """
        return [self.left_top_position[0] + self.size_per_block * coordinate[0],
                self.left_top_position[1] + self.size_per_block * coordinate[1]]

    def new_moving_tetromino(self, next_tetromino):
        """
        Creates a new moving tetromino
        :param next_tetromino: The next moving tetromino
        :post sets the coordinates of the next tetromino to be top middle of the board
        :post If the next_tetromino is not valid at this position, set the player to be death
        """
        self.moving_tetromino = next_tetromino
        self.moving_tetromino.coordinate = [int(X_SIZE / 2),
                                            -min([min(co) for co in self.moving_tetromino.shape])]

        if not self.is_valid_tetromino(self.moving_tetromino):
            self.player.death = True

    def regenerate_board(self):
        """
        Regenerates the board with all the relevant information
        """
        self.board = [[0 for _ in range(X_SIZE)] for _ in range(Y_SIZE)]
        for co in self.moving_tetromino.get_all_coordinates():
            self.board[co[1]][co[0]] = self.moving_tetromino.id

        for block in self.blocks_in_game:
            self.board[block.coordinate[1]][block.coordinate[0]] = -1

    def move_down(self):
        """
        Moves the moving tetromino down if posssible, if not possible, set the moving tetromino to None and
        Appends all its blocks to the blocks_in_game list
        """
        if self.moving_tetromino is not None and self.moving_tetromino.possible_to_move(down=True):
            self.moving_tetromino.move(down=True)
        else:
            for co in self.moving_tetromino.get_all_coordinates():
                self.blocks_in_game.append(Block(co, self.moving_tetromino.image, self))
            self.moving_tetromino = None

    def move(self, left=False, right=False, down=False):
        """
        Moves the moving tetromino in the given direction if its possible
        :param left: Boolean, whether or not the tetromino needs to move to the left
        :param right: Boolean, whether or not the tetromino needs to move to the right
        :param down: Boolean, whether or not the tetromino needs to move down
        """
        if self.moving_tetromino is not None and self.moving_tetromino.possible_to_move(left=left, right=right):
            self.moving_tetromino.move(left=left, right=right)

        if down:
            self.move_down()

    def turn(self):
        """
        Turns the moving tetromino
        """
        if self.moving_tetromino is not None:
            self.moving_tetromino.turn()

    def remove_block_with_id(self, iden):
        """
        Removes the block with the given id from the blocks_in_game list
        :param iden: Negative int, the id of the block
        """
        for i, block in enumerate(self.blocks_in_game):
            if block.id == iden:
                self.blocks_in_game = self.blocks_in_game[:i] + self.blocks_in_game[i+1:]
                break

    def remove_full_line(self):
        """
        Removes a line from the board if it's completely filled.
        :post If a given row is full of blocks, removes that row and moves all blocks on top of that row down
        """
        for i, line in enumerate(self.board):
            if all([o < 0 for o in line]):
                for iden in line:
                    self.remove_block_with_id(iden)
                for block in self.blocks_in_game:
                    if block.coordinate[1] < i:
                        block.coordinate[1] += 1

    def update(self, down=True):
        """
        Updates the board
        :param down: Boolean, whether or not the tetromino needs to move down
        :post If the moving tetromino is None, get the next tetromino
        :post regenerates the board with the current information
        :post move down if down=True
        :post remove all full lines if present.
        """
        if self.moving_tetromino is None:
            self.new_moving_tetromino(self.player.get_next_tetromino())
        self.regenerate_board()
        if down:
            self.move_down()
        self.remove_full_line()

    def projection_coordinate(self):
        """
        Gets the coordinate of the projection of the moving tetromino on the bottom of the board
        """
        if self.moving_tetromino is None:
            return None

        coordinate_tetromino = self.moving_tetromino.coordinate[:]
        for down_move in range(Y_SIZE):
            self.moving_tetromino.coordinate[1] += 1
            if not self.is_valid_tetromino(self.moving_tetromino):
                self.moving_tetromino.coordinate = coordinate_tetromino
                return [coordinate_tetromino[0], coordinate_tetromino[1] + down_move]

    def move_completely_down(self):
        """
        Moves the moving tetromino to the bottom of the board
        """
        if self.moving_tetromino is not None:
            self.moving_tetromino.coordinate = self.projection_coordinate()

    def draw_projection(self, screen):
        """
        Draws the projection of the moving tetromino on the screen.
        :param screen: Pygame screen, the screen on which to display the projection
        Used method: move the tetromino down, draw it and move it back up
        """
        if self.moving_tetromino is not None:

            old_coordinate = self.moving_tetromino.coordinate[:]
            self.moving_tetromino.coordinate = self.projection_coordinate()

            if old_coordinate[1] != self.moving_tetromino.coordinate[1]:
                for coordinate in self.moving_tetromino.get_all_coordinates():
                    position = self.coordinate_to_position(coordinate)
                    pygame.draw.rect(screen, COLORS["light grey"],
                                     tuple(position) + (self.size_per_block, self.size_per_block), 2)

            self.moving_tetromino.coordinate = old_coordinate

    def draw_background(self, screen):
        """
        Draws the background (gridlines) of the board on screen
        :param screen: Pygame screen, the screen on which to display the background.
        """
        for row in range(0, Y_SIZE * self.size_per_block, self.size_per_block):
            for col in range(0, X_SIZE * self.size_per_block, self.size_per_block):
                color = COLORS["dark grey"]
                if (row + col) // self.size_per_block % 2 == 0:
                    color = COLORS["darkest grey"]

                pygame.draw.rect(screen, color, (2 + self.left_top_position[0] + col,
                                                 2 + self.left_top_position[1] + row,
                                                 self.size_per_block - 2, self.size_per_block - 2))

    def draw(self, screen):
        """
        Draws the board on the screen
        :param screen: pygame screen, screen on which to display the board
        """
        pygame.draw.rect(screen, COLORS["darkest grey"], (self.left_top_position[0], self.left_top_position[1],
                                                          X_SIZE * self.size_per_block,
                                                          Y_SIZE * self.size_per_block))
        self.draw_background(screen)
        for block in self.blocks_in_game:
            block.draw(screen, self.size_per_block)

        if self.moving_tetromino is not None:
            self.moving_tetromino.draw(screen, self.size_per_block)

        self.draw_projection(screen)
