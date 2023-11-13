import pygame,sys
import logging
logging.basicConfig(level=logging.INFO)

from src.objects import *
from src.params import *

def chose_job(win,person):
    bg = shop_BG(900, 600)
    job_chosing = True
    base_font = pygame.font.Font(params.Font, 32)
    while job_chosing:
        win.blit(bg.bg_big, bg.rect)
        choose_btn1 = pygame.Rect(50, 50, 200, 475)
        pygame.draw.rect(win, WHITE , choose_btn1)
        choose_btn2 = pygame.Rect(350, 50, 200, 475)
        pygame.draw.rect(win, WHITE , choose_btn2)
        choose_btn3 = pygame.Rect(650, 50, 200, 475)
        pygame.draw.rect(win, WHITE , choose_btn3)
        
        knight_img = pygame.image.load('source/player/knight.png').convert_alpha()
        knight = pygame.transform.scale(knight_img, (150, 150))
        win.blit(knight,(75,70))
        magic_img = pygame.image.load('source/player/knight.png').convert_alpha()
        magic = pygame.transform.scale(magic_img, (150, 150))
        win.blit(magic,(375,70))
        bow_img = pygame.image.load('source/player/knight.png').convert_alpha()
        bow = pygame.transform.scale(bow_img, (150, 150))
        win.blit(bow,(675,70))

        knight_text = base_font.render("   騎士\n血量: 25\n魔力: 2\nDamage: 2\nDefense: 2\nHeal: 0\nMoney: 100", True, BLACK)
        win.blit(knight_text, (100, 250))
        magic_text = base_font.render("  魔法師\n血量: 15\n魔力: 4\nDamage: 0\nDefense: 0\nHeal: 1\nMoney: 0", True, BLACK)
        win.blit(magic_text, (400, 250))
        bow_text = base_font.render("  弓箭手\n血量: 20\n魔力: 3\nDamage: 1\nDefense: 0\nHeal: 0\nMoney: 50", True, BLACK)
        win.blit(bow_text, (700, 250))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                person.main_job = 4
                logging.info('你選擇成為 '+job_dict[person.main_job])
                job_chosing = False
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]==1:
                pos = pygame.mouse.get_pos()
                if 50<=pos[0]<=250  and 50<=pos[1]<=525:
                    person.main_job = 1                    
                    job_chosing = False
                    logging.info('你選擇成為 '+job_dict[person.main_job])
                elif 350<=pos[0]<=550 and 50<=pos[1]<=525:
                    person.main_job = 2
                    logging.info('你選擇成為 '+job_dict[person.main_job])
                    job_chosing = False
                elif 650<=pos[0]<=850 and 50<=pos[1]<=525:
                    person.main_job = 3
                    logging.info('你選擇成為 '+job_dict[person.main_job])
                    job_chosing = False
        pygame.display.flip()