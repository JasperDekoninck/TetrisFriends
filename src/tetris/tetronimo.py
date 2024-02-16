from .constants import *


class Block:
    """
    Small tetris 1x1 block that is used when a tetronimo is completely down on the board
    """
    NEXT_BLOCK_ID = -1

    def __init__(self, coordinate, image, board):
        """
        :param coordinate: tuple of ints, coordinate of the block
        :param image: pygame image, image used for the block
        :param board: Board, board on which the block is located
        """
        self.coordinate = coordinate
        self.board = board
        self.image = image

        # Id uniquely identyfing the block
        self.id = self.NEXT_BLOCK_ID
        self.NEXT_BLOCK_ID -= 1

    def draw(self, screen, size_block):
        """
        Draws the block on the screen
        :param screen: pygame screen object, Screen on which to display the Block
        :param size_block: Int, The size of the block:
        """
        pos = self.board.coordinate_to_position(self.coordinate)
        screen.blit(pygame.transform.scale(self.image, (size_block, size_block)), (pos[0], pos[1]))


class Tetromino:
    """
    Base Class for each tetromino
    """
    NEXT_ID = 1

    def __init__(self, start_co, image, board):
        """
        :param start_co: tuple of ints, The starting coordinate on the board of the tetromino
        :param image: pygame.image, The image for one block
        :param board: The board to which the tetromino is associated (can also be a SideBoard
        """
        self.coordinate = start_co
        self.board = board
        # The shape of the tetromino relative to its coordinate
        self.shape = []
        self.image = image

        # If a block has already been put on hold, it cannot be again put on hold
        self.holdable = True

        # id uniquely identifying the given tetromino
        self.id = self.NEXT_ID
        self.NEXT_ID += 1

    def turn(self):
        """
        Turns the tetromino if it is possible to turn the tetromino
        :post Every relative coordinate in shape is changed to -[0], [1] if the new turned shape is allowed
        """
        new_shape = []
        for shape in self.shape:
            new_shape.append([-shape[1], shape[0]])
        old_shape = self.shape[:]
        self.shape = new_shape
        if not self.board.is_valid_tetromino(self):
            self.shape = old_shape

    def possible_to_move(self, down=False, left=False, right=False):
        """
        Checks whether or not it is possible for the tetromino to move in the given direction
        :param down: Boolean, If True, Checks whether the tetromino can move Down
        :param left: Boolean, If True, Checks whether the tetromino can move left
        :param right: Boolean, If True, Checks whether the tetromino can move right

        Checking algorithm: move the tetromino in the given direction and check whether or not it can move there,
                            then move the tetromino back to its original coordinate
        """
        old_coordinate = self.coordinate[:]
        possible = False
        self.move(down, left, right)
        if self.board.is_valid_tetromino(self):
            possible = True

        self.coordinate = old_coordinate
        return possible

    def move(self, down=False, left=False, right=False):
        """
        Moves the tetromino in the given direction
        :param down: Boolean, If True, moves the tetromino down
        :param left: Boolean, If True, moves the tetromino left
        :param right: Boolean, If True, moves the tetromino right
        :return:
        """
        if down:
            self.coordinate[1] += 1
        if left:
            self.coordinate[0] -= 1
        if right:
            self.coordinate[0] += 1

    def get_all_coordinates(self):
        """
        Gets all coordinates of every block of the tetromino
        :return: A list of coordinates, each coordinate giving the absolute coordinate of the block
        """
        coordinates = []

        for relative_coordinate in self.shape:
            co = [self.coordinate[0] + relative_coordinate[0], self.coordinate[1] + relative_coordinate[1]]
            coordinates.append(co)
        return coordinates

    def draw(self, screen, size_block):
        """
        Draws the tetromino on screen with the given size of one block
        :param screen: pygame screen, Screen on which to draw the tetromino
        :param size_block: size of one block
        """
        for co in self.get_all_coordinates():
            pos = self.board.coordinate_to_position(co)
            screen.blit(pygame.transform.scale(self.image, (size_block, size_block)), pos)


class Stick(Tetromino):
    """
    Implementation of the Stick tetromino
    """
    def __init__(self, start_co, board):
        """
        :param start_co: tuple of ints, The starting coordinate on the board of the tetromino
        :param board: The board to which the tetromino is associated (can also be a SideBoard
        """
        Tetromino.__init__(self, start_co, LIGHTBLUE_BLOCK, board)
        shape1 = [[0, 0], [-1, 0], [1, 0], [2, 0]]
        self.shape = shape1


class Square(Tetromino):
    def __init__(self, start_co, board):
        """
        :param start_co: tuple of ints, The starting coordinate on the board of the tetromino
        :param board: The board to which the tetromino is associated (can also be a SideBoard
        """
        Tetromino.__init__(self, start_co, YELLOW_BLOCK, board)
        shape1 = [[0, 0], [0, 1], [1, 0], [1, 1]]
        self.shape = shape1


class RightTurn(Tetromino):
    """
    Implementation of the Right turn tetromino
    """
    def __init__(self, start_co, board):
        """
        :param start_co: tuple of ints, The starting coordinate on the board of the tetromino
        :param board: The board to which the tetromino is associated (can also be a SideBoard
        """
        Tetromino.__init__(self, start_co, GREEN_BLOCK, board)
        shape1 = [[0, 0], [-1, 0], [0, 1], [1, 1]]
        self.shape = shape1


class LeftTurn(Tetromino):
    """
    Implementation of the left turn tetromino
    """
    def __init__(self, start_co, board):
        """
        :param start_co: tuple of ints, The starting coordinate on the board of the tetromino
        :param board: The board to which the tetromino is associated (can also be a SideBoard
        """
        Tetromino.__init__(self, start_co, RED_BLOCK, board)
        shape1 = [[0, 0], [1, 0], [0, 1], [-1, 1]]
        self.shape = shape1


class TetrisBlock(Tetromino):
    """
    Implementation of the tetris block tetromino
    """
    def __init__(self, start_co, board):
        """
        :param start_co: tuple of ints, The starting coordinate on the board of the tetromino
        :param board: The board to which the tetromino is associated (can also be a SideBoard
        """
        Tetromino.__init__(self, start_co, PURPLE_BLOCK, board)
        shape1 = [[0, 0], [-1, 0], [0, -1], [1, 0]]
        self.shape = shape1


class HorseRight(Tetromino):
    """
    Implementation of the horse right tetromino
    """
    def __init__(self, start_co, board):
        """
        :param start_co: tuple of ints, The starting coordinate on the board of the tetromino
        :param board: The board to which the tetromino is associated (can also be a SideBoard
        """
        Tetromino.__init__(self, start_co, DARKBLUE_BLOCK, board)
        shape1 = [[0, 0], [1, 0], [-1, 0], [-1, -1]]
        self.shape = shape1


class HorseLeft(Tetromino):
    """
    Implementation of the Horse left tetromino
    """
    def __init__(self, start_co, board):
        """
        :param start_co: tuple of ints, The starting coordinate on the board of the tetromino
        :param board: The board to which the tetromino is associated (can also be a SideBoard
        """
        Tetromino.__init__(self, start_co, ORANGE_BLOCK, board)
        shape1 = [[0, 0], [-1, 0], [1, 0], [1, -1]]
        self.shape = shape1


POSSIBLE_TETROMINOS = [HorseLeft, HorseRight, TetrisBlock, Square, Stick, LeftTurn, RightTurn]
