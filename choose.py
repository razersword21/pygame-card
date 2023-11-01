import pygame,sys
import random
from objects import *
from card_process import *
from params import *

special_deck = Special_card()
normal_deck = special_deck.normal_deck
high_level_deck = special_deck.high_level_deck
param = params

def choose_normal(win,FONT,rounds):
    bg = BG(900, 600)
    choose_buff = ''
    choosing = True
    value = 0
    
    if rounds % 5 != 0:
        new_card = random.choice(normal_deck)
        add_hp = param.add_hp
        add_value = param.add_value
    else:
        add_hp = param.add_hp*2
        add_value = param.add_value*2
        new_card = random.choice(high_level_deck)
    
    while choosing:
        win.blit(bg.bg_big, bg.rect)
        menu_text = FONT.render("選擇獎勵", True, BLACK)
        win.blit(menu_text, (380, 100))
        choose_btn1 = pygame.Rect(50, 240, 200, 300)
        pygame.draw.rect(win, WHITE , choose_btn1)
        choose_text1 = FONT.render("血量增加", True, BLACK)
        win.blit(choose_text1, (80, 300))
        choose_text1 = FONT.render("+"+str(add_hp), True, BLACK)
        win.blit(choose_text1, (100, 400))
        choose_btn2 = pygame.Rect(350, 240, 200, 300)
        pygame.draw.rect(win, WHITE , choose_btn2)
        choose_text1 = FONT.render("全屬性增強", True, BLACK)
        win.blit(choose_text1, (400, 300))
        choose_text1 = FONT.render("傷害+1", True, BLACK)
        win.blit(choose_text1, (400, 350))
        choose_text1 = FONT.render("防禦+1", True, BLACK)
        win.blit(choose_text1, (400, 400))
        choose_text1 = FONT.render("治癒+1", True, BLACK)
        win.blit(choose_text1, (400, 450))
        
        choose_btn3 = pygame.Rect(650, 240, 200, 300)
        pygame.draw.rect(win, WHITE , choose_btn3)
        choose_text1 = FONT.render("增加特殊卡", True, BLACK)
        win.blit(choose_text1, (680, 300))
        card_text1 = FONT.render(new_card.name, True, BLACK)
        win.blit(card_text1, (700, 350))
        card_text2 = FONT.render(new_card.special, True, BLACK)
        win.blit(card_text2, (655, 420))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                choosing = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if choose_btn1.collidepoint(pos):
                    choose_buff = 'hp'
                    value = add_hp
                    choosing = False
                elif choose_btn2.collidepoint(pos):
                    choose_buff = 'all'
                    value = add_value
                    choosing = False
                elif choose_btn3.collidepoint(pos):
                    choose_buff = 'card'
                    new_card = new_card
                    choosing = False
        pygame.display.flip()
    return choose_buff,value,new_card