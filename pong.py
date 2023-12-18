import pygame, random, sys
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, PONG_SOUND, SCORE_SOUND, FONT, GREY, LIGHT_GREY
from utils import *
import math


class PongGame:
    def __init__(self, w=SCREEN_WIDTH, h = SCREEN_HEIGHT):
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption('Pong')
        self.clock = pygame.time.Clock()

        self.screen_w = w
        self.screen_h = h
        
        self.reset()

    def reset(self):
        self.ball = pygame.Rect(self.screen_w/2 - 15, self.screen_h/2 - 15, 30, 30)
        self.player = pygame.Rect(self.screen_w - 20, self.screen_h/2 - 70, 10, 140)
        self.opponent = pygame.Rect(10, self.screen_h/2 - 70, 10, 140)

        angle = random.randrange(360)
        self.ball_velocity_x, self.ball_velocity_y = directionComponents(angle)

        self.player_speed = 0
        self.opponent_speed = 7

        self.player_score = 0
        self.opponent_score = 0

        self.score_time = True

        self.frame_iteration = 0

        

    def player_move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: 
                    self.player_speed = -7
                if event.key == pygame.K_DOWN:
                    self.player_speed = 7
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.player_speed = 0
                if event.key == pygame.K_DOWN:
                    self.player_speed = 0

    def ball_animation(self):
        self.ball.x += self.ball_velocity_x
        self.ball.y += self.ball_velocity_y

        if self.ball.top <= 0 or self.ball.bottom >= self.screen_h:
            pygame.mixer.Sound.play(PONG_SOUND)
            self.ball_velocity_y *= -1

        # Player Score
        if self.ball.left <= 0:
            pygame.mixer.Sound.play(SCORE_SOUND)
            self.player_score += 1
            self.score_time = pygame.time.get_ticks()

        # Opponent Score
        if self.ball.right >= self.screen_w:
            pygame.mixer.Sound.play(SCORE_SOUND)
            self.opponent_score += 1
            self.score_time = pygame.time.get_ticks()

        if self.ball.colliderect(self.player) or self.ball.colliderect(self.opponent):
            pygame.mixer.Sound.play(PONG_SOUND)
            self.ball_velocity_x *= -1
            if self.ball.colliderect(self.player):
                self.ball_velocity_y *= (1 + 0.25 * abs(self.player_speed))
            else:
                self.ball_velocity_y *= (1 + 0.25 * abs(self.opponent_speed))

    def player_animation(self):
        self.player.y += self.player_speed

        if self.player.top <= 0:
            self.player.top = 0
        if self.player.bottom >= self.screen_h:
            self.player.bottom = self.screen_h
            
    def opponent_move(self):
        if self.opponent.top < self.ball.y:
            self.opponent.y += self.opponent_speed
        if self.opponent.bottom > self.ball.y:
            self.opponent.y -= self.opponent_speed

        if self.opponent.top <= 0:
            self.opponent.top = 0
        if self.opponent.bottom >= self.screen_h:
            self.opponent.bottom = self.screen_h

    def ball_reset(self):
        current_time = pygame.time.get_ticks()
        self.ball.center = (self.screen_w/2, self.screen_h/2)
        
        if current_time - self.score_time < 700:
            number_three = FONT.render(("3"), False, LIGHT_GREY)
            self.screen.blit(number_three, (self.screen_w/2 - 10, self.screen_h/2 + 20))
        if 700 < current_time - self.score_time <= 1400:
            number_two = FONT.render(("2"), False, LIGHT_GREY)
            self.screen.blit(number_two, (self.screen_w/2 - 10, self.screen_h/2 + 20))
        if 1400 < current_time - self.score_time <= 2100:
            number_one = FONT.render(("1"), False, LIGHT_GREY)
            self.screen.blit(number_one, (self.screen_w/2 - 10, self.screen_h/2 + 20))

        if current_time - self.score_time <= 2100:
            self.ball_velocity_x = self.ball_velocity_y = 0
        else:
            angle = random.randrange(360)
            self.ball_velocity_x, self.ball_velocity_y = directionComponents(angle)
            self.score_time = None

    def update(self):
        self.ball_animation()
        self.player_animation()
        self.opponent_move()

        self.screen.fill(GREY)
        pygame.draw.rect(self.screen, LIGHT_GREY, self.player)
        pygame.draw.rect(self.screen, LIGHT_GREY, self.opponent)
        pygame.draw.ellipse(self.screen, LIGHT_GREY, self.ball)
        pygame.draw.aaline(self.screen, LIGHT_GREY, (self.screen_w/2, 0), (self.screen_w/2, self.screen_h))

        if self.score_time:
            self.ball_reset()

        player_text = FONT.render(f'{self.player_score}',False,LIGHT_GREY)
        self.screen.blit(player_text,(660,470))

        opponent_text = FONT.render(f'{self.opponent_score}',False,LIGHT_GREY)
        self.screen.blit(opponent_text,(600,470))

        pygame.display.flip()
        self.clock.tick(60)