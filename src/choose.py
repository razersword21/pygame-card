import pygame

from src.objects import *
from src.card_process import *
from src.params import *
from src.shop import *

def choose_(win,font_list,rounds,person,out_option):
    bg = chose_BG(900, 600)
    choose_buff = ''
    choosing = True
    value = 0
    chose_card = None
    add_hp = params.add_hp
    add_value = params.add_value
    if rounds % 10 == 0 and rounds != 0:
        add_hp = params.add_hp*2
        add_value = params.add_value*2
    chose_option = [None]*3
    out_card = []
    for i,op in enumerate(out_option):
        if op == add_hp:
            chose_option[i]='hp'
        elif op == add_value:
            chose_option[i]='all'
        else:
            chose_option[i]='card'
            out_card.append(op)

    while choosing:
        win.blit(bg.bg_big, bg.rect)
        menu_text = font_list[1].render("--選擇獎勵--", True, WHITE)
        win.blit(menu_text, (250, 100))
        
        shop_text = font_list[0].render("如果選擇跳過獎勵，將得到Money+150", True, WHITE)
        win.blit(shop_text, (20, 560))
        choose_btn1 = pygame.Rect(50, 240, 200, 300)
        pygame.draw.rect(win, WHITE , choose_btn1)
        choose_btn2 = pygame.Rect(350, 240, 200, 300)
        pygame.draw.rect(win, WHITE , choose_btn2)
        choose_btn3 = pygame.Rect(650, 240, 200, 300)
        pygame.draw.rect(win, WHITE , choose_btn3)
        rerurn_btn1 = pygame.Rect(790, 555, 70, 30)
        pygame.draw.rect(win, RED , rerurn_btn1)
        rerurn_text = font_list[0].render("返回", True, BLACK)
        win.blit(rerurn_text, (795, 560))
        start_x = [100,400,700]
        for i,op in enumerate(out_option):
            if op == add_hp:
                choose_text1 = font_list[1].render("血量", True, BLACK)
                choose_text2 = font_list[1].render("增加", True, BLACK)
                win.blit(choose_text1, (start_x[i]-10, 280))
                win.blit(choose_text2, (start_x[i]-10, 360))
                choose_text1 = font_list[1].render("+"+str(add_hp), True, BLACK)
                win.blit(choose_text1, (start_x[i]+10, 450))
            elif op == add_value:
                choose_text2 = font_list[0].render("以下屬性", True, BLACK)
                choose_text22 = font_list[0].render("隨機增強", True, BLACK)
                win.blit(choose_text2, (start_x[i], 270))
                win.blit(choose_text22, (start_x[i], 310))
                choose_text2_1 = font_list[0].render("傷害+1", True, BLACK)
                win.blit(choose_text2_1, (start_x[i]+10, 350))
                choose_text2_2 = font_list[0].render("防禦+1", True, BLACK)
                win.blit(choose_text2_2, (start_x[i]+10, 390))
                choose_text2_3 = font_list[0].render("治癒+1", True, BLACK)
                win.blit(choose_text2_3, (start_x[i]+10, 430))
                choose_text2_4 = font_list[0].render("魔力+1", True, BLACK)
                win.blit(choose_text2_4, (start_x[i]+10, 470))
            else:
                choose_text3 = font_list[0].render("增加特殊卡", True, BLACK)
                win.blit(choose_text3, (start_x[i]-20, 250))
                op.draw(win,0,start_x[i]+50,380,200,300)
                        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                choosing = False
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]==1:
                pos = pygame.mouse.get_pos()
                if rerurn_btn1.collidepoint(pos):
                    choosing = False
                if 50<=pos[0]<=250 and 240<=pos[1]<=540:
                    choose_buff = chose_option[0]
                if 350<=pos[0]<=550 and 240<=pos[1]<=540:
                    choose_buff = chose_option[1]
                if 650<=pos[0]<=850 and 240<=pos[1]<=540:
                    choose_buff = chose_option[2]
                
                match choose_buff:
                    case 'hp':
                        value = add_hp
                    case 'all':
                        value = add_value
                    case 'card':
                        if 50<=pos[0]<=250 and 240<=pos[1]<=540:
                            chose_card = out_card[0]
                        elif 350<=pos[0]<=550 and 240<=pos[1]<=540:
                            if len(out_card) <= 2:
                                chose_card = out_card[0]
                            else:
                                chose_card = out_card[1]
                        elif 650<=pos[0]<=850 and 240<=pos[1]<=540:
                            if len(out_card) == 1:
                                chose_card = out_card[0]
                            elif len(out_card) == 2:
                                chose_card = out_card[1]
                            else:
                                chose_card = out_card[2]
                choosing = False
        pygame.display.flip()
    return choose_buff,value,chose_card,person