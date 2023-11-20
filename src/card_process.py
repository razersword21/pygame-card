import random
import math
import logging
logging.basicConfig(level=logging.INFO)
from src.objects import *
from src.params import *

def card_effect(target,card,myself,log_text):
    match card.type:
        case 'attack'|'little_knife':
            target,myself = attack(target,card,myself,None)
            log_text += "造成 " + str(card.do_to_other+myself.damage_buff) + " 傷害"
        case 'brk_shd':
            log_text += "破甲 : "+str(target.de)+' > 0'
            target.de = 0
        case 'thurder':
            target,myself = attack(target,card,myself,None)
            log_text += "造成 " + str(card.do_to_other+myself.damage_buff) + " 傷害"
        case 'dice':
            dice_point = random.randint(1,6)
            log_text += "你骰到"+str(dice_point)+' '
            match dice_point:
                case 6:
                    target,myself = attack(target,card,myself)
                    log_text +="造成 " + str(card.do_to_other+myself.damage_buff) + " 傷害"
                case 5:
                    target,myself = attack(target,card,myself,1)
                    log_text +="造成 " + str(1+myself.damage_buff) + " 傷害"
                case 4:
                    myself.hp += (3+myself.heal_buff)
                    log_text +="治癒 "+str((3+myself.heal_buff))
                case 3:
                    myself.de += (3+myself.defense_buff)
                    log_text +="獲得護甲 "+str((3+myself.defense_buff))
                case 2:
                    myself.hp -= 5
                    log_text +="傷害自己 5 hp"
                case 1:
                    myself.hp -= 10
                    log_text +="傷害自己 10 hp"
            
        case 'row':
            dice_point = random.randint(1,4)
            log_text += "你轉到"+str(dice_point)+' '
            match dice_point:
                case 4:
                    myself.hp -= 4
                    log_text +="傷害自己 4 hp"
                case 3:
                    target,myself = attack(target,card,myself)
                    log_text +="造成 " + str(card.do_to_other+myself.damage_buff) + " 傷害"
                case 2:
                    myself.hp += (2+myself.heal_buff)
                    log_text +="治癒 "+str((2+myself.heal_buff))
                case 1:
                    target.hp += 2
                    log_text +="治癒敵人 "+str(3)
        case 'sacrifice':
            target,myself = attack(target,card,myself)
            myself.hp = math.floor(0.5*myself.hp)
            log_text +="造成 " + str(card.do_to_other+myself.damage_buff) + " 傷害 "+'生命 -'+str(math.floor(0.5*myself.hp))
        case 'add_max_hp':
            target.max_hp += 5
            log_text +='+5生命上限'
        case 'altar':
            target.hp = math.floor(0.5*target.hp)
            target.damage_buff+=1
            log_text +='以生命'+str(math.floor(0.5*target.hp))+' 換來damage_buff+1'
        case 'defense':
            target.de+=card.do_for_self+target.defense_buff
            log_text += '補 ' + str(card.do_for_self+target.defense_buff) + ' 護盾'
        case 'guard':
            target.de+=(target.defense_buff*2)
            log_text += '補 ' + str(target.defense_buff*2) + ' 護盾'
        case 'shield':
            if target.de > 0:
               target.de -= (myself.de)
               if target.de < 0:
                  target.hp += target.de
                  target.de = 0
            else:
                target.hp -= (myself.de)
            log_text +="造成 " + str(myself.de) + " 傷害"
        case 'heal':
            target.hp+=card.do_for_self+target.heal_buff
            log_text += '補 ' + str(card.do_for_self+target.heal_buff) + ' hp'
        case 'fire':
            target,myself = attack(target,card,myself)
            duoble_buff(card,target)
        case 'vampire':
            if target.de > 0:
               target.de -= (card.do_to_other+myself.damage_buff)
               if target.de < 0:
                  target.hp += target.de
                  target.de = 0
                  myself.hp -= target.de
            else:
                target.hp -= (card.do_to_other+myself.damage_buff)
                myself.hp += (card.do_to_other+myself.damage_buff)
            if myself.hp > myself.max_hp:
                myself.hp = myself.max_hp
            log_text +="造成 " + str(card.do_to_other+myself.damage_buff) + " 傷害 補 "+str(card.do_to_other+myself.damage_buff)+' hp'
        case 'absorb':
            target.magic -= card.do_to_other
            myself.magic += card.do_to_other
            log_text += '吸收 ' + str(card.do_to_other) + ' mp'
        case 'steal':
            target,myself = attack(target,card,myself,None)
            k = random.randint(0,30)
            myself.money += k
            log_text += "造成 "+str(card.do_to_other+myself.damage_buff) + " 傷害 偷到 "+str(k)
        case 'stick':
            da = card.do_to_other+math.ceil(myself.max_hp*0.3)
            target,myself = attack(target,card,myself,da)
            log_text += "造成 "+str(da)+ " 傷害"
        case 'penetrate':
            target.hp -= (card.do_to_other+myself.damage_buff)
            log_text += "造成 "+str(card.do_to_other+myself.damage_buff)+ " 真實傷害"
    return target,myself,log_text

