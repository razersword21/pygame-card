import pygame,sys
import random
from objects import *
from card_process import *
from params import *

special_deck = Special_card()
normal_deck = special_deck.normal_deck
high_level_deck = special_deck.high_level_deck
param = params

def choose_normal(win,font_list,rounds):
    bg = BG(900, 600)
    choose_buff = ''
    choosing = True
    value,add_hp = 0,0
    chose_card = None
    if rounds % 5 != 0:
        new_card = random.choice(normal_deck)
        add_hp = param.add_hp
        add_value = param.add_value
    else:
        add_hp = param.add_hp*2
        add_value = param.add_value*2
        new_card = random.choice(high_level_deck)
    
    options = [add_hp,add_value,new_card]
    out_option = []
    chose_option = []
    for i in range(3):
        ops = random.choice(options)
        out_option.append(ops)
    
    while choosing:
        win.blit(bg.bg_big, bg.rect)
        menu_text = font_list[1].render("--選擇獎勵--", True, BLACK)
        win.blit(menu_text, (280, 100))

        choose_btn1 = pygame.Rect(50, 240, 200, 300)
        pygame.draw.rect(win, WHITE , choose_btn1)
        choose_btn2 = pygame.Rect(350, 240, 200, 300)
        pygame.draw.rect(win, WHITE , choose_btn2)
        choose_btn3 = pygame.Rect(650, 240, 200, 300)
        pygame.draw.rect(win, WHITE , choose_btn3)
        start_x = [100,400,680]
        for i,op in enumerate(out_option):
            if op == add_hp:
                choose_text1 = font_list[0].render("血量增加", True, BLACK)
                win.blit(choose_text1, (start_x[i]-20, 300))
                choose_text1 = font_list[1].render("+"+str(add_hp), True, BLACK)
                win.blit(choose_text1, (start_x[i]+20, 400))
                chose_option.append('hp')
            elif op == add_value:
                choose_text2 = font_list[0].render("全屬性增強", True, BLACK)
                win.blit(choose_text2, (start_x[i]-10, 300))
                choose_text2_1 = font_list[0].render("傷害+1", True, BLACK)
                win.blit(choose_text2_1, (start_x[i], 350))
                choose_text2_2 = font_list[0].render("防禦+1", True, BLACK)
                win.blit(choose_text2_2, (start_x[i], 400))
                choose_text2_3 = font_list[0].render("治癒+1", True, BLACK)
                win.blit(choose_text2_3, (start_x[i], 450))
                chose_option.append('all')
            else:
                choose_text3 = font_list[0].render("增加特殊卡", True, BLACK)
                win.blit(choose_text3, (start_x[i], 300))
                card_text1 = font_list[0].render(new_card.name, True, BLACK)
                win.blit(card_text1, (start_x[i], 350))
                card_text2 = font_list[0].render(new_card.special, True, BLACK)
                win.blit(card_text2, (start_x[i], 400))
                chose_option.append('card')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                choosing = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if choose_btn1.collidepoint(pos):
                    choose_buff = chose_option[0]
                elif choose_btn2.collidepoint(pos):
                    choose_buff = chose_option[1]
                elif choose_btn3.collidepoint(pos):
                    choose_buff = chose_option[2]
                match choose_buff:
                    case 'hp':
                        value = add_hp
                    case 'all':
                        value = add_value
                    case 'card':
                        chose_card = new_card
                choosing = False
        pygame.display.flip()
    return choose_buff,value,chose_card