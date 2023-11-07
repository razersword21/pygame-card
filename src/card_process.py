import random
from src.objects import *
from src.params import *

def card_effect(target,card,myself):
    match card.type:
        case 'attack'|'little_knife':
            target,myself = attack(target,card,myself,None)
            
        case 'brk_shd':
            target.de = 0
        case 'dice':
            dice_point = random.randint(1,6)
            match dice_point:
                case 6:
                    target,myself = attack(target,card,myself)
                case 5:
                    target,myself = attack(target,card,myself,1)
                case 4:
                    myself.hp += (3+myself.heal_buff)
                case 3:
                    myself.de += (3+myself.defense_buff)
                case 2:
                    myself.hp -= 5
                case 1:
                    myself.hp -= 10
        case 'sacrifice':
            target,myself = attack(target,card,myself)
            myself.hp = (0.5*myself.hp)
        case 'add_max_hp':
            target.max_hp += 5
        case 'altar':
            target.hp = (0.5*target.hp)
            target.damage_buff+=3
        case 'defense':
            target.de+=card.do_for_self+target.defense_buff
        case 'guard':
            target.de+=(target.defense_buff*2)
        case 'shield':
            if target.de > 0:
               target.de -= (myself.de)
               if target.de < 0:
                  target.hp += target.de
                  target.de = 0
            else:
                target.hp -= (myself.de)
        case 'heal':
            target.hp+=card.do_for_self+target.heal_buff
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
        case 'absorb':
            target.magic -= card.do_to_other
            if target.magic < 0:
                myself.magic -= target.magic
                target.magic = 0
            else:
                myself.magic += card.do_to_other
    return target,myself

def init_card_deck(random_control:bool=None):
    card_deck = []
    deck_index = 0
    if random_control == True:
        card_type_number = [random.randint(9,30),random.randint(3,10),random.randint(3,10)]
    else:
        card_type_number = params.card_type_number
    
    for i,card_num in enumerate(card_type_number):
        for _ in range(card_num):
            if i == 0:
                card_deck.extend([Card(deck_index,params.card_name_list[i],params.card_type_list[i],1,3,0,0,None)])
            else:
                card_deck.extend([Card(deck_index,params.card_name_list[i],params.card_type_list[i],1,0,2,0,None)])
            deck_index+=1
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
                            buff['keep_heal'][0]-=1
                            if buff['keep_heal'][0] == 0:
                                person.buff.pop(i)
                        case 'add_magic':
                            person.magic += 2
                            buff['add_magic'][0]-=1
                            if buff['add_magic'][0] == 0:
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
    return person

def duoble_buff(card,target):
    if any(card.type in b for b in target.buff):
        for buff_ in target.buff:
            try:
                buff_[card.type][0]+=card.lasting
            except:
                pass
    else:
        if card.type != 'fire':
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