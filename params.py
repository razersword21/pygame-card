from objects import *

RED = (255,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

class Special_card():
    fire_card = Card(-1,'燃燒','fire',1,2,0,2,'每回合燒敵人2hp\n  持續2回合')
    return_card = Card(-1,'重抽','return',1,0,0,0,'重新抽5張手牌')
    drop_card = Card(-1,"抽兩張",'drop',1,0,0,0,'多抽兩張')
    turtle_card = Card(-1,'烏龜模式','turtle',1,0,0,3,'成為烏龜\n 防禦+2\n 治癒+2\n 傷害-2')
    normal_deck = [drop_card,fire_card,return_card,turtle_card]

    Vampire_card = Card(-1,'壓榨','vampire',2,3,0,0,'造成3傷害\n治癒自身3hp')
    magic_card = Card(-1,'吸魔','absorb',2,2,0,0,'吸取對方2Mp')
    guard_card = Card(-1,'神聖之盾','guard',2,0,2,0,'獲得自身防禦\n  2倍的盾')
    high_level_deck = [Vampire_card,magic_card,guard_card]

class params():
    
    add_hp = 20
    add_value = 1
    add_money = 15
    card_name_list = ['攻擊','防禦','治癒']
    card_type_list = ['attack','defense','heal']