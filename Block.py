import pygame
import os
pygame.init()


class SmallBlock:
    def __init__(self, start_co, image, board):
        self.coordinate = start_co
        self.board = board
        self.image = image

    def draw(self, screen, size_block):
        pos = self.board.coordinateToPos(self.coordinate)
        screen.blit(pygame.transform.scale(self.image, (size_block, size_block)), (pos[0], pos[1]))


class Tetromino:
    def __init__(self, start_co, image, board):
        self.coordinate = start_co
        self.board = board
        self.shape = []
        self.current_shape = 0
        self.image = image

    def turn(self):
        new_shape = []
        for shape in self.shape:
            new_shape.append([-shape[1], shape[0]])
        old_shape = self.shape[:]
        self.shape = new_shape
        if not self.board.is_valid_tetromino(self):
            self.shape = old_shape

    def possible_to_move(self, down=False, left=False, right=False):
        old_coordinate = self.coordinate[:]
        possible = False
        self.move(down, left, right)
        if self.board.is_valid_tetromino(self):
            possible = True

        self.coordinate = old_coordinate
        return possible

    def move(self, down=False, left=False, right=False):
        if down:
            self.coordinate[1] += 1
        if left:
            self.coordinate[0] -= 1
        if right:
            self.coordinate[0] += 1

    def get_all_coordinates(self):
        coordinates = []

        for relative_coordinate in self.shape:
            co = [self.coordinate[0] + relative_coordinate[0], self.coordinate[1] + relative_coordinate[1]]
            coordinates.append(co)
        return coordinates

    def draw(self, screen, size_block):
        for co in self.get_all_coordinates():
            pos = self.board.coordinateToPos(co)
            screen.blit(pygame.transform.scale(self.image, (size_block, size_block)), (pos[0], pos[1]))


class Stick(Tetromino):
    def __init__(self, start_co, board):
        """
        :param start_co:
        Example start_co: [0, 0]
        :param board:
        """
        image = pygame.image.load(os.path.join("images", "lightblue.jpg"))
        Tetromino.__init__(self, start_co, image, board)
        shape1 = [[0, 0], [-1, 0], [1, 0], [2, 0]]
        self.shape = shape1


class Square(Tetromino):
    def __init__(self, start_co, board):
        """
        :param start_co:
        Example start_co: [0, 0]
        :param board:
        """
        image = pygame.image.load(os.path.join("images", "yellow.jpg"))
        Tetromino.__init__(self, start_co, image, board)
        shape1 = [[0, 0], [0, 1], [1, 0], [1, 1]]
        self.shape = shape1


class RightTurn(Tetromino):
    def __init__(self, start_co, board):
        image = pygame.image.load(os.path.join("images", "green.jpg"))
        Tetromino.__init__(self, start_co, image, board)
        shape1 = [[0, 0], [-1, 0], [0, 1], [1, 1]]
        self.shape = shape1


class LeftTurn(Tetromino):
    def __init__(self, start_co, board):
        image = pygame.image.load(os.path.join("images", "red.jpg"))
        Tetromino.__init__(self, start_co, image, board)
        shape1 = [[0, 0], [1, 0], [0, 1], [-1, 1]]
        self.shape = shape1


class TetrisBlock(Tetromino):
    def __init__(self, start_co, board):
        image = pygame.image.load(os.path.join("images", "purple.jpg"))
        Tetromino.__init__(self, start_co, image, board)
        shape1 = [[0, 0], [-1, 0], [0, -1], [1, 0]]
        self.shape = shape1


class HorseRight(Tetromino):
    def __init__(self, start_co, board):
        image = pygame.image.load(os.path.join("images", "darkblue.jpg"))
        Tetromino.__init__(self, start_co, image, board)
        shape1 = [[0, 0], [1, 0], [-1, 0], [-1, -1]]
        self.shape = shape1


class HorseLeft(Tetromino):
    def __init__(self, start_co, board):
        image = pygame.image.load(os.path.join("images", "orange.jpg"))
        Tetromino.__init__(self, start_co, image, board)
        shape1 = [[0, 0], [-1, 0], [1, 0], [1, -1]]
        self.shape = shape1