def enemy_init_card_deck():
    card_deck = []
    deck_index = 0
    card_type_number = [random.randint(5,20),random.randint(3,10),random.randint(3,10)]
    for i,card_num in enumerate(card_type_number):
        for _ in range(card_num):
            if i == 0:
                card_deck.extend([Card(deck_index,params.card_name_list[i],params.card_type_list[i],1,params.card_init_damage,0,0,None)])
            else:
                card_deck.extend([Card(deck_index,params.card_name_list[i],params.card_type_list[i],1,0,params.init_defense_or_heal,0,None)])
            deck_index+=1
    return card_deck

def init_card_deck(person):
    card_deck = []
    deck_index = 0
    card_type_number = params.card_type_number
    for i,card_num in enumerate(card_type_number):
        for _ in range(card_num):
            if i == 0:
                card_deck.extend([Card(deck_index,params.card_name_list[i],params.card_type_list[i],1,params.card_init_damage,0,0,None)])
            else:
                card_deck.extend([Card(deck_index,params.card_name_list[i],params.card_type_list[i],1,0,params.init_defense_or_heal,0,None)])
            deck_index+=1
    match person.main_job:
        case 1:
            pro_card = Special_card.guard_card
        case 2:
            pro_card = Special_card.add_magic
        case 3:
            pro_card = Special_card.penetrate
        case 5:
            pro_card = Special_card.steal_card
        case 6:
            pro_card = Special_card.stick_card
    if person.main_job != 4:
        pro_card.index = len(card_deck)
        card_deck.extend([pro_card])
    return card_deck

def check_person_buff(person,enemy,card_type=None):
    if len(person.buff) > 0:
        for i,buff in enumerate(person.buff):
            still_have_buff_ = list(buff.values())[0][0]
            if still_have_buff_ > 0:
                key = list(buff.keys())[0]
                if card_type == None:
                    match key:
                        case 'fire':
                            if person.de > 0:
                                person.de -= buff['fire'][1]+enemy.damage_buff
                            if person.de < 0:
                                person.hp -= person.de
                                person.de = 0
                            else:
                                person.hp -= buff['fire'][1]+enemy.damage_buff
                            buff['fire'][0]-=1
                            if buff['fire'][0] == 0:
                                person.buff.pop(i)
                        case 'poison':
                            person.damage_buff = math.ceil(person.damage_buff*0.5)
                            buff['poison'][0]-=1
                            if buff['poison'][0] == 0:
                                person.buff.pop(i)    
                        case 'turtle':
                            buff['turtle'][0]-=1
                            if buff['turtle'][0] == 0:
                                person.defense_buff-=2
                                person.heal_buff-=2
                                person.buff.pop(i)
                        case 'dragon':
                            buff['dragon'][0]-=1
                            if buff['dragon'][0] == 0:
                                person.defense_buff-=4
                                person.heal_buff-=4
                                person.damage_buff-=4
                                person.buff.pop(i)
                        case 'keep_heal':
                            person.hp+=(person.heal_buff)*2
                            if person.hp > person.max_hp:
                                person.hp=person.max_hp
                                more_hp = person.hp-person.max_hp
                                if enemy.de > 0:
                                    enemy.de -= (more_hp)
                                    if enemy.de < 0:
                                        enemy.hp += enemy.de
                                        enemy.de = 0
                                else:
                                    enemy.hp -= (more_hp)
                            buff['keep_heal'][0]-=1
                            if buff['keep_heal'][0] == 0:
                                person.buff.pop(i)
                        case 'add_magic':
                            person.magic += 2
                            buff['add_magic'][0]-=1
                            if buff['add_magic'][0] == 0:
                                person.buff.pop(i)
                        case 'mud':
                            person.de += 2 + person.defense_buff
                            buff['mud'][0]-=1
                            if buff['mud'][0] == 0:
                                person.buff.pop(i)
                else:
                    if card_type == 'turtle':
                        if buff[card_type][1] > 0:
                            person.defense_buff+=2
                            person.heal_buff+=2
                            buff[card_type][1]-=1
                    if card_type == 'dragon':
                        if buff[card_type][1] > 0:
                            person.defense_buff+=4
                            person.heal_buff+=4
                            person.damage_buff+=4
                            buff[card_type][1]-=1
                    if card_type == 'keep_heal':
                        if buff[card_type][1] > 0:
                            person.hp+=(person.heal_buff)*2
                            buff[card_type][1]-=1
                    if card_type == 'add_magic':
                        if buff[card_type][1] > 0:
                            person.magic += 2
                            buff[card_type][1]-=1
                    if card_type == 'add_magic':
                        if buff[card_type][1] > 0:
                            person.de += 2 + person.defense_buff
                            buff[card_type][1]-=1
                    if card_type == 'poison':
                        if buff[card_type][1] > 0:
                            person.damage_buff = math.ceil(person.damage_buff*0.5)
                            buff[card_type][1]-=1
    return person

