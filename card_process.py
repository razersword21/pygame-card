import random
from objects import *
from params import *

def card_effect(target,card,myself):
    match card.type:
        case 'attack':
            if target.de > 0:
               target.de -= (card.do_to_other+myself.damage_buff)
               if target.de < 0:
                  target.hp += target.de
                  target.de = 0
            else:
                target.hp -= (card.do_to_other+myself.damage_buff)
        case 'defense':
            target.de+=card.do_for_self+target.defense_buff
        case 'guard':
            target.de+=(target.defense_buff*2)
        case 'heal':
            target.hp+=card.do_for_self+target.heal_buff
        case 'fire':
            if target.de > 0:
               target.de -= (card.do_to_other+myself.damage_buff)
               if target.de < 0:
                  target.hp += target.de
                  target.de = 0
            else:
                target.hp -= (card.do_to_other+myself.damage_buff)
            target.buff.append({'fire':[card.lasting,2,1]})
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
        case 'absorb':
            target.magic -= card.do_to_other
            myself.magic += card.do_to_other
        case 'little_knife':
            if target.de > 0:
               target.de -= (card.do_to_other+myself.damage_buff)
               if target.de < 0:
                  target.hp += target.de
                  target.de = 0
            else:
                target.hp -= (card.do_to_other+myself.damage_buff)
    return target,myself

def init_card_deck(random_control:bool=None):
    card_deck = []
    deck_index = 0
    if random_control == True:
        card_type_number = [random.randint(5,10),random.randint(3,5),random.randint(1,5)]
    else:
        card_type_number = params.card_type_number
    
    for i,card_num in enumerate(card_type_number):
        for _ in range(card_num):
            if i == 0:
                card_deck.extend([Card(deck_index,params.card_name_list[i],params.card_type_list[i],1,4,0,0,None)])
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
                        case 'keep_heal':
                            person.hp+=(person.heal_buff)*2
                            buff['keep_heal'][0]-=1
                            if buff['keep_heal'][0] == 0:
                                person.buff.pop(i)    
                else:
                    if card_type == 'turtle':
                        if buff[card_type][1] > 0:
                            person.defense_buff+=2
                            person.heal_buff+=2
                            buff[card_type][1]-=1
                    if card_type == 'keep_heal':
                        if buff[card_type][1] > 0:
                            person.hp+=(person.heal_buff)*2
                            buff[card_type][1]-=1
    return person
