import pygame

from src.objects import *
from src.choose import *

def win_surface(win,font_list,rounds,main_role,new_card_deck):
    bg = BG(900, 600)
    show_win_surface = True
    chose_buff = ''
    add_value = 0
    new_card = None

    add_hp = params.add_hp
    add_value = params.add_value
    if rounds % 10 == 0 and rounds != 0:
        add_hp = params.add_hp*2
        add_value = params.add_value*2       
    
    options = [add_hp,add_value]
    options.extend(new_card_deck)
    out_option = random.sample(options,k=3)
    
    while show_win_surface:
        win.blit(bg.bg_big, bg.rect)

        menu_text = font_list[1].render("--勝利--", True, BLACK)
        win.blit(menu_text, (325, 100))

        choose_btn = pygame.Rect(100, 200, 400, 150)
        pygame.draw.rect(win, WHITE , choose_btn)
        choose_text = font_list[1].render("選擇獎勵", True, BLACK)
        win.blit(choose_text, (150, 250))
        shop_btn = pygame.Rect(100, 400, 400, 150)
        pygame.draw.rect(win, YELLOW , shop_btn)
        choose_text = font_list[1].render("商店", True, BLACK)
        win.blit(choose_text, (250, 450))
        next_rounds_btn = pygame.Rect(550, 200, 250, 350)
        pygame.draw.rect(win, RED , next_rounds_btn)
        choose_text = font_list[1].render("下個\n回合", True, BLACK)
        win.blit(choose_text, (625, 300))
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_win_surface = False
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]==1:
                pos = pygame.mouse.get_pos()
                if choose_btn.collidepoint(pos):
                    chose_buff,add_value,new_card,main_role = choose_(win,font_list,rounds,main_role,out_option)
                if shop_btn.collidepoint(pos):
                    main_role = shop(win,font_list,main_role)
                if next_rounds_btn.collidepoint(pos):
                    show_win_surface = False
        
        pygame.display.update()
    return chose_buff,add_value,new_card,main_role