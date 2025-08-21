import pygame
import random
from src.objects import *

class Intro_animation(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Intro_animation, self).__init__()
        self.background = pygame.image.load('source/info.png').convert_alpha()
        self.bg_big = pygame.transform.scale(self.background, (x, y))
        self.rect = self.bg_big.get_rect(center=(450, 300))

    def fadeout_animation(self, win, clock, a):
        while a > 0:
            background = pygame.Surface((win.get_rect().width, win.get_rect().height))
            background.fill(BLACK)
            self.background.set_alpha(a)
            self.bg_big = pygame.transform.scale(self.background, (300, 300))
            win.blit(background, background.get_rect())
            win.blit(self.bg_big, self.rect)
            pygame.display.update()
            clock.tick(20)
            a -= 5

class Intro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Intro, self).__init__()
        background = pygame.image.load('source/start.png').convert_alpha()
        self.bg_big = pygame.transform.scale(background, (x, y))
        self.rect = self.bg_big.get_rect(center=(450, 300))

class BG(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(BG, self).__init__()
        background = pygame.image.load('source/bg.png').convert_alpha()
        self.bg_big = pygame.transform.scale(background, (x, y))
        self.rect = self.bg_big.get_rect(left=0, top=0)

class chose_BG(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(chose_BG, self).__init__()
        background = pygame.image.load('source/chose.jpg').convert_alpha()
        self.bg_big = pygame.transform.scale(background, (x, y))
        self.rect = self.bg_big.get_rect(left=0, top=0)

class Shop_BG(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Shop_BG, self).__init__()
        background = pygame.image.load('source/shop.png').convert_alpha()
        self.bg_big = pygame.transform.scale(background, (x, y))
        self.rect = self.bg_big.get_rect(left=0, top=0)

class Job_BG(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Job_BG, self).__init__()
        background = pygame.image.load('source/job.png').convert_alpha()
        self.bg_big = pygame.transform.scale(background, (x, y))
        self.rect = self.bg_big.get_rect(left=0, top=0)
