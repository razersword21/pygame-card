import pygame,sys
import random
from objects import *
from card_process import *
from choose import *
import time
import logging
logging.basicConfig(level=logging.INFO)
from game import *
from params import *

GAME_CONTROL = False

def main():
    global GAME_CONTROL
    pygame.init()
    pygame.display.set_caption('無限地牢')  # 遊戲標題
    win = pygame.display.set_mode((900, 600))  # 窗口尺寸
    hp_font = pygame.font.Font('font/ChenYuluoyan-Thin.ttf', 32)
    
    intro = Intro(900, 600)
    show_intro = True
    while show_intro:
        win.blit(intro.bg_big, intro.rect)

        start_btn = pygame.Rect(350, 555, 70, 30) 
        pygame.draw.rect(win, WHITE , start_btn)
        btn_text = hp_font.render("Start", True, RED)
        win.blit(btn_text, (355, 560))
        quit_btn = pygame.Rect(450, 555, 70, 30) 
        pygame.draw.rect(win, BLACK , quit_btn)
        quit_text = hp_font.render("Quit", True, WHITE)
        win.blit(quit_text, (455, 560))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start_btn.collidepoint(pos):
                    GAME_CONTROL = True
                    game_(win,hp_font,GAME_CONTROL)
                if quit_btn.collidepoint(pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()

if __name__ == '__main__':
    main()