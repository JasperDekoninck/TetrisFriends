from SinglePlayerTetris import SinglePlayerTetris
import pygame
pygame.init()


def main():
    screen_size = (600, 600)
    screen = pygame.display.set_mode(screen_size)
    single_player = SinglePlayerTetris(screen, screen_size)

    single_player.play()

main()