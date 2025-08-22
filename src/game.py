import pygame,sys
import random
import time
import json
import math
import logging
logging.basicConfig(level=logging.INFO)

from src.objects import *
from src.card_process import *
from src.choose import *
from src.params import *
from src.win_page import *
from src.config import *

def set_enemy(enemy, log_text_list):
    # 設定敵人名稱
    e_index = random.randint(0, 10)
    enemy.enemy_index = e_index
    enemy.name = enemy_name[enemy.enemy_index]

    # 設定敵人屬性對應表
    effects = [
        (1, 35, "max_hp", params.add_hp, "hp"),
        (36, 40, "max_magic", params.add_value, "magic"),
        (41, 50, "damage_buff", params.add_value, "damage"),
        (51, 75, "defense_buff", params.add_value, "defense"),
        (76, 100, "heal_buff", params.add_value, "heal"),
    ]

    # 設定敵人屬性
    x = random.randint(1, 100)
    log_text = None

    for low, high, attr, value, text in effects:
        if low <= x <= high:
            log_text = apply_buff(enemy, attr, value, text)
            break

    # 重設 hp / magic
    enemy.hp = enemy.max_hp
    enemy.magic = enemy.max_magic

    # 重置 buff
    if len(enemy.buff) > 0:
        enemy.reset_buff()
       
    # 戰鬥log
    log_text_list.append(log_text)
    log_text_list = log_text_list[-params.log_text_len:]

    return enemy,log_text_list

def apply_buff(main_role, attr, value, text):
    """套用屬性增強，並回傳 log 文字"""
    setattr(main_role, attr, getattr(main_role, attr) + value)
    log_text = f"{main_role.name} 對於 {text} 增強了!"
    logging.info(log_text)
    return log_text

def set_player(main_role, choose, add_value, log_text_list, new_card=None):
    add_value = params.add_value
    log_text = None

    # 各屬性對應表
    attr_map = {
        "hp": ("max_hp", add_value, "Hp"),
        "damage": ("damage_buff", add_value, "damage"),
        "defense": ("defense_buff", add_value, "defense"),
        "heal": ("heal_buff", add_value, "heal"),
        "magic": ("magic", add_value, "magic"),
    }

    if choose == "hp":
        # 直接增強 HP
        log_text = apply_buff(main_role, *attr_map["hp"])

    elif choose == "all":
        # 隨機增強一種屬性
        sub_choose = random.choice(["damage", "defense", "heal", "magic"])
        log_text = apply_buff(main_role, *attr_map[sub_choose])

    elif choose == "":
        # 放棄選擇，拿錢
        main_role.money += params.add_pass_money
        log_text = f"{main_role.name} 放棄選擇 ， 獲得錢幣 {params.add_pass_money} !"
        logging.info(log_text)

    else:
        # 特殊卡
        log_text = f"{main_role.name} 選擇特殊卡 ! -> {new_card.name}"
        logging.info(log_text)

    # 重設狀態
    main_role.hp = main_role.max_hp
    main_role.magic = main_role.max_magic
    main_role.de = 0

    if len(main_role.buff) > 0:
        main_role.reset_buff()

    # 戰鬥 log
    log_text_list.append(log_text)
    log_text_list = log_text_list[-params.log_text_len:]

    return main_role,log_text_list

