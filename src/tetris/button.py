import pygame
import numpy as np
pygame.init()


class Button:
    def __init__(self, pos, content, hover_over_content=None, center_pos=False):
        """
        Initialize a Button object.

        Args:
            pos (tuple): The position of the button (x, y).
            content (pygame.Surface): The content to be displayed on the button.
            hover_over_content (pygame.Surface, optional): The content to be displayed when the button is hovered over. Defaults to None.
            center_pos (bool, optional): Whether to center the button position. Defaults to False.
        """
        self.pos = pos
        self.mid_pos = None
        self.content = content
        self.hover_over_content = hover_over_content
        self.center_pos = center_pos
        self.size = self.content.get_size()

        if center_pos:
            self.pos = list(pos)
            self.mid_pos = pos[:]
            self.pos[0] = self.pos[0] - self.size[0] // 2
            self.pos[1] = self.pos[1] - self.size[1] // 2

        self.selected = False

    def set_content(self, new_content):
        """
        Sets the content of the button.

        Parameters:
        - new_content: The new content to be set.

        Returns:
        None
        """
        self.content = new_content
        self.size = self.content.get_size()
        if self.center_pos:
            self.pos[0] = self.mid_pos[0] - self.size[0] // 2
            self.pos[1] = self.mid_pos[1] - self.size[1] // 2

    def is_selected(self, pos):
        """
        Check if the button is selected based on the given position.

        Args:
            pos (tuple): The position to check against.

        Returns:
            bool: True if the button is selected, False otherwise.
        """
        return self.pos[0] <= pos[0] <= self.pos[0] + self.size[0] and \
               self.pos[1] <= pos[1] <= self.pos[1] + self.size[1]

    def update_selected(self, pos):
        """
        Updates the selected state of the button based on the given position.

        Args:
            pos (tuple): The position (x, y) to check for selection.

        Returns:
            None
        """
        self.selected = self.is_selected(pos)

    def render(self, screen, pos=np.zeros(2)):
        """
        Renders the button on the screen at the specified position.

        Args:
            screen: The screen surface to render the button on.
            pos: The position of the button on the screen. Defaults to (0, 0).

        Returns:
            None
        """
        pos = np.array(pos)
        if not self.selected or self.hover_over_content is None:
            position = (self.pos[0] + pos[0].astype(np.int32), self.pos[1] + pos[1].astype(np.int32))
            screen.blit(self.content, position)
        else:
            screen.blit(self.hover_over_content, self.pos - pos.astype(np.int32))


class TextButton(Button):
    def __init__(self, pos, message, size, color_not_selected, color_selected=None, center_pos=False):
        """
        Initializes a TextButton object.

        Args:
            pos (tuple): The position of the button (x, y).
            message (str): The text to be displayed on the button.
            size (int): The font size of the text.
            color_not_selected (tuple): The color of the text when the button is not selected (R, G, B).
            color_selected (tuple, optional): The color of the text when the button is selected (R, G, B). Defaults to None.
            center_pos (bool, optional): Whether to center the button position. Defaults to False.
        """
        
        font = pygame.font.Font("motion-control.bold.otf", size)
        content = font.render(message, True, color_not_selected)
        hover_content = None
        if color_selected is not None:
            hover_content = font.render(message, True, color_selected)

        self.font = font
        self.message = message
        self.color = color_not_selected
        self.color_selected = color_selected
        super(TextButton, self).__init__(pos, content, hover_content, center_pos=center_pos)

    def set_text(self, new_text):
        """
        Sets the text of the button.

        Args:
            new_text (str): The new text to be displayed on the button.

        Returns:
            None
        """
        new_content = self.font.render(new_text, True, self.color)
        self.message = new_text
        self.set_content(new_content)
        if self.color_selected is not None:
            self.hover_over_content = self.font.render(new_text, True, self.color_selected)


class InputField:
    def __init__(self, pos, question, size, color, center_pos=True):
        """
        Initializes a Button object.

        Args:
            pos (list): The position of the button.
            question (str): The text displayed on the button.
            size (int): The font size of the button text.
            color (tuple): The color of the button.
            center_pos (bool, optional): Whether to center the button position. Defaults to True.
        """
        
        self.question = TextButton(pos, question, size, color, center_pos=center_pos)
        self.input = TextButton([pos[0], pos[1] + self.question.content.get_size()[1]],
                                "", size, color, center_pos=center_pos)

    def new_input_letter(self, new_letter=None):
        """
        Updates the input message by adding a new letter.

        Args:
            new_letter (str, optional): The new letter to be added. If not provided, the last letter is removed.

        Returns:
            None
        """
        if new_letter is None:
            self.input.set_text(self.input.message[:-1])
        else:
            self.input.set_text(self.input.message + new_letter)

    def render(self, screen):
        """
        Renders the button on the screen.

        Args:
            screen: The screen surface to render the button on.
        """
        self.question.render(screen)
        self.input.render(screen)
