import pygame,sys
import pygame.locals

from src.objects import *
from src.card_process import *
from src.choose import *
from src.game import *
from src.params import *
from src.input_name import *
from src.rank import *
from src.job_page import *

GAME_CONTROL = False

def main():
    global GAME_CONTROL
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("source/bg_music.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(loops=-1)
    pygame.display.set_caption('數值-無限輪迴 ( Numerical value-infinite reincarnation )')  # 遊戲標題
    win = pygame.display.set_mode((900, 600))  # 窗口尺寸
    clock = pygame.time.Clock()
    
    base_font = pygame.font.Font(params.Font, 32)
    title_font = pygame.font.Font(params.Font, 80)
    btn_font = pygame.font.Font(params.Font, 50)
    all_font = [base_font,title_font]
    intro = Intro(900, 600)
    intro_animation = Intro_animation(300,300)
    show_intro,show_animation = True,True
    enemy = Enemy(params.enemy_max_hp,params.enemy_max_de,params.enemy_max_magic)
    main_role = Main_role(params.init_max_hp,params.init_max_de,params.init_max_magic,params.money)

    while show_intro:
        if show_animation:
            intro_animation.fadeout_animation(win,clock,a=255)
            show_animation = False
        win.blit(intro.bg_big, intro.rect)

        start_btn = pygame.Rect(250, 530, 130, 50) 
        pygame.draw.rect(win, RED , start_btn)
        btn_text = btn_font.render("Start", True, BLACK)
        win.blit(btn_text, (270, 530))

        rank_btn = pygame.Rect(400, 530, 130, 50) 
        pygame.draw.rect(win, YELLOW , rank_btn)
        rank_text = btn_font.render("排名榜", True, BLACK)
        win.blit(rank_text, (405, 530))

        quit_btn = pygame.Rect(550, 530, 130, 50) 
        pygame.draw.rect(win, BLACK , quit_btn)
        quit_text = btn_font.render("Quit", True, WHITE)
        win.blit(quit_text, (575, 530))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start_btn.collidepoint(pos):
                    input_name(win,main_role)
                    chose_job(win,main_role)
                    if len(main_role.name) > 0:
                        GAME_CONTROL = True
                        game_(win,all_font,GAME_CONTROL,main_role,enemy)
                if rank_btn.collidepoint(pos): 
                    rank_page(win)
                if quit_btn.collidepoint(pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()

if __name__ == '__main__':
    main()