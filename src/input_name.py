import pygame,sys

from src.objects import *
from src.params import *

def input_name(win,main_role):
    bg = BG(900, 600)
    inputing = True
    color_inactive = BLACK
    color_active = RED
    color = color_inactive
    text = ""
    active = False
    
    while inputing:
        win.blit(bg.bg_big, bg.rect)
        title_font = pygame.font.Font(params.Font, 80)
        base_font = pygame.font.Font(params.Font, 40)
        menu_text = title_font.render("輸入玩家名字", True, BLACK)
        menu_text2 = title_font.render("(限英文)", True, BLACK)
        win.blit(menu_text, (280, 70))
        win.blit(menu_text2, (320, 160))

        input_box = pygame.Rect(350, 275, 200, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inputing = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = True if input_box.collidepoint(event.pos) else False
                # Change the current color of the input box
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print("玩家姓名: ",text)
                        main_role.name = text
                        inputing = False
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        
        text_surface = base_font.render(text, True, color)
        input_box_width = max(200, text_surface.get_width()+10)
        input_box.w = input_box_width
        input_box.center = (900/2, 600/2)
        win.blit(text_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(win, color, input_box, 3)
        
        knight_t = "說明 :\n1.攻擊力=玩家加成數值+卡牌傷害(防禦和治癒相同，\n         甚至buff與debuff都會加上加成數值)\n2.商店可購買加成屬性\n3.每次打贏敵人可選擇獎勵".split('\n')
        start_y = 375
        for t in knight_t:
            knight_text = base_font.render(t, True, WHITE)
            win.blit(knight_text, (100, start_y))
            start_y+=40

        pygame.display.flip()