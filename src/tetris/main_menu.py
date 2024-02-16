from .constants import *
from .button import TextButton


class MainMenu:
    """
    Main menu
    """
    def __init__(self, screen):
        """
        Initializes the Main Menu object.

        Args:
            screen: The Pygame screen object.

        Attributes:
            screen: The Pygame screen object.
            play_button: The button for single player mode.
            clock: The Pygame clock object.
            time_since_creation: The time elapsed since the creation of the Main Menu object.
        """
        
        self.screen = screen
        self.play_button = TextButton((10, 10), "Single player", 40, pygame.Color("white"), pygame.Color("red"))
        self.clock = pygame.time.Clock()
        self.time_since_creation = 0

    def render(self):
        """
        Renders the main menu screen.
        """
        self.screen.fill((0, 0, 0))
        self.play_button.render(self.screen)
        # self.level_button.render(self.screen)
        # self.about_button.render(self.screen)
        # self.settings_button.render(self.screen)

    def loop(self, *args):
        """
        Executes the main menu loop.
        
        Args:
            *args: Variable length argument list.
        
        Returns:
            str: The selected menu option.
        """
        
        self.time_since_creation = 0
        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            mouse_buttons = pygame.mouse.get_pressed()
            pos = pygame.mouse.get_pos()
            self.play_button.update_selected(pos)
            # self.level_button.update_selected(pos)
            # self.about_button.update_selected(pos)
            # self.settings_button.update_selected(pos)
            if mouse_buttons[0] and self.time_since_creation > 0.1:
                if self.play_button.selected:
                    return "single player"
                #elif self.level_button.selected:
                    #   return "creator"
                #elif self.about_button.selected:
                    #   return "about"
                #elif self.settings_button.selected:
                    #   return "settings"

            self.render()
            get_fps = self.clock.get_fps()
            if get_fps != 0:
                # this small line allows a user to play the game in the main menu!
                self.time_since_creation += 1 / get_fps

            pygame.display.update()
