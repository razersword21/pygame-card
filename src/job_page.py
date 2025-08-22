import pygame,sys
import json
import logging
logging.basicConfig(level=logging.INFO)

from src.objects import *
from src.params import *
from src.config import *

class JobPage:
    """職業選擇頁面類"""
    def __init__(self, window_surface, main_role):
        self.window = window_surface
        self.person = main_role
        self.config = GameConfig()
        self.colors = Colors()
        self.bg = Job_BG(self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT)
        self.fonts = {
            'job': pygame.font.Font(params.Font, 50),
            'base': pygame.font.Font(params.Font, 30)
        }

        self.job_chosing = True
        self.check_job = False
        self.rank_list = self.load_rankings()

        self.buttons = {
            'knight': (pygame.Rect(30, 100, 130, 80), '騎士', BLUE, WHITE, 1),
            'mage': (pygame.Rect(180, 100, 130, 80), '魔法師', PURPLE, WHITE, 2),
            'archer': (pygame.Rect(330, 100, 130, 80), '弓箭手', GREEN, BLACK, 3),
            'thief': (pygame.Rect(30, 240, 130, 80), '盜賊', Coconut_Brown, WHITE, 5),
            'priest': (pygame.Rect(180, 240, 130, 80), '牧師', YELLOW, BLACK, 6),
            'return': (pygame.Rect(790, 555, 100, 40), '前往挑戰', RED, BLACK, 'return')
        }

        self.arrow_buttons = {
            'left': pygame.Rect(500, 100, 50, 50),
            'right': pygame.Rect(800, 100, 50, 50)
        }

        self.job_descriptions = params.job_descriptions

    def load_rankings(self):
        """載入排名列表"""
        try:
            with open('source/rankings.json') as f:
                rank_list = json.load(f)
            return self.calculate_job_unlocks(rank_list)
        except FileNotFoundError:
            logging.error("排名檔案未找到，將返回空解鎖資料")
            return {}
    
    def calculate_job_unlocks(self, rank_list):
        out_dict = {}
        for index, job in job_dict.items():
            max_score = max(
                (int(player['score']) for player in rank_list if player['job'] == job),
                default=0
            )
            out_dict[index] = max_score
        return out_dict

    def draw_buttons(self):
        """繪製所有按鈕"""
        for key, (rect, text, color, text_color, _) in self.buttons.items():
            pygame.draw.rect(self.window, color, rect)
            font = self.fonts['base'] if key == 'return' else self.fonts['job']
            text_surface = font.render(text, True, text_color)
            text_rect = text_surface.get_rect(center=rect.center)
            self.window.blit(text_surface, text_rect)
    
    def draw_arrow(self, surface, rect, direction):
        """簡單繪製箭頭"""
        color = Coconut_Brown
        if direction == 'left':
            pygame.draw.polygon(surface, color, [
                (rect.right, rect.top),
                (rect.left, rect.centery),
                (rect.right, rect.bottom)
            ])
        else:
            pygame.draw.polygon(surface, color, [
                (rect.left, rect.top),
                (rect.right, rect.centery),
                (rect.left, rect.bottom)
            ])

    def display_job_info(self):
        """顯示選擇職業後的資訊"""
        if not self.check_job:
            return
        
        job_id = self.person.main_job
        index = self.person.role_index

        # 顯示屬性資訊
        y = 250
        for name, value in params.player_value[job_id].items():
            display_name = self.translate_attribute(name)
            if display_name:
                text = self.fonts['base'].render(f"{display_name} : {value}", True, WHITE)
                self.window.blit(text, (500, y))
                y += 40

        # 顯示職業圖片與說明
        job_img = pygame.image.load(job_image[job_id][index]).convert_alpha()
        job_img = pygame.transform.scale(job_img, (250, 250))
        self.window.blit(job_img, (550, 0))

        description_lines = params.job_descriptions[job_id].split('\n')
        y = 250
        for line in description_lines:
            text = self.fonts['base'].render(line, True, WHITE)
            self.window.blit(text, (650, y))
            y += 40

        # 箭頭
        self.draw_arrow(self.window, self.arrow_buttons['left'], 'left')
        self.draw_arrow(self.window, self.arrow_buttons['right'], 'right')

        hint_text = self.fonts['base'].render("可使用鍵盤方向鍵察看解鎖造型", True, YELLOW)
        self.window.blit(hint_text, (100, 550))

        # 顯示鎖定圖示
        if self.is_locked(job_id, index):
            locker = pygame.image.load('source/locker.png')
            locker = pygame.transform.scale(locker, (200, 200))
            self.window.blit(locker, (550, 0))

    def translate_attribute(self, name):
        """將屬性名稱翻譯為中文"""
        mapping = {
            'name': '職業',
            'max_hp': '血量',
            'damage_b': '傷害+',
            'defense_b': '護甲+',
            'heal_b': '治癒+',
            'magic': '魔力',
            'money': '錢幣'
        }
        return mapping.get(name)
    
    def is_locked(self, job_id, index):
        """判斷該職業選擇是否鎖定"""
        if len(self.rank_list) > 0:
            return self.rank_list.get(job_id, 0) < index * 10
        else:
            return index != 0

    def handle_event(self, event):
        """處理事件"""
        if event.type == pygame.QUIT:
            self.person.main_job = 4
            logging.info(f'恭喜你獲得隱藏職業！接下來的挑戰你成為 {job_dict[self.person.main_job]} 不會獲得任何專屬卡。')
            self.job_chosing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and self.check_job and self.person.role_index < 2:
                self.person.role_index += 1
            elif event.key == pygame.K_LEFT and self.check_job and self.person.role_index >= 1:
                self.person.role_index -= 1
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_mouse(pygame.mouse.get_pos())

    def handle_mouse(self, pos):
        for key, (rect, _, _, _, job_id) in self.buttons.items():
            if rect.collidepoint(pos):
                if key == 'return':
                    if not self.is_locked(self.person.main_job, self.person.role_index):
                        self.job_chosing = False
                else:
                    self.person.main_job = job_id
                    self.person.role_index = 0
                    self.check_job = True
                    logging.info(f'你選擇成為 {job_dict[job_id]}')

    def render(self):
        """渲染職業選擇頁面"""
        self.window.blit(self.bg.bg_big, self.bg.rect)
        self.draw_buttons()
        self.display_job_info()
        pygame.display.flip()

def chose_job(win, person):
    """職業選擇函數"""
    job_page = JobPage(win, person)
    
    while job_page.job_chosing:
        for event in pygame.event.get():
            job_page.handle_event(event)
        job_page.render()