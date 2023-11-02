from objects import *

RED = (255,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

class Special_card():
    fire_card = Card(-1,'燃燒','fire',1,2,0,2,'每回合燒\n 敵人2hp\n 持續2回合')
    return_card = Card(-1,'重抽','return',1,0,0,0,'重新抽\n  5張手牌')
    drop_card = Card(-1,"抽兩張",'drop',1,0,0,0,'多抽兩張')
    turtle_card = Card(-1,'龜化','turtle',1,0,0,2,'成為烏龜2回合\n 防禦+2\n 治癒+2\n 傷害-2')
    knife_card = Card(-1,'小刀*2','knife',1,0,0,0,'生成2張\n  小刀\n該回合沒用\n 即消失')
    Vampire_card = Card(-1,'壓榨','vampire',2,3,0,0,'造成3傷害\n 治癒自身3hp')
    magic_card = Card(-1,'吸魔','absorb',2,2,0,0,'吸取對方\n  2Mp')
    shield_bash = Card(-1,"盾擊",'shield',2,0,2,0,'造成自身\n當前防禦值\n的傷害')
    normal_deck = [Vampire_card,magic_card,drop_card,fire_card,return_card,knife_card,turtle_card,shield_bash] 
    # normal_deck = []

    guard_card = Card(-1,'神聖之盾','guard',2,0,2,0,'獲得自身防禦增強\n 2倍的盾')
    keep_heal = Card(-1,"回春",'keep_heal',2,0,2,2,'持續回自身治癒增強\n  *2的血量\n  2回合')
    add_magic = Card(-1,'回魔','add_magic',2,0,2,2,'兩回合\n  Mp+2')
    high_level_deck = [guard_card,keep_heal,add_magic]

class params():
    
    init_max_hp,init_max_de,init_max_magic,money = 10,0,3,0
    add_hp = 20
    add_value = 1
    add_pass_money = 150
    card_name_list = ['攻擊','防禦','治癒']
    card_type_list = ['attack','defense','heal']
    card_type_number = [9,3,3]