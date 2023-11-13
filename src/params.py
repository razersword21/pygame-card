from src.objects import *

RED = (255,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

class Special_card():
    fire_card = Card(-1,'燃燒','fire',1,2,0,2,'每回合燒\n 敵人2hp\n 持續2回合')
    return_card = Card(-1,'重抽','return',1,0,0,0,'重新抽\n  5張手牌')
    drop_card = Card(-1,"抽兩張",'drop',1,0,0,0,'多抽兩張')
    turtle_card = Card(-1,'龜化','turtle',1,0,0,3,'成為烏龜3回合\n 防禦+2\n 治癒+2\n 傷害-2')
    knife_card = Card(-1,'小刀*2','knife',1,0,0,0,'生成2張\n  小刀\n該回合沒用\n 即消失')
    Vampire_card = Card(-1,'壓榨','vampire',2,3,0,0,'造成3傷害\n 治癒自身3hp')
    magic_card = Card(-1,'吸魔','absorb',1,2,0,0,'吸取對方\n  2Mp')
    shield_bash = Card(-1,"盾擊",'shield',2,0,2,0,'造成自身\n當前防禦值\n的傷害')
    sacrifice_card = Card(-1,'捨身','sacrifice',1,10,0,0,'造成10點傷害\n也對自己造成\n當前50%hp傷害')
    altar_card = Card(-1,'獻祭','altar',2,0,0,0,'以目前50%hp\n換來damage+3')
    normal_deck = [Vampire_card,magic_card,drop_card,fire_card,return_card,knife_card,turtle_card,shield_bash,altar_card] 
    # normal_deck = [fire_card]
    guard_card = Card(-1,'神聖之盾','guard',2,0,3,0,'獲得自身\n 防禦增強\n 2倍的盾')
    keep_heal = Card(-1,"回春",'keep_heal',2,0,3,2,'持續回自身\n  治癒增強\n  *2的血量\n  3回合')
    add_magic = Card(-1,'回魔','add_magic',2,0,2,2,'兩回合\n  Mp+2')
    dragon_card = Card(-1,'化龍','dragon',2,0,0,3,'化龍3回合\n 防禦+4\n 治癒+4\n 傷害+4')
    broke_shield = Card(-1,'破盾','brk_shd',2,0,0,0,'消除所有\n  護盾值')
    max_hp_card = Card(-1,'血量上限+','add_max_hp',2,0,5,0,'增加血量上限\n  +5')
    dice_card = Card(-1,'幸運骰子','dice',1,5,3,0,'隨機執行動作\n6:5傷 5:1傷\n4:+3hp 3:+3de\n2:-5hp 1:-10hp')
    high_level_deck = [guard_card,keep_heal,add_magic,dragon_card,broke_shield,max_hp_card,dice_card]

class params():
    init_max_hp,init_max_de,init_max_magic,money = 20,0,3,0
    player_value = {1:{'name':'騎士','max_hp':25,'max_de':0,'damage_b':2,'defense_b':2,'heal_b':0,'magic':2,'money':400},
                    2:{'name':'魔法師','max_hp':15,'max_de':0,'damage_b':0,'defense_b':0,'heal_b':1,'magic':4,'money':0},
                    3:{'name':'弓箭手','max_hp':20,'max_de':0,'damage_b':1,'defense_b':0,'heal_b':0,'magic':3,'money':50},
                    4:{'name':'凡人','max_hp':10,'max_de':0,'damage_b':0,'defense_b':0,'heal_b':0,'magic':3,'money':0}}
    enemy_max_hp,enemy_max_de,enemy_max_magic = 10,0,3
    add_hp = 10
    add_value = 1
    add_pass_money = 150
    card_name_list = ['攻擊','防禦','治癒']
    card_type_list = ['attack','defense','heal']
    card_type_number = [10,3,3]
    card_init_damage = 3
    init_defense_or_heal = 2
    Font = 'source/font/ChenYuluoyan-Thin.ttf'
    log_text_len = 10