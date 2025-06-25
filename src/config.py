from dataclasses import dataclass
from typing import Tuple, Dict, Callable
from enum import Enum
import pygame

from src.params import *

class GameStateEnum(Enum):
    """遊戲狀態枚舉"""
    INTRO = "intro"
    INPUT_NAME = "input_name"
    CHOOSE_JOB = "choose_job"
    PLAYING = "playing"
    RANK = "rank"
    QUIT = "quit"

class GameState:
    """遊戲狀態類"""
    state: GameStateEnum = GameStateEnum.INTRO

    @classmethod
    def set_state(cls, new_state: GameStateEnum):
        """設置遊戲狀態"""
        cls.state = new_state

@dataclass
class GameConfig:
    """遊戲配置類"""
    WINDOW_WIDTH: int = 900
    WINDOW_HEIGHT: int = 600
    MUSIC_VOLUME: float = 0.1
    FPS: int = 60
    TITLE: str = '數值-無限輪迴 ( Numerical value-infinite reincarnation )'

    """輸入框配置"""
    INPUT_BOX_MIN_WIDTH: int = 200
    INPUT_BOX_HEIGHT: int = 50
    INPUT_PADDING: int = 10
    MAX_NAME_LENGTH: int = 20
    MIN_NAME_LENGTH: int = 1

@dataclass
class ButtonConfig:
    """按鈕配置類"""
    rect: pygame.Rect
    color: Tuple[int, int, int]
    text: str
    text_color: Tuple[int, int, int]
    action: str

@dataclass
class Colors:
    """顏色配置"""
    INACTIVE: Tuple[int, int, int] = BLACK
    ACTIVE: Tuple[int, int, int] = RED
    TEXT: Tuple[int, int, int] = BLACK
    HINT_TEXT: Tuple[int, int, int] = WHITE
    ERROR_TEXT: Tuple[int, int, int] = RED