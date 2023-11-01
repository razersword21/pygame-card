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
            target.buff.append({'fire':[card.lasting,2+myself.damage_buff]})
        case 'turtle':
            target.buff.append({'turtle':[card.lasting,1]})
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
    return target,myself

def init_card_deck(random_control:bool=None):
    card_deck = []
    deck_index = 0
    if random_control == True:
        card_type_number = [random.randint(1,10),random.randint(2,5),random.randint(2,5)]
    else:
        card_type_number = [10,5,5]
    
    for i,card_num in enumerate(card_type_number):
        for _ in range(card_num):
            if i == 0:
                card_deck.extend([Card(deck_index,params.card_name_list[i],params.card_type_list[i],1,3,0,0,None)])
            else:
                card_deck.extend([Card(deck_index,params.card_name_list[i],params.card_type_list[i],1,0,2,0,None)])
            deck_index+=1
    return card_deck

def check_person_buff(person):
    if len(person.buff) > 0:
        for i,buff in enumerate(person.buff):
            still_have_buff_ = list(buff.values())[0][0]
            if still_have_buff_ > 0:
                key = list(buff.keys())[0]
                match key:
                    case 'fire':
                        if person.de > 0:
                            person.de -= buff['fire'][1]
                        if person.de < 0:
                            person.hp -= person.de
                            person.de = 0
                        else:
                            person.hp -= buff['fire'][1]
                        buff['fire'][0]-=1
                    case 'turtle':
                        if buff['turtle'][1] > 0:
                            person.defense_buff+=2
                            person.heal_buff+=2
                            buff['turtle'][1]-=1
                        buff['turtle'][0]-=1
            else:
                if list(buff.keys())[0] == 'turtle':
                    person.defense_buff-=2
                    person.heal_buff-=2
                person.buff.pop(i)

    return person