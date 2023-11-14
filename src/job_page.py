import pygame,sys
import logging
logging.basicConfig(level=logging.INFO)

from src.objects import *
from src.params import *

def chose_job(win,person):
    bg = BG(900, 600)
    job_chosing,check_job = True,False
    job_font = pygame.font.Font(params.Font, 50)
    base_font = pygame.font.Font(params.Font, 32)

    while job_chosing:
        win.blit(bg.bg_big, bg.rect)
        choose_btn1 = pygame.Rect(50, 100, 130, 80)
        pygame.draw.rect(win, BLUE , choose_btn1)
        knight_text = job_font.render("騎士", True, WHITE)
        win.blit(knight_text, (75, 115))
        choose_btn2 = pygame.Rect(200, 100, 130, 80)
        pygame.draw.rect(win, PURPLE , choose_btn2)
        knight_text = job_font.render("魔法師", True, WHITE)
        win.blit(knight_text, (200, 115))
        choose_btn3 = pygame.Rect(350, 100, 130, 80)
        pygame.draw.rect(win, GREEN , choose_btn3)
        knight_text = job_font.render("弓箭手", True, BLACK)
        win.blit(knight_text, (370, 115))
        rerurn_btn1 = pygame.Rect(790, 555, 100, 40)
        pygame.draw.rect(win, RED , rerurn_btn1)
        rerurn_text = base_font.render("前往挑戰", True, BLACK)
        win.blit(rerurn_text, (790, 560))
        
        if check_job:
            match person.main_job:
                case 1:
                    knight_img = pygame.image.load(job_image[1]).convert_alpha()
                    knight = pygame.transform.scale(knight_img, (150, 150))
                    win.blit(knight,(650,100))
                    knight_text = base_font.render("   騎士\n血量: 25\n魔力: 2\nDamage: 2\nDefense: 2\nHeal: 0\nMoney: 100", True, BLACK)
                    win.blit(knight_text, (500, 250))
                    knight_text = base_font.render("帝國之盾\n從小接受騎士教育\n因此熟練劍盾使用\n但智力相對較低\n遇到挑戰時的動作單一\n擁有專屬卡 - 神聖之盾\n獲得自身防禦buff*2\n的護盾", True, BLACK)
                    win.blit(knight_text, (625, 250))
                case 2:
                    magic_img = pygame.image.load(job_image[2]).convert_alpha()
                    magic = pygame.transform.scale(magic_img, (150, 150))
                    win.blit(magic,(650,70))
                    magic_text = base_font.render("  魔法師\n血量: 15\n魔力: 4\nDamage: 0\nDefense: 0\nHeal: 1\nMoney: 50", True, BLACK)
                    win.blit(magic_text, (500, 250))
                    magic_text = base_font.render("賢者之父\n為帝國賢者的父親\n不要妄想有兒子般的能力\n你只是因為兒子而受尊敬\n至少智力比騎士高\n擁有專屬卡 - 回魔\n兩回合MP+2", True, BLACK)
                    win.blit(magic_text, (625, 250))
                case 3:
                    bow_img = pygame.image.load(job_image[3]).convert_alpha()
                    bow = pygame.transform.scale(bow_img, (150, 150))
                    win.blit(bow,(650,70))
                    bow_text = base_font.render("  弓箭手\n血量: 20\n魔力: 3\nDamage: 1\nDefense: 0\nHeal: 0\nMoney: 0", True, BLACK)
                    win.blit(bow_text, (500, 250))
                    bow_text = base_font.render("普通的神箭手\n平常一直練習射箭\n帝國內所有人事物\n都是你的目標\n因為得罪太多人\n被趕來挑戰輪迴\n擁有專屬卡 - 破盾\n消除敵人所有護盾值", True, BLACK)
                    win.blit(bow_text, (625, 250))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                person.main_job = 4
                logging.info('恭喜你獲得隱藏職業！接下來的挑戰你成為 '+job_dict[person.main_job])
                job_chosing = False
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]==1:
                pos = pygame.mouse.get_pos()
                if choose_btn1.collidepoint(pos):
                    person.main_job = 1                    
                    logging.info('你選擇成為 '+job_dict[person.main_job])
                    check_job = True
                if choose_btn2.collidepoint(pos):
                    person.main_job = 2
                    logging.info('你選擇成為 '+job_dict[person.main_job])
                    check_job = True
                if choose_btn3.collidepoint(pos):
                    person.main_job = 3
                    logging.info('你選擇成為 '+job_dict[person.main_job])
                    check_job = True
                if rerurn_btn1.collidepoint(pos):
                    job_chosing = False
        pygame.display.flip()