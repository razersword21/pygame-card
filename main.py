import pygame,sys
import pygame.locals
import keyboard
import ctypes

from src.objects import *
from src.card_process import *
from src.choose import *
from src.game import *
from src.params import *
from src.input_name import *
from src.rank import *

GAME_CONTROL = False

def main():
    global GAME_CONTROL
    pygame.init()
    pygame.display.set_caption('數值-無限地牢')  # 遊戲標題
    win = pygame.display.set_mode((900, 600))  # 窗口尺寸
    
    base_font = pygame.font.Font(params.Font, 32)
    title_font = pygame.font.Font(params.Font, 80)
    all_font = [base_font,title_font]
    intro = Intro(900, 600)
    show_intro = True
    enemy = Enemy(params.init_max_hp,params.init_max_de,params.init_max_magic)
    main_role = Main_role(params.init_max_hp,params.init_max_de,params.init_max_magic,params.money)

    user32 = ctypes.WinDLL('user32', use_last_error=True)
    curr_window = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
    klid = user32.GetKeyboardLayout(thread_id)
    lid = klid & (2**16 - 1)
    lid_hex = hex(lid)
    
    while show_intro:
        win.blit(intro.bg_big, intro.rect)

        start_btn = pygame.Rect(300, 555, 70, 30) 
        pygame.draw.rect(win, RED , start_btn)
        btn_text = base_font.render("Start", True, BLACK)
        win.blit(btn_text, (305, 560))

        rank_btn = pygame.Rect(400, 555, 70, 30) 
        pygame.draw.rect(win, YELLOW , rank_btn)
        rank_text = base_font.render("Rank", True, BLACK)
        win.blit(rank_text, (405, 560))

        quit_btn = pygame.Rect(500, 555, 70, 30) 
        pygame.draw.rect(win, BLACK , quit_btn)
        quit_text = base_font.render("Quit", True, WHITE)
        win.blit(quit_text, (505, 560))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start_btn.collidepoint(pos):
                    if lid_hex == '0x404':
                        keyboard.send('alt+shift')
                    input_name(win,main_role)
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