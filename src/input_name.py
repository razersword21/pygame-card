import pygame
import sys
import re
from dataclasses import dataclass
from typing import Tuple, List

from src.objects import *
from src.params import *
from src.config import *

class InputValidator:
    """輸入驗證器類"""
    @staticmethod
    def is_valid_english_name(text: str) -> Tuple[bool, str]:
        """驗證是否為有效的英文名字"""
        if not text.strip():
            return False, "名字不能為空"
        
        if len(text) < GameConfig.MIN_NAME_LENGTH:
            return False, f"名字至少需要 {GameConfig.MIN_NAME_LENGTH} 個字符"
        
        if len(text) > GameConfig.MAX_NAME_LENGTH:
            return False, f"名字不能超過 {GameConfig.MAX_NAME_LENGTH} 個字符"
        
        # 檢查是否只包含英文字母、數字和基本符號
        if not re.match(r'^[a-zA-Z0-9_-]+$', text):
            return False, "只能使用英文字母、數字、底線和連字符"
        
        return True, ""

class InputPage:
    """輸入頁面類"""
    def __init__(self, window_surface):
        self.window = window_surface
        self.config = GameConfig()
        self.colors = Colors()
        self.validator = InputValidator()
        
        # 初始化字體
        self.fonts = {
            'title': pygame.font.Font(params.Font, 80),
            'base': pygame.font.Font(params.Font, 40),
            'hint': pygame.font.Font(params.Font, 30),
            'error': pygame.font.Font(params.Font, 25)
        }
        
        # 初始化背景
        self.bg = BG(self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT)
        
        # 輸入狀態
        self.text = ""
        self.active = False
        self.error_message = ""
        
        # 說明文字
        self.instructions = [
            "遊戲說明:",
            "1. 攻擊力 = 玩家加成數值 + 卡牌傷害",
            "   (防禦和治癒相同，buff與debuff都會加成)",
            "2. 商店可購買加成屬性",
            "3. 每次打贏敵人可選擇獎勵",
            "",
            "操作提示:",
            "• 輸入完成後按 Enter 確認",
            "• 按 Backspace 刪除字符"
        ]
    
    def get_input_box(self) -> pygame.Rect:
        """獲取輸入框矩形"""
        text_surface = self.fonts['base'].render(self.text, True, self.colors.TEXT)
        box_width = max(self.config.INPUT_BOX_MIN_WIDTH, text_surface.get_width() + self.config.INPUT_PADDING * 2)
        
        input_box = pygame.Rect(0, 0, box_width, self.config.INPUT_BOX_HEIGHT)
        input_box.center = (self.config.WINDOW_WIDTH // 2, self.config.WINDOW_HEIGHT // 2)
        
        return input_box

    def handle_events(self) -> Tuple[bool, bool]:
        """處理事件，返回 (繼續輸入, 輸入完成)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                input_box = self.get_input_box()
                self.active = input_box.collidepoint(event.pos)
                self.error_message = ""  # 清除錯誤訊息
            
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    is_valid, error_msg = self.validator.is_valid_english_name(self.text)
                    if is_valid:
                        return False, True  # 停止輸入，確認完成
                    else:
                        self.error_message = error_msg
                
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.error_message = ""  # 清除錯誤訊息
                
                elif event.key == pygame.K_ESCAPE:
                    return False, False  # 取消輸入
                
                else:
                    # 限制輸入長度
                    if len(self.text) < self.config.MAX_NAME_LENGTH:
                        # 只允許英文字母、數字和基本符號
                        if event.unicode and re.match(r'[a-zA-Z0-9_-]', event.unicode):
                            self.text += event.unicode
                            self.error_message = ""
        
        return True, False

    def render_title(self):
        """渲染標題"""
        title_text = self.fonts['title'].render("輸入玩家名字", True, self.colors.TEXT)
        subtitle_text = self.fonts['title'].render("(限英文)", True, self.colors.TEXT)
        
        title_rect = title_text.get_rect(center=(self.config.WINDOW_WIDTH // 2, 100))
        subtitle_rect = subtitle_text.get_rect(center=(self.config.WINDOW_WIDTH // 2, 180))
        
        self.window.blit(title_text, title_rect)
        self.window.blit(subtitle_text, subtitle_rect)
    
    def render_input_box(self):
        """渲染輸入框"""
        input_box = self.get_input_box()
        
        # 繪製輸入框邊框
        border_color = self.colors.ACTIVE if self.active else self.colors.INACTIVE
        pygame.draw.rect(self.window, border_color, input_box, 3)
        
        # 繪製輸入文字
        if self.text:
            text_surface = self.fonts['base'].render(self.text, True, self.colors.TEXT)
            text_rect = text_surface.get_rect(centery=input_box.centery, x=input_box.x + 5)
            self.window.blit(text_surface, text_rect)
        else:
            # 顯示提示文字
            placeholder = "請輸入名字..."
            placeholder_surface = self.fonts['hint'].render(placeholder, True, (128, 128, 128))
            placeholder_rect = placeholder_surface.get_rect(centery=input_box.centery, x=input_box.x + 5)
            self.window.blit(placeholder_surface, placeholder_rect)
        
        # 繪製游標（當輸入框激活時）
        if self.active:
            cursor_x = input_box.x + 5 + self.fonts['base'].size(self.text)[0]
            cursor_y1 = input_box.y + 5
            cursor_y2 = input_box.y + input_box.height - 5
            pygame.draw.line(self.window, self.colors.ACTIVE, (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2)
    
    def render_error_message(self):
        """渲染錯誤訊息"""
        if self.error_message:
            error_surface = self.fonts['error'].render(self.error_message, True, self.colors.ERROR_TEXT)
            error_rect = error_surface.get_rect(center=(self.config.WINDOW_WIDTH // 2, 350))
            self.window.blit(error_surface, error_rect)
    
    def render_instructions(self):
        """渲染說明文字"""
        start_y = 400
        line_height = 35
        
        for instruction in self.instructions:
            if instruction.strip():  # 跳過空行
                text_surface = self.fonts['hint'].render(instruction, True, self.colors.HINT_TEXT)
                self.window.blit(text_surface, (50, start_y))
            start_y += line_height
    
    def render(self):
        """渲染整個UI"""
        # 繪製背景
        self.window.blit(self.bg.bg_big, self.bg.rect)
        
        # 繪製各個組件
        self.render_title()
        self.render_input_box()
        self.render_error_message()
        self.render_instructions()
        
        pygame.display.flip()

def input_name(win, main_role):
    input_ui = InputPage(win)

    while True:
        continue_input, input_completed = input_ui.handle_events()
        
        if not continue_input:
            if input_completed:
                main_role.name = input_ui.text.strip()
            break
        
        input_ui.render()