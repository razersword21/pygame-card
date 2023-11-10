import pygame,sys
import random

from src.objects import *
from src.card_process import *
from src.params import *
from src.shop import *

special_deck = Special_card()
normal_deck = special_deck.normal_deck
high_level_deck = special_deck.high_level_deck

def choose_(win,font_list,rounds,person,new_card_deck):
    bg = BG(900, 600)
    choose_buff = ''
    choosing = True
    value,add_hp = 0,0
    chose_card = None
    
    add_hp = params.add_hp
    add_value = params.add_value
    if rounds % 10 == 0 and rounds != 0:
        add_hp = params.add_hp*2
        add_value = params.add_value*2       
    
    options = [add_hp,add_value]
    out_option = []
    chose_option = []
    out_card = []
    
    options.extend(new_card_deck)
    out_option = random.sample(options,k=3)
        
    while choosing:
        win.blit(bg.bg_big, bg.rect)
        menu_text = font_list[1].render("--選擇獎勵--", True, BLACK)
        win.blit(menu_text, (280, 100))
        
        shop_text = font_list[0].render("如果選擇跳過獎勵，關閉頁面將得到Money+150", True, BLACK)
        win.blit(shop_text, (20, 560))
        choose_btn1 = pygame.Rect(50, 240, 200, 300)
        pygame.draw.rect(win, WHITE , choose_btn1)
        choose_btn2 = pygame.Rect(350, 240, 200, 300)
        pygame.draw.rect(win, WHITE , choose_btn2)
        choose_btn3 = pygame.Rect(650, 240, 200, 300)
        pygame.draw.rect(win, WHITE , choose_btn3)
        rerurn_btn1 = pygame.Rect(790, 555, 70, 30)
        pygame.draw.rect(win, RED , rerurn_btn1)
        rerurn_text = font_list[0].render("跳過", True, BLACK)
        win.blit(rerurn_text, (795, 560))
        start_x = [100,400,700]
        for i,op in enumerate(out_option):
            if op == add_hp:
                choose_text1 = font_list[0].render("血量增加", True, BLACK)
                win.blit(choose_text1, (start_x[i], 300))
                choose_text1 = font_list[1].render("+"+str(add_hp), True, BLACK)
                win.blit(choose_text1, (start_x[i]+20, 400))
                chose_option.append('hp')
            elif op == add_value:
                choose_text2 = font_list[0].render("隨機屬性增強", True, BLACK)
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
                win.blit(choose_text3, (start_x[i]-20, 250))
                card_text1 = font_list[0].render(op.name, True, BLACK)
                win.blit(card_text1, (start_x[i], 290))
                card_text = font_list[0].render("Cost: "+str(op.cost), True, BLACK)
                win.blit(card_text, (start_x[i]-10, 330))
                card_text2 = font_list[0].render(op.special, True, BLACK)
                win.blit(card_text2, (start_x[i]-20, 370))
                chose_option.append('card')
                out_card.append(op)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                choosing = False
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]==1:
                pos = pygame.mouse.get_pos()
                if rerurn_btn1.collidepoint(pos):
                    choosing = False
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
                        if pos[0] >= 50 and pos[0] <= 250:
                            chose_card = out_card[0]
                        elif pos[0] >= 350 and pos[0] <= 550:
                            if len(out_card) <= 2:
                                chose_card = out_card[0]
                            else:
                                chose_card = out_card[1]
                        else:
                            if len(out_card) == 1:
                                chose_card = out_card[0]
                            elif len(out_card) == 2:
                                chose_card = out_card[1]
                            else:
                                chose_card = out_card[2]
                choosing = False
                
        pygame.display.flip()
    return choose_buff,value,chose_card,person