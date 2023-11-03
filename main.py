import pygame,sys

from objects import *
from card_process import *
from choose import *
from game import *
from params import *
from input_name import *

GAME_CONTROL = False

def main():
    global GAME_CONTROL
    pygame.init()
    pygame.display.set_caption('數值-無限地牢')  # 遊戲標題
    win = pygame.display.set_mode((900, 600))  # 窗口尺寸
    
    base_font = pygame.font.Font('font/ChenYuluoyan-Thin.ttf', 32)
    title_font = pygame.font.Font('font/ChenYuluoyan-Thin.ttf', 80)
    all_font = [base_font,title_font]
    intro = Intro(900, 600)
    show_intro = True
    enemy = Enemy(params.init_max_hp,params.init_max_de,params.init_max_magic)
    main_role = Main_role(params.init_max_hp,params.init_max_de,params.init_max_magic,params.money)

    while show_intro:
        win.blit(intro.bg_big, intro.rect)

        start_btn = pygame.Rect(350, 555, 70, 30) 
        pygame.draw.rect(win, RED , start_btn)
        btn_text = base_font.render("Start", True, BLACK)
        win.blit(btn_text, (355, 560))
        quit_btn = pygame.Rect(450, 555, 70, 30) 
        pygame.draw.rect(win, BLACK , quit_btn)
        quit_text = base_font.render("Quit", True, WHITE)
        win.blit(quit_text, (455, 560))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start_btn.collidepoint(pos):
                    input_name(win,main_role)
                    if len(main_role.name) > 0:
                        GAME_CONTROL = True
                        game_(win,all_font,GAME_CONTROL,main_role,enemy)
                if quit_btn.collidepoint(pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()

if __name__ == '__main__':
    main()