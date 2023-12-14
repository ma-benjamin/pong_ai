import pygame


SCREEN_HEIGHT = 960
SCREEN_WIDTH = 1280

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
PONG_SOUND = pygame.mixer.Sound("pong.ogg")
SCORE_SOUND = pygame.mixer.Sound("score.ogg")

FONT = pygame.font.Font("freesansbold.ttf", 32)

GREY = pygame.Color('grey12')
LIGHT_GREY = (200, 200, 200)