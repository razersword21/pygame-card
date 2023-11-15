import pygame,sys
import logging
logging.basicConfig(level=logging.INFO)

from src.objects import *
from src.params import *

def chose_job(win,person):
    bg = job_BG(900, 600)
    job_chosing,check_job = True,False
    job_font = pygame.font.Font(params.Font, 50)
    base_font = pygame.font.Font(params.Font, 32)

    while job_chosing:
        win.blit(bg.bg_big, bg.rect)
        choose_btn1 = pygame.Rect(30, 100, 130, 80)
        pygame.draw.rect(win, BLUE , choose_btn1)
        knight_text = job_font.render("騎士", True, WHITE)
        win.blit(knight_text, (55, 115))
        choose_btn2 = pygame.Rect(180, 100, 130, 80)
        pygame.draw.rect(win, PURPLE , choose_btn2)
        knight_text = job_font.render("魔法師", True, WHITE)
        win.blit(knight_text, (180, 115))
        choose_btn3 = pygame.Rect(330, 100, 130, 80)
        pygame.draw.rect(win, GREEN , choose_btn3)
        knight_text = job_font.render("弓箭手", True, BLACK)
        win.blit(knight_text, (350, 115))
        rerurn_btn1 = pygame.Rect(790, 555, 100, 40)
        pygame.draw.rect(win, RED , rerurn_btn1)
        choose_btn5 = pygame.Rect(30, 240, 130, 80)
        pygame.draw.rect(win, Coconut_Brown , choose_btn5)
        knight_text = job_font.render("盜賊", True, WHITE)
        win.blit(knight_text, (55, 260))
        choose_btn6 = pygame.Rect(180, 240, 130, 80)
        pygame.draw.rect(win, YELLOW , choose_btn6)
        knight_text = job_font.render("牧師", True, BLACK)
        win.blit(knight_text, (200, 260))
        rerurn_text = base_font.render("前往挑戰", True, BLACK)
        win.blit(rerurn_text, (790, 560))
        
        if check_job:
            match person.main_job:
                case 1:
                    knight_img = pygame.image.load(job_image[1]).convert_alpha()
                    knight = pygame.transform.scale(knight_img, (250, 250))
                    win.blit(knight,(530,-20))
                    knight_text = base_font.render("   騎士\n血量: 25\n魔力: 2\nDamage: 1\nDefense: 2\nHeal: 0\nMoney: 100", True, WHITE)
                    win.blit(knight_text, (500, 250))
                    knight_text = base_font.render("帝國之盾\n從小接受騎士教育\n因此熟練劍盾使用\n但智力相對較低\n遇到挑戰時的動作單一\n擁有初始專屬卡 - 神聖之盾\n獲得自身防禦buff*2\n的護盾", True, WHITE)
                    win.blit(knight_text, (625, 250))
                case 2:
                    magic_img = pygame.image.load(job_image[2]).convert_alpha()
                    magic = pygame.transform.scale(magic_img, (200, 250))
                    win.blit(magic,(550,-20))
                    magic_text = base_font.render("  魔法師\n血量: 15\n魔力: 4\nDamage: 0\nDefense: 0\nHeal: 1\nMoney: 50", True, WHITE)
                    win.blit(magic_text, (500, 250))
                    magic_text = base_font.render("賢者之父\n為帝國賢者的父親\n不要妄想有兒子般的能力\n你只是因為兒子而受尊敬\n至少智力比騎士高\n擁有初始專屬卡 - 回魔\n兩回合MP+2", True, WHITE)
                    win.blit(magic_text, (625, 250))
                case 3:
                    bow_img = pygame.image.load(job_image[3]).convert_alpha()
                    bow = pygame.transform.scale(bow_img, (300, 300))
                    win.blit(bow,(520,-20))
                    bow_text = base_font.render("  弓箭手\n血量: 20\n魔力: 3\nDamage: 1\nDefense: 0\nHeal: 0\nMoney: 0", True, WHITE)
                    win.blit(bow_text, (500, 250))
                    bow_text = base_font.render("普通的神箭手\n平常一直練習射箭\n帝國內所有人事物\n都是你的目標\n因為得罪太多人\n被趕來挑戰輪迴\n擁有初始專屬卡 - 破甲箭\n無視防禦\n造成真實傷害", True, WHITE)
                    win.blit(bow_text, (625, 250))
                case 5:
                    thief_img = pygame.image.load(job_image[3]).convert_alpha()
                    thief = pygame.transform.scale(thief_img, (300, 300))
                    win.blit(thief,(520,-20))
                    thief_text = base_font.render("  盜賊\n血量: 20\n魔力: 3\nDamage: 2\nDefense: -1\nHeal: 0\nMoney: 25", True, WHITE)
                    win.blit(thief_text, (500, 250))
                    thief_text = base_font.render("沉迷賭博的盜賊\n作為不小心\n沉迷賭博之人\n同時作為盜賊\n所有動作充滿\n「隨機與竊取」\n擁有初始專屬卡 - 竊取\n造成2傷害\n並隨機偷取對方\n0~30 Money", True, WHITE)
                    win.blit(thief_text, (625, 250))
                case 6:
                    priest_img = pygame.image.load(job_image[3]).convert_alpha()
                    priest = pygame.transform.scale(priest_img, (300, 300))
                    win.blit(priest,(520,-20))
                    priest_text = base_font.render("  牧師\n血量: 30\n魔力: 3\nDamage: 0\nDefense: 0\nHeal: 2\nMoney: 0", True, WHITE)
                    win.blit(priest_text, (500, 250))
                    priest_text = base_font.render("健身牧師-甲\n不要問為何血量如此\n一切都是平常的努力\n甚至攻擊都是基於\n血量上限與補血量\n擁有初始專屬卡 - 當頭棒喝\n造成1+生命上限30%傷害", True, WHITE)
                    win.blit(priest_text, (625, 250))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                person.main_job = 4
                logging.info('恭喜你獲得隱藏職業！接下來的挑戰你成為 '+job_dict[person.main_job]+' 不會獲得任何專屬卡。')
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
                if choose_btn5.collidepoint(pos):
                    person.main_job = 5
                    logging.info('你選擇成為 '+job_dict[person.main_job])
                    check_job = True
                if choose_btn6.collidepoint(pos):
                    person.main_job = 6
                    logging.info('你選擇成為 '+job_dict[person.main_job])
                    check_job = True
                if rerurn_btn1.collidepoint(pos):
                    job_chosing = False
        pygame.display.flip()