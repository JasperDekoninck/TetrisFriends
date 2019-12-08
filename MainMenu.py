from CONSTANTS import *
from Button import TextButton


class MainMenu:
    """
    Main menu
    """
    def __init__(self, screen):
        self.screen = screen
        # Loading the background world for the main menu
        self.play_button = TextButton((10, 10), "Single player", 40, pygame.Color("white"), pygame.Color("red"))
        self.level_button = TextButton((10, 60), "Level Creator", 40, pygame.Color("white"), pygame.Color("red"))
        self.about_button = TextButton((10, 110), "About", 40, pygame.Color("white"), pygame.Color("red"))
        self.settings_button = TextButton((10, 160), "Settings", 40, pygame.Color("white"), pygame.Color("red"))
        self.clock = pygame.time.Clock()
        self.time_since_creation = 0

    def render(self):
        self.play_button.render(self.screen)
        self.level_button.render(self.screen)
        self.about_button.render(self.screen)
        self.settings_button.render(self.screen)

    def loop(self, *args):
        self.time_since_creation = 0
        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            mouse_buttons = pygame.mouse.get_pressed()
            pos = pygame.mouse.get_pos()
            self.play_button.update_selected(pos)
            self.level_button.update_selected(pos)
            self.about_button.update_selected(pos)
            self.settings_button.update_selected(pos)
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