from src.background import *

class Special_card():
    
    return_card = Card(-1,'重抽','return',1,0,0,0,'重新抽\n  5張手牌')
    drop_card = Card(-1,"抽兩張",'drop',1,0,0,0,'多抽兩張')
    turtle_card = Card(-1,'龜化','turtle',1,0,0,3,'成為烏龜3回合\n 防禦+2\n 治癒+2\n 傷害-2')
    knife_card = Card(-1,'小刀*2','knife',1,0,0,0,'生成2張\n  小刀\n該回合沒用\n 即消失')
    Vampire_card = Card(-1,'壓榨','vampire',2,3,0,0,'造成3傷害\n 治癒自身3hp')
    magic_card = Card(-1,'吸魔','absorb',1,2,0,0,'吸取對方\n  2Mp')
    shield_bash = Card(-1,"盾擊",'shield',1,0,2,0,'造成自身\n當前防禦值\n的傷害')
    sacrifice_card = Card(-1,'捨身','sacrifice',1,10,0,0,'造成10點傷害\n也對自己造成\n當前50%hp傷害')
    normal_deck = [Vampire_card,magic_card,drop_card,return_card,knife_card,turtle_card,shield_bash] 

    max_hp_card = Card(-1,'Hp上限+','add_max_hp',2,0,5,0,'增加血量上限\n  +5')
    altar_card = Card(-1,'獻祭','altar',2,0,0,0,'以目前50%hp\n換來damage+1')
    high_level_deck = [altar_card,max_hp_card]
    
    dragon_card = Card(-1,'化龍','dragon',2,0,0,3,'化龍3回合\n 防禦+4\n 治癒+4\n 傷害+4')
    guard_card = Card(-1,'神聖之盾','guard',1,0,3,0,'獲得自身\n 防禦增強\n 2倍的盾')
    defense_card = Card(-1,'防禦','defense',1,0,2,0,'獲得 2 護甲')
    double_defense = Card(-1,'疊盾','double_defense',1,0,3,0,'獲得自身\n 防禦\n 2倍的盾')
    sword_card = Card(-1,'劍術精通','sword',1,0,0,3,'傷害+2 \n 持續3回合')
    knight_deck = [dragon_card,guard_card,defense_card,double_defense,sword_card]
    add_magic = Card(-1,'回魔','add_magic',2,0,2,2,'兩回合\n  Mp+2')
    fire_card = Card(-1,'燃燒','fire',1,2,0,2,'每回合燒\n 敵人2hp\n 持續2回合')
    mud_card = Card(-1,'土盾','mud',1,2,0,3,'每回合獲得\n 2 護甲\n 持續3回合')
    thurder_card = Card(-1,'雷擊','thurder',2,2,0,0,'造成2點傷害\n30%使敵人暫停一回合')
    
    magic_deck = [fire_card,mud_card,thurder_card]
    broke_shield = Card(-1,'破盾','brk_shd',2,0,0,0,'消除所有\n  護盾值')
    penetrate = Card(-1,'破甲箭','penetrate',1,2,0,0,'無視防禦\n造成真實傷害')
    poison = Card(-1,'塗毒','poison',1,2,0,2,'造成2傷害\n敵人虛弱2回合\n虛弱:damage-50%')
    archer_deck = [broke_shield,penetrate,poison]
    dice_card = Card(-1,'幸運骰子','dice',1,5,3,0,'隨機執行動作\n6:5傷 5:1傷\n4:+3hp 3:+3de\n2:-5hp 1:-10hp')
    steal_card = Card(-1,'竊取','steal',1,2,0,0,'造成2傷害\n並隨機偷取對方\n0~30 Money')
    row_card = Card(-1,'輪盤','row',1,4,2,0,'隨機執行動作\n1:敵人補兩hp\n2:自己補2hp\n3:傷害敵人4hp\n4:傷害自己4hp')
    theif_card = [dice_card,steal_card,row_card]
    keep_heal = Card(-1,"回春",'keep_heal',2,0,3,2,'持續回自身\n  治癒增強\n  *2的血量\n  3回合') 
    stick_card = Card(-1,'當頭棒喝','stick',2,1,0,0,'造成1+生命上限30%傷害')
    heal_card = Card(-1,'治癒','heal',1,0,2,0,'治癒 2 hp')
    priest_deck = [max_hp_card,keep_heal,stick_card,heal_card]
    pro_job_deck = {1:knight_deck,2:magic_deck,3:archer_deck,4:[],5:theif_card,6:priest_deck}

class params():
    init_max_hp, init_max_de, init_max_magic, money = 20, 0, 3, 0
    player_value = {
        1:{'name':'騎士','max_hp':25,'max_de':0,'damage_b':1,'defense_b':2,'heal_b':0,'magic':2,'money':100},
        2:{'name':'魔法師','max_hp':15,'max_de':0,'damage_b':0,'defense_b':0,'heal_b':1,'magic':4,'money':50},
        3:{'name':'弓箭手','max_hp':20,'max_de':0,'damage_b':1,'defense_b':0,'heal_b':0,'magic':3,'money':0},
        4:{'name':'凡人','max_hp':10,'max_de':0,'damage_b':0,'defense_b':0,'heal_b':0,'magic':3,'money':0},
        5:{'name':'盜賊','max_hp':20,'max_de':0,'damage_b':1,'defense_b':-1,'heal_b':0,'magic':3,'money':25},
        6:{'name':'牧師','max_hp':25,'max_de':0,'damage_b':0,'defense_b':0,'heal_b':2,'magic':3,'money':0}
    }
    enemy_max_hp,enemy_max_de,enemy_max_magic = 10,0,3
    add_hp = 10
    add_value = 1
    add_pass_money = 150
    card_name_list = ['攻擊','防禦','治癒']
    card_type_list = ['attack','defense','heal']
    card_type_number = [5,3,3]
    card_init_damage = 2
    init_defense_or_heal = 2
    Font = 'source/font/ChenYuluoyan-Thin.ttf'
    log_text_len = 10
    job_descriptions = {
        1: "帝國之盾\n從小接受騎士教育\n因此熟練劍盾使用\n但智力相對較低\n遇到挑戰動作單一\n初始專屬卡 - 神聖之盾\n獲得自身防禦buff*2的護盾",
        2: "賢者之父\n為帝國賢者的父親\n不要妄想如兒子般\n但至少智力比騎士高\n初始專屬卡 - 回魔\n兩回合MP+2",
        3: "普通的神箭手\n平常一直練習射箭\n所有人事物都是目標\n因為得罪太多人\n被趕來挑戰輪迴\n初始專屬卡 - 破甲箭\n無視防禦造成真實傷害",
        5: "沉迷賭博的盜賊\n不小心沉迷賭博之人\n所有動作充滿隨機與竊取\n初始專屬卡 - 竊取\n造成2傷害並隨機偷取0~30 Money",
        6: "健身牧師-甲\n不要問為何血量如此\n一切都是平常的努力\n甚至攻擊都是基於血量與超出補血量\n初始專屬卡 - 當頭棒喝\n造成1+生命上限30%傷害"
    }