def duoble_buff(card,target):
    if any(card.type in b for b in target.buff):
        for buff_ in target.buff:
            try:
                buff_[card.type][0]+=card.lasting
            except:
                pass
    else:
        if card.type != 'fire'|'poison':
            target.buff.append({card.type:[card.lasting,1]})
        else:
            target.buff.append({card.type:[card.lasting,card.do_to_other]})

def attack(target,card,myself,k=None):
    if k != None:
        damage = k
    else:
        damage = card.do_to_other
    if target.de > 0:
        target.de -= (damage+myself.damage_buff)
        if target.de < 0:
            target.hp += target.de
            target.de = 0
    else:
        target.hp -= (damage+myself.damage_buff)
    
    return target,myself

def use_card_effect(main_card,enemy,main_role,GAME_CONTROL,main_remain_deck,main_used_cards,current_cards,log_text_list,name):
    value = ''
    log_text = main_role.name+' 打出 '+main_card.name+' '
    takedown = False
    match main_card.type:
        case 'attack'|'fire'|'vampire'|'absorb'|'little_knife'|'shield'|'brk_shd'|'sacrifice'|'dice'|'steal'|'stick'|'penetrate'|'row'|'thurder':
            enemy,main_role,log_text = card_effect(enemy,main_card,main_role,log_text)
            value = str(main_card.do_to_other+main_role.damage_buff)
            if main_card.type == 'thurder':
                d = random.randint(1,100)
                if d <= 30:
                    takedown = True
            if enemy.hp <= 0:
                enemy.hp = 0
                GAME_CONTROL = False
        case 'defense'|'heal'|'guard'|'altar'|'add_max_hp':
            if main_card.type in ['defense','guard']:
                value = str(main_card.do_for_self+main_role.defense_buff)
            else:
                value = str(main_card.do_for_self+main_role.heal_buff)
            main_role,enemy,log_text = card_effect(main_role,main_card,enemy,log_text)
            if main_role.hp > main_role.max_hp:
                if name == 'player':
                    if main_role.main_job == 6:
                        more_hp = main_role.hp-main_role.max_hp
                        if enemy.de > 0:
                            enemy.de -= (more_hp)
                            if enemy.de < 0:
                                enemy.hp += enemy.de
                                enemy.de = 0
                        else:
                            enemy.hp -= (more_hp)
                main_role.hp = main_role.max_hp                           
            if enemy.hp <= 0:
                enemy.hp = 0
                GAME_CONTROL = False
        case 'return':
            current_cards = random.sample(main_remain_deck,main_role.every_drop)
            log_text += '=> 重抽手牌'
        case 'drop':
            if (len(current_cards)+2) <= main_role.max_card:
                new_drop = random.sample(main_remain_deck,2)
                current_cards.extend(new_drop)
                log_text += '=> 多抽 2 手牌'
            else:
                limit_crad = main_role.max_card - len(current_cards)
                log_text += '=> 因為最多只能持9張手牌，因此多抽 '+str(limit_crad)+' 手牌'
                new_drop = random.sample(main_remain_deck,limit_crad)
                current_cards.extend(new_drop)
        case 'knife':
            log_text += '=> 生成 2 張0費小刀，本回合沒用就消失'
            little_knife = Card(-1,'小刀','little_knife',0,2,0,0,'消逝')
            new_drop = [little_knife,little_knife]
            current_cards.extend(new_drop)
        case 'turtle'|'keep_heal'|'add_magic'|'dragon'|'mud'|'poison':
            value = '持續 '+str(main_card.lasting) + ' 回合'
            log_text += value + '效果: ' + (main_card.special.replace('\n',' '))
            if main_card.type == 'poison':
                target,myself = attack(target,main_card,myself,None)
            duoble_buff(main_card,main_role)
            check_person_buff(main_role,enemy,main_card.type)
            if enemy.hp <= 0:
                enemy.hp = 0
                GAME_CONTROL = False
    logging.info(main_role.name+' 打出 '+main_card.name+' '+value+' | '
            +'剩餘卡牌:'+str(len(main_remain_deck))+' | 用過卡牌:'+str(len(main_used_cards))+'\n'
            +main_role.name+' 狀態: Hp '+str(main_role.hp)+' De '+str(main_role.de)+' mp '+str(main_role.magic)+' Buff '+str(main_role.buff)+'\n'
            +enemy.name+' 狀態: Hp '+str(enemy.hp)+' De '+str(enemy.de)+' mp '+str(enemy.magic)+' Buff '+str(enemy.buff))
    log_text_list.append(log_text)
    log_text_list = log_text_list[-params.log_text_len:]
    return GAME_CONTROL,current_cards,log_text_list,takedown