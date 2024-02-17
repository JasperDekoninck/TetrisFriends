from .board import Board
from .side_board import SideBoard
from .button import TextButton
from .constants import *
import time


class Player:
    def __init__(self, base_pos, size_per_block):
        """
        Initializes a Player object.

        Args:
            base_pos (list): The base position of the player.
            size_per_block (int): The size of each block.

        Attributes:
            pos (list): The position of the player.
            board (Board): The player's game board.
            size_per_block (int): The size of each block.
            size_square (int): The size of the player's square.
            size_per_block_side_board (int): The size of each block on the side board.
            sideboard (SideBoard): The player's side board.
            death (bool): Indicates if the player is dead.
            points (int): The player's points.
            lines (int): The number of lines cleared by the player.
            pressed_times (list): The times at which the player's keys were pressed.
            time_between_movements (float): The time between movements.
            time_between_turns (float): The time between turns.
            points_message (TextButton): The message displaying the player's points.
        """
        
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
        """
        Retrieves the next tetromino from the sideboard.

        Returns:
            The next tetromino object.
        """
        return self.sideboard.get_next_tetromino()

    def draw_points(self, screen):
        """
        Draw the player's points on the screen.

        Args:
            screen: The screen surface to draw on.
        """
        self.points_message.set_text("Points: {}".format(self.points))
        self.points_message.render(screen)

    def draw(self, screen):
        """
        Draw the player's board, sideboard, and points on the screen.

        Args:
            screen: The screen surface to draw on.
        """
        self.board.draw(screen)
        self.sideboard.draw(screen, self.size_square)
        self.draw_points(screen)

    def move_tetromino(self, left=False, right=False, down=False):
        """
        Move the tetromino in the specified direction.

        Args:
            left (bool): Whether to move the tetromino to the left.
            right (bool): Whether to move the tetromino to the right.
            down (bool): Whether to move the tetromino down.

        Returns:
            None
        """
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
        """
        Turns the current tetromino in the game board.
        """
        if time.time() - self.pressed_times[3] > self.time_between_turns:
            self.board.turn()
            self.pressed_times[3] = time.time()

    def move_completely_down(self):
        """
        Moves the player's piece completely down on the game board.
        """
        if time.time() - self.pressed_times[4] > self.time_between_turns:
            self.pressed_times[4] = time.time()
            self.board.move_completely_down()

    def hold_block(self):
        """
        Holds the current tetromino and updates the sideboard.

        This method is called when the player wants to hold the current tetromino and switch it with the one in the hold area.
        It checks if enough time has passed since the last hold action, and if so, updates the hold area on the sideboard with the current tetromino.

        """
        if time.time() - self.pressed_times[5] > self.time_between_turns:
            self.pressed_times[5] = time.time()
            self.sideboard.set_hold_tetromino(self.board.moving_tetromino)

    def update(self, down=True):
        """
        Update the player's position on the board.

        Parameters:
        - down (bool): Whether the player is moving down or not. Default is True.

        Returns:
        None
        """
        self.board.update(down)