class Gaming:
    def __init__(self, window, font_list, GAME_CONTROL, main_role, enemy):
        self.win = window
        self.font_list = font_list
        self.GAME_CONTROL = GAME_CONTROL
        self.main_role = main_role
        self.enemy = enemy

        self.config = GameConfig()
        self.colors = Colors()
        self.bg = BG(self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT)

        with open('source/rankings.json') as f:
            rank_list = json.load(f)
        self.rank_list = rank_list

        self.rounds = 0
        self.clock = pygame.time.Clock()
        self.running = True

        self.init_enemy_card_deck = enemy_init_card_deck()
        self.enemy_remain_deck = self.init_enemy_card_deck.copy()
        self.enemy_normal_deck = Special_card.normal_deck.copy()
        self.enemy_current_cards = random.sample(self.enemy_remain_deck, 5)
        self.enemy_used_cards = []
        self.new_add_enemy_card = []

        self.init_main_card_deck = init_card_deck(main_role)
        self.main_remain_deck = self.init_main_card_deck.copy()
        self.main_used_cards = []

        self.log_text_list = []

        self.next_turn_btn = pygame.Rect(800, 400, 70, 70)
        self.remain_btn = pygame.Rect(700, 400, 70, 70)
        self.history_btn = pygame.Rect(800, 500, 70, 70)
        self.used_btn = pygame.Rect(700, 500, 70, 70)
        self.quit_btn = pygame.Rect(820, 20, 65, 30)

    def run(self):
        """遊戲主循環"""

        # 初始化遊戲狀態
        player_turn, show_history, show_remain, show_used, takedown, show_next = True, False, False, False, False, True
        chose_buff = ''
        turnFlag, current_card_index, new_card = 0, 0, None
        remain_start_y, used_start_y = 5, 5

        self.main_role.reset(params.player_value)
        self.enemy.reset(params.enemy_max_hp, params.enemy_max_de, params.enemy_max_magic)

        current_cards = random.sample(self.main_remain_deck, self.main_role.every_drop)

        card_font = pygame.font.Font(params.Font, 25)

        # 遊戲主循環
        while self.running:
            show_next_stage = True
            self.win.blit(self.bg.bg_big, self.bg.rect)
            Rounds_text = self.font_list[0].render("關卡: "+ str(self.rounds), True, BLACK)
            self.win.blit(Rounds_text, (10, 10))

            self.main_role.draw(self.win, 230, 300)
            self.enemy.draw(self.win, 700, 300)

            # 繪製玩家屬性
            self.draw_player_value()

            # 繪製敵人屬性
            self.draw_enemy_value()

            # 繪製UI
            self.draw_ui(show_history, show_remain, show_used, card_font, remain_start_y, used_start_y)

            # 處理事件
            response = self.handel_event(
                remain_start_y, used_start_y, show_remain, show_history, show_used, player_turn, current_cards
            )
        
            remain_start_y = response['remain_start_y']
            used_start_y = response['used_start_y']
            show_history = response['show_history']
            show_remain = response['show_remain']
            show_used = response['show_used']
            current_cards = response['current_cards']
            player_turn = response['player_turn']

            if self.GAME_CONTROL:
                if player_turn:
                    self.log_text_list, turnFlag, self.enemy_current_cards, player_turn = self.handle_player_turn(
                        current_cards, turnFlag, show_history, show_used, show_remain, player_turn
                    )
                else:
                    self.log_text_list, turnFlag, self.GAME_CONTROL, player_turn, current_cards = self.handle_enemy_turn(
                        player_turn, takedown, turnFlag, show_history, show_used, show_remain
                    )
            elif not self.GAME_CONTROL and self.enemy.hp == 0:
                current_cards = self.handel_round(show_next)
            else:
                over_bg = pygame.Rect(200, 225, 500, 150) 
                pygame.draw.rect(self.win, BLACK , over_bg)
                over_font = pygame.font.Font(params.Font, 150)
                over_text = over_font.render("Game Over", True, RED)
                self.win.blit(over_text, (225, 230))
                pygame.display.update()
                time.sleep(3)
                self.running = False
                write_game_records(self.rank_list, self.main_role, self.rounds)
                logging.warning(self.main_role.name+' 用 '+ job_dict[self.main_role.main_job] + ' 打到 關卡: '+str(self.rounds))

            pygame.display.flip()
            self.clock.tick(40) 

    def draw_player_value(self):
        """繪製玩家屬性"""
        # 要繪製的屬性 (文字, 顏色, 座標)
        attributes = [
            (f"HP: {self.main_role.hp}", RED, (200, 10)),
            (f"Def: {self.main_role.de}", BLUE, (200, 40)),
            (f"MP: {self.main_role.magic}", BLACK, (200, 70)),
            (f"Money: {self.main_role.money}", YELLOW, (15, 375)),
            (f"Damage: {self.main_role.damage_buff}", PURPLE, (10, 200)),
            (f"Def: {self.main_role.defense_buff}", PURPLE, (10, 240)),
            (f"Heal: {self.main_role.heal_buff}", PURPLE, (10, 280)),
        ]

        # 批量繪製屬性
        for text, color, pos in attributes:
            self.win.blit(self.font_list[0].render(text, True, color), pos)

        # 繪製玩家名稱和職業
        name_x = 170 if len(self.main_role.name) > 10 else 200
        player_name_text = self.font_list[0].render(self.main_role.name, True, Coconut_Brown)
        self.win.blit(player_name_text, (name_x, 100))
        # 玩家職業
        player_job_text = self.font_list[0].render(job_dict[self.main_role.main_job], True, Coconut_Brown)
        self.win.blit(player_job_text, (125, 100))

        # 繪製玩家增益效果
        if self.main_role.buff:
            start_y = 200
            for i, buff in enumerate(self.main_role.buff):
                buff_name = list(buff.keys())[0]  # 取 buff 名稱
                main_buff_text = self.font_list[0].render(buff_name, True, Coconut_Brown)
                self.win.blit(main_buff_text, (300, start_y + 50 * i))

    def draw_enemy_value(self):
        """繪製敵人屬性"""
        # 要繪製的屬性 (文字, 顏色, 座標)
        attributes = [
            (f"HP: {self.enemy.hp}", RED, (685, 10)),
            (f"Def: {self.enemy.de}", BLUE, (685, 40)),
            (f"MP: {self.enemy.magic}", BLACK, (685, 70)),
            (f"Damage: {self.enemy.damage_buff}", PURPLE, (780, 200)),
            (f"Def: {self.enemy.defense_buff}", PURPLE, (780, 240)),
            (f"Heal: {self.enemy.heal_buff}", PURPLE, (780, 280)),
        ]

        # 批量繪製屬性
        for text, color, pos in attributes:
            self.win.blit(self.font_list[0].render(text, True, color), pos)

        # 繪製敵人名稱
        name_x = 685 if len(self.enemy.name) > 3 else 655
        enemy_name_text = self.font_list[0].render(self.enemy.name, True, Coconut_Brown)
        self.win.blit(enemy_name_text, (name_x, 100))

        # 繪製敵人增益效果
        if self.enemy.buff:
            start_y_e = 200
            for i, ebuff in enumerate(self.enemy.buff):
                ebuff_name = list(ebuff.keys())[0]  # 取 buff 名稱
                enemy_buff_text = self.font_list[0].render(ebuff_name, True, Coconut_Brown)
                self.win.blit(enemy_buff_text, (550, start_y_e + 50 * i))

    def draw_button(self, rect, color, texts, text_color=BLACK):
        """繪製按鈕"""
        pygame.draw.rect(self.win, color, rect)
        for i, text in enumerate(texts):
            text_surface = self.font_list[0].render(text, True, text_color)
            self.win.blit(text_surface, (rect.x , rect.y + i*40))

    def draw_panel(self, rect, color, texts, text_color=BLACK, line_height=30, offset=(30, 10)):
        """繪製面板"""
        panel = pygame.Surface((rect.width, rect.height))
        panel.fill(color)
        for i, text in enumerate(texts):
            text_surface = self.font_list[0].render(text, True, text_color)
            panel.blit(text_surface, (offset[0], offset[1] + i * line_height))
        self.win.blit(panel, (rect.x, rect.y))

    def draw_deck_panel(self, rect, color, cards, start_y=0, text_color=BLACK):
        """繪製卡片面板"""
        panel = pygame.Surface((rect.width, rect.height))
        panel.fill(color)
        for i, card in enumerate(cards):
            card_text = self.font_list[0].render(card.name, True, text_color)
            panel.blit(card_text, (5 + (i % 9) * 50, start_y + (i // 9) * 50))
        self.win.blit(panel, (rect.x, rect.y))

    def draw_ui(self, show_history, show_remain, show_used, card_font, remain_start_y, used_start_y):
        # 按鈕們
        buttons = [
            (self.quit_btn, BLACK, ["Quit"], WHITE),
            (self.history_btn, Wisteria, ["戰鬥", "歷程"]),
            (self.remain_btn, Bisque, ["剩餘", str(len(self.main_remain_deck))]),
            (self.used_btn, Silver, ["用過", str(len(self.main_used_cards))]),
            (self.next_turn_btn, RED, ["回合", "結束"])
        ]
        for rect, color, texts, *text_color in buttons:
            if text_color:
                self.draw_button(rect, color, texts, text_color[0])
            else:
                self.draw_button(rect, color, texts)

        # 面板們
        if show_history:
            self.draw_panel(pygame.Rect(200, 30, 500, 350), Wisteria, self.log_text_list)

        if show_remain:
            self.draw_deck_panel(pygame.Rect(200, 30, 500, 350), Bisque, self.main_remain_deck, start_y=remain_start_y)

        if show_used:
            self.draw_deck_panel(pygame.Rect(200, 30, 500, 350), Silver, self.main_used_cards, start_y=used_start_y)

    def handle_quit(self):
        """處理退出"""
        write_game_records(self.rank_list, self.main_role, self.rounds)
        logging.warning(f"{self.main_role.name} 用 {job_dict[self.main_role.main_job]} 打到 關卡: {self.rounds}")
        pygame.quit()
        sys.exit()

    def toggle_panel(self, show_flag, reset_y=None):
        """切換面板顯示"""
        return not show_flag, (5 if reset_y is not None else reset_y)

    def handle_card_click(self, pos, current_cards, player_turn):
        """處理卡片點擊"""
        end_x = (len(current_cards) + 1) * 100
        if not (20 <= pos[0] <= end_x and 430 <= pos[1] <= 570 and self.GAME_CONTROL and player_turn):
            return self.GAME_CONTROL, current_cards, self.log_text_list, None

        card_index = pos[0] // 100
        card_index = min(card_index, len(current_cards) - 1)

        # 使用卡牌
        main_card = current_cards[card_index]
        if (self.main_role.magic - main_card.cost) >= 0:
            current_cards.pop(card_index)
            self.main_role.magic -= main_card.cost
            if main_card.index != -1:
                self.main_used_cards.append(main_card)
                usedcardindex = [x.index for x in self.main_remain_deck].index(main_card.index)
                self.main_remain_deck.pop(usedcardindex)
            return use_card_effect(main_card, self.enemy, self.main_role, self.GAME_CONTROL, self.main_remain_deck, self.main_used_cards, 
                current_cards, self.log_text_list, 'player')
        
        return self.GAME_CONTROL, current_cards, self.log_text_list, None

    def handel_event(self, remain_start_y, used_start_y, show_remain, show_history, show_used, player_turn, current_cards):
        """處理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.handle_quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    if remain_start_y < -5 and show_remain:
                        remain_start_y += 20
                    if used_start_y < -5 and show_used:
                        used_start_y += 20
                elif event.button == 5:
                    if math.floor(len(main_remain_deck) / 9) * 50 + remain_start_y > 370 and show_remain:
                        remain_start_y -= 20
                    if math.floor(len(main_used_cards) / 9) * 50 + used_start_y > 370 and show_used:
                        used_start_y -= 20

                # 點擊處理
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    if self.next_turn_btn.collidepoint(pos):
                        player_turn = False
                    elif self.history_btn.collidepoint(pos):
                        show_history, _ = self.toggle_panel(show_history)
                        if show_history:
                            show_used, show_remain = False, False
                    elif self.remain_btn.collidepoint(pos):
                        show_remain, remain_start_y = self.toggle_panel(show_remain, reset_y=5)
                        if show_remain:
                            show_history, show_used = False, False
                    elif self.used_btn.collidepoint(pos):
                        show_used, used_start_y = self.toggle_panel(show_used, reset_y=5)
                        if show_used:
                            show_remain, show_history = False, False
                    elif self.quit_btn.collidepoint(pos):
                        self.handle_quit()

                    # 卡牌區點擊
                    self.GAME_CONTROL, current_cards, self.log_text_list, takedown = self.handle_card_click(
                        pos, current_cards, player_turn
                    )

        response = {
            'remain_start_y': remain_start_y,
            'used_start_y': used_start_y,
            'show_history': show_history,
            'show_remain': show_remain,
            'show_used': show_used,
            'current_cards': current_cards,
            'main_remain_deck': self.main_remain_deck,
            'main_used_cards': self.main_used_cards,
            'GAME_CONTROL': self.GAME_CONTROL,
            'log_text_list': self.log_text_list,
            'player_turn': player_turn
        }
        return response

    def handle_player_turn(self, current_cards, turnFlag, show_history, show_used, show_remain, player_turn):
        """處理關卡"""
        if not show_history and not show_used and not show_remain:
            turn_index = pygame.image.load('source/mainrole_turn.png')
            self.win.blit(turn_index, (280, 150))

        # 繪製玩家手牌
        for i, card in enumerate(current_cards):
            card.draw(self.win, i)

        pygame.display.update()

        # 回合開始記錄
        if turnFlag == 0:
            turnFlag = 1
            log_text = '---------------Player Turn---------------'
            self.log_text_list.append(log_text)
            self.log_text_list = self.log_text_list[-params.log_text_len:]
            logging.info(log_text)

        # 敵人抽牌
        if len(self.enemy_remain_deck) < 5:
            enemy_return_cards = random.sample(self.enemy_used_cards, 5 - len(self.enemy_remain_deck))
            self.enemy_remain_deck.extend(enemy_return_cards)
            self.enemy_current_cards = random.sample(self.enemy_remain_deck, 5)
            self.enemy_remain_deck.extend(self.enemy_used_cards)
            self.enemy_used_cards.clear()
        else:
            self.enemy_current_cards = random.sample(self.enemy_remain_deck, 5)

        return self.log_text_list, turnFlag, self.enemy_current_cards, player_turn

    def handle_enemy_turn(self, player_turn, takedown, turnFlag, show_history, show_used, show_remain):
        """處理敵人回合"""
        if takedown:
            player_turn = True

        # 玩家補牌
        if len(self.main_remain_deck) < self.main_role.every_drop:
            return_cards = random.sample(self.main_used_cards, self.main_role.every_drop - len(self.main_remain_deck))
            self.main_remain_deck.extend(return_cards)
            current_cards = random.sample(self.main_remain_deck, self.main_role.every_drop)
            self.main_remain_deck.extend(self.main_used_cards)
            self.main_used_cards.clear()
        else:
            current_cards = random.sample(self.main_remain_deck, self.main_role.every_drop)

        # 回合開始記錄
        if turnFlag == 1:
            check_person_buff(self.enemy, self.main_role)
            log_text = '---------------Enemy Turn---------------'
            self.log_text_list.append(log_text)
            self.log_text_list = self.log_text_list[-params.log_text_len:]
            logging.info(log_text)
            turnFlag = 0
        
        # 顯示敵人回合
        if not show_history and not show_used and not show_remain:
            enemy_turn_index = pygame.image.load('source/enemy_turn.png')
            self.win.blit(enemy_turn_index, (550, 150))
            pygame.display.update()

        # 敵人使用卡牌
        if self.enemy.magic > 0:
            card = self.enemy.use_cardAI(self.enemy_current_cards)
            if (self.enemy.magic - card.cost) >= 0:
                time.sleep(0.5)
                self.enemy.magic -= card.cost
                if card.index != -1:
                    enemy_cardindex = [x.index for x in self.enemy_remain_deck].index(card.index)
                    self.enemy_remain_deck.pop(enemy_cardindex)
                    enemy_current_cardindex = [x.index for x in self.enemy_current_cards].index(card.index)
                    self.enemy_current_cards.pop(enemy_current_cardindex)
                    self.enemy_used_cards.append(card)

                self.GAME_CONTROL, self.enemy_current_cards, self.log_text_list, _ = use_card_effect(
                    card, self.main_role, self.enemy, self.GAME_CONTROL,
                    self.enemy_remain_deck, self.enemy_used_cards, self.enemy_current_cards,
                    self.log_text_list, 'enemy'
                )

                # 敵人出牌繪製
                card.draw(self.win, 0, 450, 200)
                enemy_use_card_text = self.font_list[0].render("敵人使用了 " + card.name, True, BLACK)
                self.win.blit(enemy_use_card_text, (370, 50))
                pygame.display.update()
                time.sleep(0.5)
            else:
                logging.info('敵人抽牌中 ! ...')
        else:
            time.sleep(1)
            player_turn = True
            self.enemy.magic = self.enemy.max_magic
            self.main_role.magic = self.main_role.max_magic
            check_person_buff(self.main_role, self.enemy)
        
        return self.log_text_list, turnFlag, self.GAME_CONTROL, player_turn, current_cards

    def handel_round(self, show_next):
        """處理勝利結算與新回合初始化"""
        mm = random.randint(50, 100)
        self.main_role.money += mm
        self.rounds += 1
        logging.info('勝利！獲得 ' + str(mm) + ' 金錢')

        # 給新卡
        if self.rounds % 5 == 0:
            new_card_deck = random.sample(
            Special_card.normal_deck + Special_card.high_level_deck +
            Special_card.pro_job_deck[self.main_role.main_job], k=3)

            self.new_add_enemy_card.append(random.choice(self.enemy_normal_deck))

        else:
            new_card_deck = random.sample(
            Special_card.normal_deck + Special_card.pro_job_deck[self.main_role.main_job], k=3)

        chose_buff, add_value, new_card, self.main_role = win_surface(
            self.win, self.font_list, self.rounds, self.main_role, new_card_deck)
            
        log_text = '********* Next Round *********'
        self.log_text_list.append(log_text)
        self.log_text_list = self.log_text_list[-params.log_text_len:]
        logging.warning(log_text)

        if new_card:
            new_card.index = len(self.init_main_card_deck)
            self.init_main_card_deck.append(new_card)

        # 更新敵人與玩家
        self.main_remain_deck = self.init_main_card_deck.copy()
        self.main_used_cards.clear()
        current_cards = random.sample(self.main_remain_deck, self.main_role.every_drop)

        self.init_enemy_card_deck = enemy_init_card_deck() 
        self.enemy_remain_deck = self.init_enemy_card_deck.copy()

        for new_e_card in self.new_add_enemy_card:
            new_e_card.index = len(init_enemy_card_deck)
            self.enemy_remain_deck.append(new_e_card)
        self.new_add_enemy_card.clear()
        self.enemy_used_cards.clear()
        self.enemy_current_cards = random.sample(self.enemy_remain_deck, 5)

        if self.rounds % 5 != 0 or self.rounds == 0:
            self.enemy, self.log_text_list = set_enemy(self.enemy, self.log_text_list)
        self.main_role, self.log_text_list = set_player(self.main_role, chose_buff, add_value, self.log_text_list, new_card)

        if show_next:
            background = pygame.Surface((self.win.get_rect().width, self.win.get_rect().height))
            background.fill(BLACK)
            self.win.blit(background, background.get_rect())
            rounds_text1 = self.font_list[1].render("關卡", True, WHITE)
            rounds_text2 = self.font_list[1].render(str(self.rounds-1)+' -> '+str(self.rounds), True, WHITE)
            self.win.blit(rounds_text1, (350, 250))
            self.win.blit(rounds_text2, (350, 350))
            pygame.display.update()
            time.sleep(2)
            show_next = False
        self.GAME_CONTROL = True

        return current_cards

def temp_game_(win, font_list, GAME_CONTROL, main_role, enemy):
    gaming = Gaming(win, font_list, GAME_CONTROL, main_role, enemy)
    gaming.run()

"""def game_(win, font_list, GAME_CONTROL, main_role, enemy):
    bg = BG(900, 600)
    rounds = 0
    clock = pygame.time.Clock()
    main_role.reset(params.player_value)
    enemy.reset(params.enemy_max_hp,params.enemy_max_de,params.enemy_max_magic)
    card_font = pygame.font.Font(params.Font, 25)
    chose_buff = ''
    with open('source/rankings.json') as f:
        rank_list = json.load(f)
    running = True 
    player_turn,show_history,show_remain,show_used,takedown = True,False,False,False,False

    init_enemy_card_deck = enemy_init_card_deck()
    init_main_card_deck = init_card_deck(main_role)

    main_remain_deck = init_main_card_deck.copy()
    main_used_cards = []
    current_cards = random.sample(main_remain_deck,main_role.every_drop)
    
    enemy_remain_deck = init_enemy_card_deck.copy()
    enemy_normal_deck = Special_card.normal_deck.copy()
    enemy_current_cards = random.sample(enemy_remain_deck,5)
    enemy_used_cards = []
    new_add_enemy_card = []
    
    test,current_card_index,log_text_list,new_card = 0,0,[],None
    remain_start_y,used_start_y = 5,5
    while running:
        show_next = True
        win.blit(bg.bg_big, bg.rect)
        Rounds_text = font_list[0].render("關卡: "+str(rounds), True, BLACK)
        win.blit(Rounds_text, (10, 10))

        main_role.draw(win,230,300)
        enemy.draw(win,700,300)

        player_hp_text = font_list[0].render("HP: "+str(main_role.hp), True, RED)
        player_de_text = font_list[0].render("Def: "+str(main_role.de), True, BLUE)
        player_mp_text = font_list[0].render("MP: "+str(main_role.magic), True, BLACK)
        player_money_text = font_list[0].render("Money: "+str(main_role.money), True, YELLOW)
        player_value_text1 = font_list[0].render("Damage: "+str(main_role.damage_buff), True, PURPLE)
        player_value_text2 = font_list[0].render('Def: '+str(main_role.defense_buff), True, PURPLE)
        player_value_text3 = font_list[0].render('Heal: '+str(main_role.heal_buff), True, PURPLE)
        player_name_text = font_list[0].render(main_role.name, True, Coconut_Brown)
        player_job_text = font_list[0].render(job_dict[main_role.main_job], True, Coconut_Brown)
        win.blit(player_hp_text, (200, 10))
        win.blit(player_de_text, (200, 40))
        win.blit(player_mp_text, (200, 70))
        win.blit(player_money_text, (15, 375))
        win.blit(player_value_text1, (10, 200))
        win.blit(player_value_text2, (10, 240))
        win.blit(player_value_text3, (10, 280))
        if len(enemy.name) > 10:
            win.blit(player_name_text, (170, 100))
        else:
            win.blit(player_name_text, (200, 100))
        win.blit(player_job_text, (125, 100))
        start_y = 200
        if len(list(main_role.buff)) > 0:
            for i,buff in enumerate(main_role.buff):
                start_y += 50*i
                main_buff_text = font_list[0].render(list(buff.keys())[0], True, Coconut_Brown)
                win.blit(main_buff_text, (300, start_y))

        enemy_hp_text = font_list[0].render("HP: "+str(enemy.hp), True, RED)
        enemy_de_text = font_list[0].render("Def: "+str(enemy.de), True, BLUE)
        enemy_mp_text = font_list[0].render("MP: "+str(enemy.magic), True, BLACK)
        enemy_value_text1 = font_list[0].render("Damage: "+str(enemy.damage_buff), True, PURPLE)
        enemy_value_text2 = font_list[0].render('Def: '+str(enemy.defense_buff), True, PURPLE)
        enemy_value_text3 = font_list[0].render('Heal: '+str(enemy.heal_buff), True, PURPLE)
        enemy_name_text = font_list[0].render(enemy.name, True, Coconut_Brown)
        win.blit(enemy_hp_text, (685, 10))
        win.blit(enemy_de_text, (685, 40))
        win.blit(enemy_mp_text, (685, 70))
        win.blit(enemy_value_text1, (780, 200))
        win.blit(enemy_value_text2, (780, 240))
        win.blit(enemy_value_text3, (780, 280))
        if len(enemy.name) > 3:
            win.blit(enemy_name_text, (655, 100))
        else:
            win.blit(enemy_name_text, (685, 100))
        start_y_e = 200
        if len(list(enemy.buff)) > 0:
            for i,ebuff in enumerate(enemy.buff):
                start_y_e += 50*i
                enemy_buff_text = font_list[0].render(list(ebuff.keys())[0], True, Coconut_Brown)
                win.blit(enemy_buff_text, (550, start_y_e))

        next_turn_btn = pygame.Rect(800, 400, 70, 70) 
        pygame.draw.rect(win, RED , next_turn_btn)
        btn_text = font_list[0].render("回合", True, BLACK)
        win.blit(btn_text, (800, 400))
        btn_text = font_list[0].render("結束", True, BLACK)
        win.blit(btn_text, (800, 440))
        quit_btn = pygame.Rect(820, 20, 65, 30) 
        pygame.draw.rect(win, BLACK , quit_btn)
        quit_text = font_list[0].render("Quit", True, WHITE)
        win.blit(quit_text, (825, 20))
        history_btn = pygame.Rect(800, 500, 70, 70) 
        pygame.draw.rect(win, Wisteria , history_btn)
        history_text1 = font_list[0].render("戰鬥", True, BLACK)
        history_text2 = font_list[0].render("歷程", True, BLACK)
        win.blit(history_text1, (810, 500))
        win.blit(history_text2, (810, 540))
        remain_btn = pygame.Rect(700, 400, 70, 70) 
        pygame.draw.rect(win, Bisque , remain_btn)
        remain_text1 = font_list[0].render("剩餘", True, BLACK)
        remain_text2 = font_list[0].render(str(len(main_remain_deck)), True, BLACK)
        win.blit(remain_text1, (710, 400))
        win.blit(remain_text2, (710, 440))
        used_btn = pygame.Rect(700, 500, 70, 70) 
        pygame.draw.rect(win, Silver , used_btn)
        used_text1 = font_list[0].render("用過", True, BLACK)
        used_text2 = font_list[0].render(str(len(main_used_cards)), True, BLACK)
        win.blit(used_text1, (710, 500))
        win.blit(used_text2, (710, 540))
        
        if show_history:
            history_surface = pygame.Surface((500,350))
            history_surface.fill(Wisteria)
            for i, text in enumerate(log_text_list):
                log_text = font_list[0].render(text, True, BLACK)
                history_surface.blit(log_text, (30, 10+i*30))
            win.blit(history_surface, (200, 30))
            # pygame.display.update()
        if show_remain:
            remain_surface = pygame.Surface((500,350))
            remain_surface.fill(Bisque)
            for i,card in enumerate(main_remain_deck):
                card_text = card_font.render(card.name,True,BLACK)
                remain_surface.blit(card_text, (5+(i % 9)*50, remain_start_y+math.floor(i/9)*50))
            win.blit(remain_surface, (200, 30))
            # pygame.display.update()

        if show_used:
            used_surface = pygame.Surface((500,350))
            used_surface.fill(Silver)
            for i,card in enumerate(main_used_cards):
                card_text = card_font.render(card.name,True,BLACK)
                used_surface.blit(card_text, (5+(i % 9)*50, used_start_y+math.floor(i/9)*50))
            win.blit(used_surface, (200, 30))
            # pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                write_game_records(rank_list,main_role,rounds)
                logging.warning(main_role.name+' 用 '+ job_dict[main_role.main_job] + ' 打到 關卡: '+str(rounds))
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                if remain_start_y<-5 and show_remain:
                    remain_start_y+=20
                if used_start_y<-5 and show_used:
                    used_start_y+=20
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                if math.floor(len(main_remain_deck)/9)*50+remain_start_y > 370 and show_remain:
                    remain_start_y-=20
                if math.floor(len(main_used_cards)/9)*50+used_start_y > 370 and show_used:
                    used_start_y-=20    
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]==1:
                pos = pygame.mouse.get_pos()
                if next_turn_btn.collidepoint(pos):
                    player_turn = False
                if history_btn.collidepoint(pos):
                    if not show_history:
                        show_history = True
                        show_used = False
                        show_remain = False
                    else:
                        show_history = False
                if remain_btn.collidepoint(pos):
                    if not show_remain:
                        remain_start_y = 5
                        show_remain = True
                        show_history = False
                        show_used = False
                    else:
                        show_remain = False
                if used_btn.collidepoint(pos):
                    if not show_used:
                        used_start_y = 5
                        show_used = True
                        show_remain = False
                        show_history = False
                    else:
                        show_used = False
                if quit_btn.collidepoint(pos):
                    write_game_records(rank_list,main_role,rounds)
                    logging.warning(main_role.name+' 用 '+ job_dict[main_role.main_job] + ' 打到 關卡: '+str(rounds))
                    running = False
                end_x = (len(current_cards)+1)*100
                if GAME_CONTROL and 20<=pos[0]<= end_x and player_turn and 430<=pos[1]<=570:
                    card_index = pos[0] // 100
                    if len(current_cards)<=5:
                        if card_index>=4:
                            card_index = 4
                    else:
                        if card_index>=(len(current_cards)-1):
                            card_index = len(current_cards)-1
                    main_card = current_cards[card_index]
                    if (main_role.magic - main_card.cost) >= 0:
                        current_cards.pop(card_index)
                        main_role.magic -= main_card.cost
                        if main_card.index != -1:
                            main_used_cards.append(main_card)
                            usedcardindex = [x.index for x in main_remain_deck].index(main_card.index)
                            main_remain_deck.pop(usedcardindex)
                        GAME_CONTROL,current_cards,log_text_list,takedown = use_card_effect(main_card,enemy,main_role,GAME_CONTROL,main_remain_deck,main_used_cards,current_cards,log_text_list,'player')
        if GAME_CONTROL:
            if player_turn:
                if not show_history and not show_used and not show_remain:
                    turn_index = pygame.image.load('source/mainrole_turn.png')
                    win.blit(turn_index,(280,150))
                for i in range(len(current_cards)):
                    current_cards[i].draw(win,i)
                    current_card_index += 1
                pygame.display.update()
                current_card_index = 0
                if test == 0:
                    test = 1
                    log_text = '---------------Player Turn---------------'
                    log_text_list.append(log_text)
                    log_text_list = log_text_list[-params.log_text_len:]
                    logging.info('---------------Player Turn---------------')
                if len(enemy_remain_deck) < 5:
                    enemy_return_cards = random.sample(enemy_used_cards,5-len(enemy_remain_deck))
                    enemy_remain_deck.extend(enemy_return_cards)
                    enemy_current_cards = random.sample(enemy_remain_deck,5)
                    enemy_remain_deck.extend(enemy_used_cards)
                    enemy_used_cards = []
                else:
                    enemy_current_cards = random.sample(enemy_remain_deck,5)
            else:
                if takedown:
                    player_turn = True
                # 玩家剩餘牌<5從用過的牌拉回
                if len(main_remain_deck) < main_role.every_drop:
                    return_cards = random.sample(main_used_cards,main_role.every_drop-len(main_remain_deck))
                    main_remain_deck.extend(return_cards)
                    current_cards = random.sample(main_remain_deck,main_role.every_drop)
                    main_remain_deck.extend(main_used_cards)
                    main_used_cards = []
                else:
                    current_cards = random.sample(main_remain_deck,main_role.every_drop)
                
                if test == 1:
                    check_person_buff(enemy,main_role)
                    log_text = '---------------Enemy Turn---------------'
                    log_text_list.append(log_text)
                    log_text_list = log_text_list[-params.log_text_len:]
                    logging.info('---------------Enemy Turn---------------')
                    test = 0
                if not show_history and not show_used and not show_remain:
                    enemy_turn_index = pygame.image.load('source/enemy_turn.png')
                    win.blit(enemy_turn_index,(550,150))
                    pygame.display.update()
                
                if enemy.magic > 0:
                    card = enemy.use_cardAI(enemy_current_cards)
                    if (enemy.magic - card.cost) >= 0:
                        time.sleep(0.5)
                        enemy.magic -= card.cost
                        if card.index != -1:
                            enemy_cardindex = [x.index for x in enemy_remain_deck].index(card.index)
                            enemy_remain_deck.pop(enemy_cardindex)
                            enemy_current_cardindex = [x.index for x in enemy_current_cards].index(card.index)
                            enemy_current_cards.pop(enemy_current_cardindex)
                            enemy_used_cards.append(card)

                        GAME_CONTROL,enemy_current_cards,log_text_list,_ = use_card_effect(card,main_role,enemy,GAME_CONTROL,enemy_remain_deck,enemy_used_cards,enemy_current_cards,log_text_list,'enemy')
                        
                        card.draw(win,0,450,200)
                        enemy_use_card_text = font_list[0].render("敵人使用了 "+card.name, True, BLACK)
                        win.blit(enemy_use_card_text, (370, 50))
                        pygame.display.update()
                        time.sleep(0.5)
                    else:
                        logging.info('Enemy drops new card ! ...')
                else:
                    time.sleep(1)
                    player_turn = True
                    enemy.magic = enemy.max_magic
                    main_role.magic = main_role.max_magic
                    check_person_buff(main_role,enemy)
                    
        elif not GAME_CONTROL and enemy.hp == 0:
            mm = random.randint(50,100)
            main_role.money += mm
            logging.info('勝利！獲得 '+str(mm)+' 金錢')
            rounds += 1
            if rounds % 5 == 0 and rounds != 0:
                new_card_deck = random.sample(Special_card.normal_deck+Special_card.high_level_deck+Special_card.pro_job_deck[main_role.main_job],k=3)
            else:
                new_card_deck = random.sample(Special_card.normal_deck+Special_card.pro_job_deck[main_role.main_job],k=3)
            chose_buff,add_value,new_card,main_role = win_surface(win,font_list,rounds,main_role,new_card_deck)
            
            log_text = '********* Next Round *********'
            log_text_list.append(log_text)
            log_text_list = log_text_list[-params.log_text_len:]
            logging.warning('********* Next Round *********')
            if new_card != None:
                new_card.index = len(init_main_card_deck)
                init_main_card_deck.append(new_card)
                
            main_remain_deck = init_main_card_deck.copy()
            main_used_cards = []
            current_cards = random.sample(main_remain_deck,main_role.every_drop)

            init_enemy_card_deck = enemy_init_card_deck()
            if rounds % 5 == 0 and rounds != 0:
                new_add_enemy_card.append(random.choice(enemy_normal_deck))
            enemy_remain_deck = init_enemy_card_deck.copy()
            for new_e_card in new_add_enemy_card:
                new_e_card.index = len(init_enemy_card_deck)
                enemy_remain_deck.append(new_e_card)
            enemy_used_cards = []
            enemy_current_cards = random.sample(enemy_remain_deck,5)

            if rounds % 5 != 0 or rounds == 0:
                enemy,log_text_list = set_enemy(enemy,log_text_list)
            main_role,log_text_list = set_player(main_role,chose_buff,add_value,log_text_list,new_card)
            if show_next:
                background=pygame.Surface((win.get_rect().width, win.get_rect().height))
                background.fill(BLACK)
                win.blit(background, background.get_rect())
                rounds_text1 = font_list[1].render("關卡", True, WHITE)
                rounds_text2 = font_list[1].render(str(rounds-1)+' -> '+str(rounds), True, WHITE)
                win.blit(rounds_text1, (350, 250))
                win.blit(rounds_text2, (350, 350))
                pygame.display.update()
                time.sleep(2)
                show_next = False
            GAME_CONTROL = True
        else:
            over_bg = pygame.Rect(200, 225, 500, 150) 
            pygame.draw.rect(win, BLACK , over_bg)
            over_font = pygame.font.Font(params.Font, 150)
            over_text = over_font.render("Game Over", True, RED)
            win.blit(over_text, (225, 230))
            pygame.display.update()
            time.sleep(3)
            running = False
            write_game_records(rank_list,main_role,rounds)
            logging.warning(main_role.name+' 用 '+ job_dict[main_role.main_job] + ' 打到 關卡: '+str(rounds))
        pygame.display.flip()
        clock.tick(40)"""

def write_game_records(rank_list, main_role, rounds):
    if not any(player['name'] == main_role.name for player in rank_list) or not any(player['job'] == main_role.main_job for player in rank_list):
        rank_list.append({"name":main_role.name,"job":params.player_value[main_role.main_job]['name'],"score":str(rounds)})
    else:
        for player in rank_list:
            if player['name'] == main_role.name and player['job'] == main_role.main_job and int(player['score']) < rounds:
                player['score'] = str(rounds)
    rank_list = sorted(rank_list, key=lambda k: k['score'], reverse=True)
    if len(rank_list) > 9:
        rank_list.pop(-1)
    with open('source/rankings.json','w') as f:
        json.dump(rank_list, f)
