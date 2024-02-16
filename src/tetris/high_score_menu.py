from .button import TextButton
from .constants import *
import pickle


class HighScoreMenu:
    def __init__(self, screen, screen_size):
        """
        Initializes the HighScoreMenu object.

        Args:
            screen (pygame.Surface): The screen surface to draw on.
            screen_size (tuple): The size of the screen.

        Attributes:
            screen (pygame.Surface): The screen surface to draw on.
            drawings (pygame.Surface): A copy of the screen surface for drawing purposes.
            highscore (TextButton): The button for displaying the highscores.
            highscores (list): A list of highscores.
            highscore_messages (list): A list of TextButton objects for displaying the highscore messages.
            extra_message (TextButton): An additional message button.
            main_menu_message (TextButton): The button for returning to the main menu.
        """
        
        self.screen = screen
        self.drawings = screen.copy()
        highscore_pos = (screen_size[0] // 2, 30)
        self.highscore = TextButton(highscore_pos, "Highscores", 40, pygame.Color("white"), center_pos=True)

        try:
            self.highscores = self.read_highscore_file()
        except Exception:
            self.highscores = []

        self.highscore_messages = []
        self.extra_message = TextButton((highscore_pos[0], highscore_pos[1] + self.highscore.content.get_size()[1]),
                                        "", 30, pygame.Color("white"), center_pos=True)

        current_pos = [self.extra_message.pos[0] - self.highscore.content.get_size()[0] // 2,
                        self.extra_message.pos[1] + self.extra_message.content.get_size()[1]]

        for highscore in self.highscores:
            self.highscore_messages.append(TextButton(current_pos[:], highscore, 20, pygame.Color("white")))
            current_pos[1] += self.highscore_messages[-1].content.get_size()[1] + 5

        pos = (self.extra_message.pos[0],
                self.extra_message.pos[1] + self.extra_message.content.get_size()[1] * 10)
        self.main_menu_message = TextButton(pos, "Main Menu", 40, pygame.Color("white"), pygame.Color("red"),
                                            center_pos=True)

    def read_highscore_file(self):
        """
        Reads the highscore data from the 'highscore.pkl' file and returns it.

        Returns:
            The highscore data read from the file.
        """
        with open("highscore.pkl", "rb") as f:
            return pickle.load(f)

    def write_highscore(self):
        """
        Writes the highscores to a file using pickle.

        This method serializes the `highscores` attribute of the class
        and saves it to a file named "highscore.pkl" using the pickle module.

        Parameters:
        None

        Returns:
        None
        """
        pickle.dump(self.highscores, open("highscore.pkl", "wb"))

    def insert_points(self, points, name):
        """
        Inserts the given points and name into the highscores list, updating the rankings accordingly.

        Args:
            points (int): The points to be inserted.
            name (str): The name associated with the points.

        Returns:
            None
        """
        
        scores = [int(highscore.split(" ")[-1]) for highscore in self.highscores]
        place = 0
        while place < len(scores) and scores[place] >= points:
            place += 1

        if place >= 10:
            self.extra_message.set_text("Unfortunately, you did not make it into the top 10.")
        else:
            self.extra_message.set_text(f"Congrats! You ended on place {place + 1}.")

        new_score = f"{place + 1}. {name}: {int(points)}"
        self.highscores.insert(place, new_score)

        for i in range(place + 1, len(self.highscores)):
            self.highscores[i] = str(int(self.highscores[i][0]) + 1) + self.highscores[i][1:]

        if len(self.highscores) > 10:
            self.highscores = self.highscores[:-1]

        self.write_highscore()

        self.highscore_messages = []
        current_pos = [self.extra_message.pos[0] - self.highscore.content.get_size()[0] // 2,
                        self.extra_message.pos[1] + self.extra_message.content.get_size()[1]]

        for highscore in self.highscores:
            self.highscore_messages.append(TextButton(current_pos[:], highscore, 20, pygame.Color("white")))
            current_pos[1] += self.highscore_messages[-1].content.get_size()[1] + 5

    def loop(self, points, name):
        """
        Runs the main loop of the high score menu.
        
        Args:
            points (int): The player's score.
            name (str): The player's name.
        Returns:
            str: The next menu to navigate to.
        """
        self.insert_points(points, name)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            mouse_pressed = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            self.main_menu_message.update_selected(mouse_pos)
            if mouse_pressed[0]:
                if self.main_menu_message.selected:
                    return "main menu"

            self.draw()
            pygame.display.update()

    def draw(self):
        """
        Draws the high score menu on the screen.
        """
        self.screen.fill((0, 0, 0))
        self.highscore.render(self.screen)
        self.extra_message.render(self.screen)
        self.main_menu_message.render(self.screen)
        for highscore in self.highscore_messages:
            highscore.render(self.screen)
