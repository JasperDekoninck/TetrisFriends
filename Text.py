import pygame

pygame.init()

class Text:
    def __init__(self, message, pos, position=["middle", "top"], size=40, type="liberationserif", bold=False,
                 italic=False, color=(85, 85, 85), background_color=(255, 255, 255)):
        """message: message you want to show
           pos: position of the message
           position: where the coordinates of the pos, should be located e.g. 'middle' means that pos will be
           in the exact middle of the text, you have the possibility to give this in as a list like ["middle", "top"]
           or just "top" if it is the same for both coordinates, the different possibilities are: "middle", "top" (only for y),
           "bottom" (only for y), "left" (only for x), "right" (only for x)
           size: size of the text
           type: type of text
           bold: whether or not you want your text to be bold
           italic: whether or not you want italics
           color: color of your text
           background_color: background color text
        """
        self.font = pygame.font.SysFont(type, size=size, bold=bold, italic=italic)
        self.message = self.font.render(message, True, color, background_color)
        self.size_message = self.message.get_size()
        self.color = color
        self.background_color = background_color
        self.original_pos = pos[:]
        self.pos = pos
        if isinstance(position, (str)):
            position = [position, position]

        self.position = position

        if position[0] == "middle":
            self.pos[0] -= int(self.size_message[0] / 2)
        elif position[0] == "right":
            self.pos[0] -= self.size_message[0]

        if position[1] == "middle":
            self.pos[1] -= int(self.size_message[1] / 2)
        elif position[1] == "bottom":
            self.pos[1] -= self.size_message[1]

    def draw(self, screen):
        screen.blit(self.message, self.pos)

    def change_message(self, new_message):
        self.pos = self.original_pos[:]
        self.message = self.font.render(new_message, True, self.color, self.background_color)
        self.size_message = self.message.get_size()
        if self.position[0] == "middle":
            self.pos[0] -= int(self.size_message[0] / 2)
        elif self.position[0] == "right":
            self.pos[0] -= self.size_message[0]

        if self.position[1] == "middle":
            self.pos[1] -= int(self.size_message[1] / 2)
        elif self.position[1] == "bottom":
            self.pos[1] -= self.size_message[1]