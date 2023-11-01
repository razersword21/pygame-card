import pygame,sys
import logging
from objects import *
from card_process import *
from params import *
logging.basicConfig(level=logging.INFO)

def shop(win,font_list,person):
    bg = BG(900, 600)
    shop_activate = True
    
    while shop_activate:
        win.blit(bg.bg_big, bg.rect)
        menu_text = font_list[1].render("--商店--", True, BLACK)
        win.blit(menu_text, (300, 100))
        choose_btn1 = pygame.Rect(50, 240, 200, 300)
        pygame.draw.rect(win, WHITE , choose_btn1)
        choose_btn2 = pygame.Rect(350, 240, 200, 300)
        pygame.draw.rect(win, WHITE , choose_btn2)
        choose_btn3 = pygame.Rect(650, 240, 200, 300)
        pygame.draw.rect(win, WHITE , choose_btn3)
        rerurn_btn1 = pygame.Rect(790, 555, 70, 30)
        pygame.draw.rect(win, RED , rerurn_btn1)
        rerurn_text = font_list[0].render("Rerurn", True, BLACK)
        win.blit(rerurn_text, (795, 560))
        start_x = [100,400,700]
        shop_add_value = ['damage','defense','heal']
        for i,add_v in enumerate(shop_add_value):
            choose_text1 = font_list[0].render(add_v, True, BLACK)
            win.blit(choose_text1, (start_x[i], 300))
            choose_text1 = font_list[1].render("+ 1", True, BLACK)
            win.blit(choose_text1, (start_x[i]+20, 400))
            choose_text1 = font_list[0].render("Money: 300", True, BLACK)
            win.blit(choose_text1, (start_x[i], 450))
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shop_activate = False
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]==1:
                pos = pygame.mouse.get_pos()
                if (person.money - 300) >= 0: 
                    person.money -= 300
                    if pos[0] >= 50 and pos[0] <= 250:
                        person.damage_buff += 1
                        logging.warn('玩家 購買 傷害加成')
                    elif pos[0] >= 350 and pos[0] <= 550:
                        person.defense_buff += 1
                        logging.warn('玩家 購買 防禦加成')
                    else:
                        person.heal_buff += 1
                        logging.warn('玩家 購買 治癒加成')
        pygame.display.flip()
    return person