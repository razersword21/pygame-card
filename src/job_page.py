import pygame,sys
import json
import logging
logging.basicConfig(level=logging.INFO)

from src.objects import *
from src.params import *

def chose_job(win,person):
    bg = job_BG(900, 600)
    job_chosing,check_job = True,False

    job_font = pygame.font.Font(params.Font, 50)
    base_font = pygame.font.Font(params.Font, 30)

    with open('source/rankings.json') as f:
        rank_list = json.load(f)
    out_dict = check_job_(rank_list)

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
            turn_index = pygame.image.load('source/mainrole_turn.png')
            win.blit(turn_index,(500,150))
            enemy_turn_index = pygame.image.load('source/enemy_turn.png')
            win.blit(enemy_turn_index,(800,150))
            st_y = 250
            for name,txt in params.player_value[person.main_job].items():
                match name:
                    case 'name':
                        name = '職業'
                    case 'max_hp':
                        name = '血量'
                    case 'max_de':
                        continue
                    case 'damage_b':
                        name = '傷害+'
                    case 'defense_b':
                        name = '護甲+'
                    case 'heal_b':
                        name = '治癒+'
                    case 'magic':
                        name = '魔力'
                    case 'money':
                        name = '錢幣'
                knight_text = base_font.render(name+' : '+str(txt), True, WHITE)
                win.blit(knight_text, (500, st_y))
                st_y+=40

            match person.main_job:
                case 1:
                    knight_img = pygame.image.load(job_image[1][person.role_index]).convert_alpha()
                    knight = pygame.transform.scale(knight_img, (200, 250))
                    win.blit(knight,(550,-20))
                    
                    knight_t = "帝國之盾\n從小接受騎士教育\n因此熟練劍盾使用\n但智力相對較低\n遇到挑戰動作單一\n初始專屬卡 - 神聖之盾\n獲得自身防禦buff*2\n的護盾".split('\n')
                    start_y = 250
                    for t in knight_t:
                        knight_text = base_font.render(t, True, WHITE)
                        win.blit(knight_text, (650, start_y))
                        start_y+=40
                case 2:
                    magic_img = pygame.image.load(job_image[2][person.role_index]).convert_alpha()
                    magic = pygame.transform.scale(magic_img, (200, 250))
                    win.blit(magic,(570,-20))
                    
                    knight_t = "賢者之父\n為帝國賢者的父親\n不要妄想如兒子般\n但至少智力比騎士高\n初始專屬卡 - 回魔\n兩回合MP+2".split('\n')
                    start_y = 250
                    for t in knight_t:
                        knight_text = base_font.render(t, True, WHITE)
                        win.blit(knight_text, (650, start_y))
                        start_y+=40
                case 3:
                    bow_img = pygame.image.load(job_image[3][person.role_index]).convert_alpha()
                    bow = pygame.transform.scale(bow_img, (300, 300))
                    win.blit(bow,(520,-20))
                    
                    knight_t = "普通的神箭手\n平常一直練習射箭\n所有人事物都是目標\n因為得罪太多人\n被趕來挑戰輪迴\n初始專屬卡 - 破甲箭\n無視防禦\n造成真實傷害".split('\n')
                    start_y = 250
                    for t in knight_t:
                        knight_text = base_font.render(t, True, WHITE)
                        win.blit(knight_text, (650, start_y))
                        start_y+=40
                case 5:
                    thief_img = pygame.image.load(job_image[5][person.role_index]).convert_alpha()
                    thief = pygame.transform.scale(thief_img, (250, 300))
                    win.blit(thief,(550,-20))
                    
                    knight_t = "沉迷賭博的盜賊\n不小心沉迷賭博之人\n所有動作充滿\n「隨機與竊取」\n初始專屬卡 - 竊取\n造成2傷害並隨機偷取\n0~30 Money".split('\n')
                    start_y = 250
                    for t in knight_t:
                        knight_text = base_font.render(t, True, WHITE)
                        win.blit(knight_text, (650, start_y))
                        start_y+=40
                case 6:
                    priest_img = pygame.image.load(job_image[6][person.role_index]).convert_alpha()
                    priest = pygame.transform.scale(priest_img, (250, 250))
                    win.blit(priest,(560,0))
                    
                    knight_t = "健身牧師-甲\n不要問為何血量如此\n一切都是平常的努力\n甚至攻擊都是基於\n血量與超出補血量\n初始專屬卡 - 當頭棒喝\n造成1+生命上限30%傷害".split('\n')
                    start_y = 250
                    for t in knight_t:
                        knight_text = base_font.render(t, True, WHITE)
                        win.blit(knight_text, (650, start_y))
                        start_y+=40

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                person.main_job = 4
                logging.info('恭喜你獲得隱藏職業！接下來的挑戰你成為 '+job_dict[person.main_job]+' 不會獲得任何專屬卡。')
                job_chosing = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and check_job and person.role_index<2:
                person.role_index+=1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and check_job and person.role_index>=1:
                person.role_index-=1
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]==1:
                pos = pygame.mouse.get_pos()
                if choose_btn1.collidepoint(pos):
                    person.main_job = 1                    
                    logging.info('你選擇成為 '+job_dict[person.main_job])
                    check_job = True
                    person.role_index = 0
                if choose_btn2.collidepoint(pos):
                    person.main_job = 2
                    logging.info('你選擇成為 '+job_dict[person.main_job])
                    check_job = True
                    person.role_index = 0
                if choose_btn3.collidepoint(pos):
                    person.main_job = 3
                    logging.info('你選擇成為 '+job_dict[person.main_job])
                    check_job = True
                    person.role_index = 0
                if choose_btn5.collidepoint(pos):
                    person.main_job = 5
                    logging.info('你選擇成為 '+job_dict[person.main_job])
                    check_job = True
                    person.role_index = 0
                if choose_btn6.collidepoint(pos):
                    person.main_job = 6
                    logging.info('你選擇成為 '+job_dict[person.main_job])
                    check_job = True
                    person.role_index = 0
                if rerurn_btn1.collidepoint(pos):
                    job_chosing = False
        pygame.display.flip()

def check_job_(rank_list):
    out_dict = {}
    for index,job in job_dict.items():
        if len(rank_list) > 0:
            for player in rank_list:
                if player['job'] == job:
                    if player['score'] > max_levels:
                        max_levels = player['score']
            out_dict[index] = max_levels
    return out_dict