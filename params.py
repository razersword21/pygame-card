from objects import *

RED = (255,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

class Special_card():
    fire_card = Card(-1,'燃燒','fire',1,2,0,2,'每回合燒敵人2hp\n 持續2回合')
    return_card = Card(-1,'重抽','return',1,0,0,0,'重新抽5張手牌')
    drop_card = Card(-1,"抽兩張",'drop',1,0,0,0,'多抽兩張')
    turtle_card = Card(-1,'烏龜','turtle',1,0,0,1,'成為烏龜\n 防禦+2\n 治癒+2\n 傷害-2')
    knife_card = Card(-1,'小刀*2','knife',1,0,0,0,'生成2張\n   小刀')
    Vampire_card = Card(-1,'壓榨','vampire',2,3,0,0,'造成3傷害\n 治癒自身3hp')
    magic_card = Card(-1,'吸魔','absorb',2,2,0,0,'吸取對方2Mp')
    normal_deck = [Vampire_card,magic_card,drop_card,fire_card,return_card,knife_card,turtle_card] # 

    guard_card = Card(-1,'神聖之盾','guard',2,0,2,0,'獲得自身防禦增強\n 2倍的盾')
    high_level_deck = [guard_card]

class params():
    
    init_max_hp,init_max_de,init_max_magic,money = 10,0,3,0
    add_hp = 20
    add_value = 1
    add_pass_money = 200
    card_name_list = ['攻擊','防禦','治癒']
    card_type_list = ['attack','defense','heal']
    card_type_number = [5,3,0]