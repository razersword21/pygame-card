import pygame
import sys

from src.config import *
from src.objects import *
from src.card_process import *
from src.choose import *
from src.game import *
from src.params import *
from src.input_name import *
from src.rank import *
from src.job_page import *

class GameManager:
    """遊戲管理器類"""
    def __init__(self):
        self.config = GameConfig()
        self.state = GameState.state
        self.clock = pygame.time.Clock()
        self.fonts = {}
        self.game_objects = {}
        self.show_animation = True
        
        self._init_pygame()
        self._init_fonts()
        self._init_game_objects()
        self._init_buttons()

    def _init_pygame(self):
        pygame.init()
        pygame.mixer.init()

        try:
            pygame.mixer.music.load("source/bg_music.mp3")
            pygame.mixer.music.set_volume(self.config.MUSIC_VOLUME)
            pygame.mixer.music.play(loops=-1)
        except pygame.error as e:
            print(f"Error loading music: {e}")
        
        self.screen = pygame.display.set_mode((self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT))
        pygame.display.set_caption(self.config.TITLE)

    def _init_fonts(self):
        """初始化字體"""
        self.fonts = {
            'base': pygame.font.Font(params.Font, 32),
            'title': pygame.font.Font(params.Font, 80),
            'button': pygame.font.Font(params.Font, 50)
        }

    def _init_game_objects(self):
        """初始化遊戲物件"""
        self.game_objects = {
            'intro': Intro(self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT),
            'intro_animation': Intro_animation(300, 300),
            'enemy': Enemy(params.enemy_max_hp, params.enemy_max_de, params.enemy_max_magic),
            'main_role': Main_role(params.init_max_hp, params.init_max_de, params.init_max_magic, params.money)
        }

    def _init_buttons(self):
        """初始化按鈕"""
        self.buttons = {
            'start': ButtonConfig(
                rect=pygame.Rect(250, 530, 130, 50),
                color=RED,
                text="Start",
                text_color=BLACK,
                action="start_game"
            ),
            'rank': ButtonConfig(
                rect=pygame.Rect(400, 530, 130, 50),
                color=YELLOW,
                text="排名榜",
                text_color=BLACK,
                action="show_rank"
            ),
            'quit': ButtonConfig(
                rect=pygame.Rect(550, 530, 130, 50),
                color=BLACK,
                text="Quit",
                text_color=WHITE,
                action="quit_game"
            )
        }

    def draw_button(self, button_config: ButtonConfig):
        """繪製按鈕"""
        pygame.draw.rect(self.screen, button_config.color, button_config.rect)
        text_surface = self.fonts['button'].render(button_config.text, True, button_config.text_color)
        
        # 計算文字置中位置
        text_rect = text_surface.get_rect(center=button_config.rect.center)
        self.screen.blit(text_surface, text_rect)

    def handle_button_click(self, pos: Tuple[int, int]) -> str:
        """處理按鈕點擊事件"""
        for button_name, button_config in self.buttons.items():
            if button_config.rect.collidepoint(pos):
                return button_config.action
        return ""

    def handle_intro_events(self):
        """處理介面事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameState.set_state(GameStateEnum.QUIT)
                self.state = GameState.state
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = self.handle_button_click(pygame.mouse.get_pos())
                
                if action == "start_game":
                    self._start_new_game()
                elif action == "show_rank":
                    self._show_rank_page()
                elif action == "quit_game":
                    GameState.set_state(GameStateEnum.QUIT)
                    self.state = GameState.state

    def _start_new_game(self):
        """開始新遊戲"""
        main_role = self.game_objects['main_role']
        
        # 輸入名字
        input_name(self.screen, main_role)

        if not main_role.name:
            GameState.set_state(GameStateEnum.INTRO)
            self.state = GameState.state
            return
        logging.debug(f"玩家名字: {main_role.name}")

        # 選擇職業
        chose_job(self.screen, main_role)
        logging.debug(f"玩家選擇的職業: {job_dict[main_role.main_job]}")

        GameState.set_state(GameStateEnum.PLAYING)
        self.state = GameState.state
        all_fonts = [self.fonts['base'], self.fonts['title']]

        try:
            game_(self.screen, all_fonts, True, main_role, self.game_objects['enemy'])
        except Exception as e:
            print(f"Error game: {e}")
            GameState.set_state(GameStateEnum.INTRO)
            self.state = GameState.state
            return

        # 遊戲結束後返回主選單
        GameState.set_state(GameStateEnum.INTRO)
        self.state = GameState.state
        self._reset_game_objects()

    def _show_rank_page(self):
        """顯示排名榜"""
        rank_page(self.screen)

    def _reset_game_objects(self):
        """重置遊戲物件"""
        self.game_objects['enemy'] = Enemy(params.enemy_max_hp, params.enemy_max_de, params.enemy_max_magic)
        self.game_objects['main_role'] = Main_role(params.init_max_hp, params.init_max_de, params.init_max_magic, params.money)
        self.show_animation = True

    def render_intro(self):
        """渲染介面畫面"""
        # 播放動畫
        if self.show_animation:
            self.game_objects['intro_animation'].fadeout_animation(self.screen, self.clock, a=255)
            self.show_animation = False
        
        # 繪製背景
        intro = self.game_objects['intro']
        self.screen.blit(intro.bg_big, intro.rect)
        
        # 繪製按鈕
        for button_config in self.buttons.values():
            self.draw_button(button_config)

    def run(self):
        """主遊戲循環"""
        running = True
        
        while running:
            if self.state == GameStateEnum.INTRO:
                self.handle_intro_events()
                self.render_intro()
                
            elif self.state == GameStateEnum.QUIT:
                running = False
            
            pygame.display.flip()
            self.clock.tick(self.config.FPS)
        
        self._cleanup()
    
    def _cleanup(self):
        """清理資源"""
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()

# main
def main():
    try:
        game_manager = GameManager()
        game_manager.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == '__main__':
    main()