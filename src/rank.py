import pygame,sys
import json
from src.objects import *
from src.params import *

def rank_page(win):
    bg = BG(900, 600)
    ranking = True
    with open('source/rankings.json') as f:
        rank_list = json.load(f)
    rank_list = sorted(rank_list, key=lambda k: k['score'], reverse=True)
    if len(rank_list) > 9:
        rank_list.pop(-1)
    while ranking:
        win.blit(bg.bg_big, bg.rect)
        base_font = pygame.font.Font(params.Font, 32)
        title_font = pygame.font.Font(params.Font, 80)
        menu_text = title_font.render("排名榜", True, BLACK)
        win.blit(menu_text, (350, 10))

        return_btn = pygame.Rect(800, 560, 70, 30) 
        pygame.draw.rect(win, RED , return_btn)
        return_text = base_font.render("返回", True, BLACK)
        win.blit(return_text, (805, 560))

        name_text = base_font.render("姓名", True, BLACK)
        job_text = base_font.render("職業", True, BLACK)
        score_text = base_font.render("關卡(Rounds)", True, BLACK)
        win.blit(name_text, (150, 100))
        win.blit(job_text, (450, 100))
        win.blit(score_text, (650, 100))

        y = 150 
        for player in rank_list:
            player_name_text = player['name']
            player_job = player['job']
            player_score_text = str(player['score']) + " 關"  
            name_surf = base_font.render(player_name_text, True, PURPLE)
            job_surf = base_font.render(player_job, True, PURPLE)
            score_surf = base_font.render(player_score_text, True, PURPLE)
            win.blit(name_surf, (150, y))
            win.blit(job_surf, (450, y))
            win.blit(score_surf, (675, y))
            y += 50

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ranking = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if return_btn.collidepoint(pos):
                    ranking = False
        pygame.display.flip()