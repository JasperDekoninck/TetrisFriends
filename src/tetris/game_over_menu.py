from .constants import *
from .button import TextButton, InputField


class GameOverMenu:
    """
    Menu for when the player dies or wins the level.
    """
    def __init__(self, screen, screen_size):
        """
        Initializes the GameOverMenu object.

        Args:
            screen (pygame.Surface): The screen surface to render the menu on.
            screen_size (tuple): The size of the screen.

        Attributes:
            screen (pygame.Surface): The screen surface to render the menu on.
            screen_size (tuple): The size of the screen.
            report_button (TextButton): The button to report the game over.
            play_button (TextButton): The button to play the game again.
            main_button (TextButton): The button to go back to the main menu.
            input_field (InputField): The input field to enter the player's name.
            clock (pygame.time.Clock): The clock object to control the frame rate.
            time_after_creation (int): The time elapsed since the menu was created.
        """
        
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
        """
        Renders the game over menu on the screen.
        """
        self.screen.fill((0, 0, 0))
        self.report_button.render(self.screen)
        self.play_button.render(self.screen)
        self.main_button.render(self.screen)
        self.input_field.render(self.screen)

    def mouse_update(self):
        """
        Updates the mouse state and handles mouse click events.

        Returns:
            tuple or None: A tuple containing the action and additional data if a button is clicked, 
                            or None if no button is clicked.
        """
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
        """
        Main loop for the game over menu.

        Args:
            points (int): The number of points the player has earned.

        Returns:
            tuple: A tuple containing the next menu to display and the player's name.
        """
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
