import pygame
from pong import PongGame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

SCREEN_HEIGHT = 960
SCREEN_WIDTH = 1280

def play():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    pygame.display.set_caption('Pong')
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    game = PongGame(screen)

    while True:
        game.player_move()

        game.update()

        pygame.display.flip()
        clock.tick(60)

play()