import pygame,sys
import logging
logging.basicConfig(level=logging.INFO)

from src.objects import *
from src.card_process import *
from src.params import *

def shop(win,font_list,person):
    bg = shop_BG(900, 600)
    shop_activate = True
    
    while shop_activate:
        win.blit(bg.bg_big, bg.rect)
        Money_text = font_list[0].render("Money: "+str(person.money), True, Coconut_Brown)
        win.blit(Money_text, (780, 20))
        choose_btn1 = pygame.Rect(50, 240, 200, 270)
        pygame.draw.rect(win, WHITE , choose_btn1)
        choose_btn2 = pygame.Rect(350, 240, 200, 270)
        pygame.draw.rect(win, WHITE , choose_btn2)
        choose_btn3 = pygame.Rect(650, 240, 200, 270)
        pygame.draw.rect(win, WHITE , choose_btn3)
        rerurn_btn1 = pygame.Rect(790, 555, 70, 30)
        pygame.draw.rect(win, RED , rerurn_btn1)
        rerurn_text = font_list[0].render("返回", True, BLACK)
        win.blit(rerurn_text, (795, 555))
        start_x = [100,400,700]
        shop_add_value = ['Damage','Defense','Heal']
        for i,add_v in enumerate(shop_add_value):
            choose_text1 = font_list[1].render(add_v, True, BLACK)
            if i < 2:
                win.blit(choose_text1, (start_x[i]-30, 270))
            else:
                win.blit(choose_text1, (start_x[i], 270))
            choose_text1 = font_list[1].render("+ 1", True, BLACK)
            win.blit(choose_text1, (start_x[i]+20, 335))
            choose_text1 = font_list[0].render("Money cost: 300", True, BLACK)
            win.blit(choose_text1, (start_x[i]-20, 420))
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shop_activate = False
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]==1:
                pos = pygame.mouse.get_pos()
                if (person.money - 300) >= 0: 
                    person.money -= 300
                    if pos[0] >= 50 and pos[0] <= 250  and 240<=pos[1]<=540:
                        person.damage_buff += 1
                        logging.warn(person.name+' 購買 傷害加成')
                    elif pos[0] >= 350 and pos[0] <= 550 and 240<=pos[1]<=540:
                        person.defense_buff += 1
                        logging.warn(person.name+' 購買 防禦加成')
                    elif 650<=pos[0]<=850 and 240<=pos[1]<=540:
                        if 240<=pos[1]<=540:
                            person.heal_buff += 1
                            logging.warn(person.name+' 購買 治癒加成')
                else:
                    logging.warn('太窮了！買不起....QAQ')
                if rerurn_btn1.collidepoint(pos):
                    shop_activate = False
        pygame.display.flip()
    return person