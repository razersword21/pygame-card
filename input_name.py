import pygame,sys
import random
from objects import *

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
        title_font = pygame.font.Font('font/ChenYuluoyan-Thin.ttf', 80)
        base_font = pygame.font.Font('font/ChenYuluoyan-Thin.ttf', 50)
        menu_text = title_font.render("輸入玩家名字\n   (限英文)", True, BLACK)
        win.blit(menu_text, (280, 70))

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
        pygame.display.flip()