from tetris import SinglePlayerTetris, MainMenu, GameOverMenu, HighScoreMenu
import pygame
pygame.init()


def main():
    screen_size = (600, 600)
    screen = pygame.display.set_mode(screen_size)
    main_menu = MainMenu(screen)
    single_player = SinglePlayerTetris(screen, screen_size)
    game_over = GameOverMenu(screen, screen_size)
    high_score_menu = HighScoreMenu(screen, screen_size)
    menu = "main menu"
    points = 0
    name = None

    while True:
        if menu == "single player":
            single_player.reset()
            menu, points = single_player.loop()
        elif menu == "main menu":
            menu = main_menu.loop()
        elif menu == "game over":
            menu, name = game_over.loop(points)
        elif menu == "high score":
            menu = high_score_menu.loop(points, name)


main()