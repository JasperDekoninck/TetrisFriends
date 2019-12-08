from CONSTANTS import *
from Button import TextButton, InputField


class GameOverMenu:
    """
    Menu for when the player dies or wins the level.
    """
    def __init__(self, screen, screen_size):
        self.screen = screen
        self.screen_size = screen_size
        self.report_button = TextButton((10, 10), "Game over", 40, pygame.Color("White"))
        self.play_button = TextButton((10, 70), "Play again", 40, pygame.Color("white"), pygame.Color("red"))
        self.main_button = TextButton((10, 130), "Main menu", 40, pygame.Color("white"), pygame.Color("red"))
        self.input_field = InputField((screen_size[0] // 2, screen_size[1] // 2), "What is your name?", 30,
                                      pygame.Color("white"))
        self.clock = pygame.time.Clock()

        # A variable registering how long the user has been in the menu. Not allowing anything to happen before
        # this variable gets to a certain size, makes sure it is not possible to accidently click and go two menus
        # further
        self.time_after_creation = 0

    def render(self):
        self.screen.fill((0, 0, 0))
        self.report_button.render(self.screen)
        self.play_button.render(self.screen)
        self.main_button.render(self.screen)
        self.input_field.render(self.screen)

    def mouse_update(self):
        mouse_buttons = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()

        self.play_button.update_selected(pos)
        self.main_button.update_selected(pos)
        if mouse_buttons[0] and self.time_after_creation > 0.1:
            if self.play_button.selected:
                return "single player", None
            elif self.main_button.selected:
                return "main menu", None

        return None

    def loop(self, points, *args):
        self.time_after_creation = 0
        self.input_field.question.set_text("You have {} points. What is your name?".format(points))
        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.input_field.new_input_letter(None)
                    elif event.key == pygame.K_RETURN:
                        return "high score", self.input_field.input.message
                    else:
                        self.input_field.new_input_letter(event.unicode)

            selected_menu = self.mouse_update()
            if selected_menu is not None:
                return selected_menu

            get_fps = self.clock.get_fps()
            if get_fps != 0:
                self.time_after_creation += 1 / get_fps

            self.render()
            pygame.display.update()
