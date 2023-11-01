import pygame,sys
import random
from objects import *
from card_process import *
from choose import *
from params import *
import logging
logging.basicConfig(level=logging.INFO)

def set_enemy(enemy):
    x = random.randint(0,100)
    if x <= 35:
        enemy.max_hp += params.add_hp
        logging.info(enemy.name+' 對於 hp 增強了!')
    if x > 45 and x < 55:
        enemy.damage_buff += params.add_value
        logging.info(enemy.name+' 對於 damage 增強了!')
    if x >= 55:
        enemy.defense_buff += params.add_value
        enemy.heal_buff += params.add_value
        logging.info(enemy.name+' 對於 defense & heal 增強了!')
    if x > 35 and x < 45:
        enemy.max_magic += params.add_value
        logging.info(enemy.name+' 對於 magic 增強了!')
    enemy.hp = enemy.max_hp
    enemy.magic = enemy.max_magic
    return enemy

def set_player(main_role,choose,add_value):
    if choose == 'hp':
        main_role.max_hp += add_value
        main_role.money += random.randint(50,100)
        logging.info(main_role.name+' 對於 Hp 增強了!')
    elif choose == 'all':
        y = random.randint(0,2)
        match y:
            case 0:
                main_role.damage_buff += add_value
                choose = 'damage'
            case 1:
                main_role.defense_buff += add_value
                choose = 'defense'
            case 2:
                main_role.heal_buff += add_value
                choose = 'heal'
        main_role.money += random.randint(50,100)
        logging.info(main_role.name+' 對於 '+choose+' 屬性增強了!')
    elif choose == '':
        main_role.money += params.add_pass_money
        logging.info(main_role.name+'放棄選擇 ， 獲得錢幣 +200 !')
    else:
        logging.info(main_role.name+' 選擇特殊卡 !')
    main_role.hp = main_role.max_hp
    main_role.magic = main_role.max_magic
    return main_role

def game_(win,font_list,GAME_CONTROL):
    bg = BG(900, 600)
    rounds = 0
    
    chose_buff = []
    enemy = Enemy(params.init_max_hp,params.init_max_de,params.init_max_magic)
    main_role = Main_role(params.init_max_hp,params.init_max_de,params.init_max_magic,params.money)

    running = True 
    player_turn = True
    next_turn_btn_press_down = True

    init_enemy_card_deck = init_card_deck(True)
    init_main_card_deck = init_card_deck()

    main_remain_deck = init_main_card_deck.copy()
    main_used_cards = []
    current_cards = random.sample(main_remain_deck,main_role.every_drop)
    
    enemy_remain_deck = init_enemy_card_deck.copy()
    enemy_normal_deck = Special_card.normal_deck.copy()
    enemy_high_level_deck = Special_card.high_level_deck.copy()
    enemy_used_cards = []
    new_add_enemy_card = []
    
    test,current_card_index = 0,0
    while running:
                
        win.blit(bg.bg_big, bg.rect)
        Rounds_text = font_list[0].render("Rounds: "+str(rounds), True, BLACK)
        win.blit(Rounds_text, (10, 10))

        main_role.draw(win,200,300)
        enemy.draw(win,700,300,0)

        player_hp_text = font_list[0].render("HP:"+str(main_role.hp)+"|"+str(main_role.max_hp), True, RED)
        player_de_text = font_list[0].render("Def: "+str(main_role.de), True, BLUE)
        player_mp_text = font_list[0].render("MP: "+str(main_role.magic), True, BLACK)
        player_money_text = font_list[0].render("Money: "+str(main_role.money), True, YELLOW)
        player_value_text = font_list[0].render("Damage: "+str(main_role.damage_buff)+'\nDef: '
                                        +str(main_role.defense_buff)+'\nHeal: '+str(main_role.heal_buff), True, PURPLE)
        win.blit(player_hp_text, (75, 140))
        win.blit(player_de_text, (170, 140))
        win.blit(player_mp_text, (240, 140))
        win.blit(player_money_text, (755, 500))
        win.blit(player_value_text, (10, 200))

        enemy_hp_text = font_list[0].render("HP: "+str(enemy.hp)+"|"+str(enemy.max_hp), True, RED)
        enemy_de_text = font_list[0].render("Def: "+str(enemy.de), True, BLUE)
        enemy_mp_text = font_list[0].render("MP: "+str(enemy.magic), True, BLACK)
        enemy_value_text = font_list[0].render("Damage: "+str(enemy.damage_buff)+'\nDef: '
                                        +str(enemy.defense_buff)+'\nHeal: '+str(enemy.heal_buff), True, PURPLE)
        win.blit(enemy_hp_text, (580, 140))
        win.blit(enemy_de_text, (685, 140))
        win.blit(enemy_mp_text, (750, 140))
        win.blit(player_value_text, (780, 200))

        next_turn_btn = pygame.Rect(750, 555, 110, 30) 
        next_turn_down_btn = pygame.Rect(750, 555, 110, 30) 
        if next_turn_btn_press_down:
            pygame.draw.rect(win, RED , next_turn_btn)
        else:
            pygame.draw.rect(win, BLUE , next_turn_down_btn)

        btn_text = font_list[0].render("Next Turn", True, WHITE)
        win.blit(btn_text, (755, 560))
        quit_btn = pygame.Rect(820, 20, 65, 30) 
        pygame.draw.rect(win, BLACK , quit_btn)
        quit_text = font_list[0].render("Quit", True, WHITE)
        win.blit(quit_text, (825, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                next_turn_btn_press_down = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if next_turn_btn.collidepoint(pos):
                    player_turn = False
                    next_turn_btn_press_down = False
                    main_role.magic = main_role.max_magic
                if quit_btn.collidepoint(pos):
                    running = False
                
                end_x = (len(current_cards)+1)*100
                if GAME_CONTROL and pos[0] >= 100 and pos[0] <= end_x and player_turn:
                    card_index = pos[0] // 100 -1
                    if len(current_cards)<=5:
                        if card_index>=4:
                            card_index = 4
                    else:
                        if card_index>=6:
                            card_index = 6
                    main_card = current_cards[card_index]
                    if (main_role.magic - main_card.cost) >= 0:
                        current_cards.pop(card_index)
                        main_role.magic -= main_card.cost
                        if main_card.index != -1:
                            main_used_cards.append(main_card)
                            usedcardindex = [x.index for x in main_remain_deck].index(main_card.index)
                            main_remain_deck.pop(usedcardindex)
                        
                        match main_card.type:
                            case 'attack'|'fire'|'vampire'|'absorb'|'little_knife':
                                enemy,main_role = card_effect(enemy,main_card,main_role)
                                if enemy.hp <= 0:
                                    enemy.hp = 0
                                    GAME_CONTROL = False
                            case 'defense'|'heal'|'guard':
                                main_role,enemy = card_effect(main_role,main_card,enemy)
                                if main_role.hp > params.init_max_hp:
                                    main_role.hp = params.init_max_hp
                            case 'return':
                                current_cards = random.sample(main_remain_deck,main_role.every_drop)
                            case 'drop':
                                new_drop = random.sample(main_remain_deck,2)
                                current_cards.extend(new_drop)
                            case 'knife':
                                little_knife = Card(-1,'小刀','little_knife',0,2,0,0,'消逝')
                                new_drop = [little_knife,little_knife]
                                current_cards.extend(new_drop)
                            case 'turtle':
                                main_role.buff.append({'turtle':[main_card.lasting,1]})
                                check_person_buff(main_role,enemy,'turtle')
                        logging.info(main_role.name+' 打出 '+main_card.name+' '+str(max(main_card.do_to_other+main_role.damage_buff,main_card.do_for_self+main_role.defense_buff))+' | '
                                +'剩餘卡牌:'+str(len(main_remain_deck))+' | 用過卡牌:'+str(len(main_used_cards))+'\n'
                                +main_role.name+' 狀態: Hp '+str(main_role.hp)+' De '+str(main_role.de)+' de_b '+str(main_role.defense_buff)+' Buff '+str(main_role.buff)+'\n'
                                +enemy.name+' 狀態: Hp '+str(enemy.hp)+' De '+str(enemy.de)+' de_b '+str(enemy.defense_buff)+' Buff '+str(enemy.buff))
        if GAME_CONTROL:
            if player_turn:
                for i in range(len(current_cards)):
                    current_cards[i].draw(win,BLACK,WHITE,i,font_list[0])
                    current_card_index += 1
                pygame.display.update()
                current_card_index = 0
                if test == 0:
                    test = 1
                    logging.info('---------------Player Turn---------------')
            else:
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
                    logging.info('---------------Enemy Turn---------------')
                    test = 0
                
                if enemy.magic > 0:
                    if len(enemy_remain_deck) <= 0:
                        enemy_remain_deck.extend(enemy_used_cards)
                        enemy_used_cards = []
                    card = random.choice(enemy_remain_deck)
                    if (enemy.magic - card.cost) >= 0:
                        use_cards = enemy.use_card(card)
                        if use_cards:
                            enemy.magic -= card.cost
                            enemy_cardindex = [x.index for x in enemy_remain_deck].index(card.index)
                            enemy_remain_deck.pop(enemy_cardindex)
                            enemy_used_cards.append(card)
                            
                            match card.type:
                                case 'attack'|'fire'|'vampire'|'absorb':
                                    main_role,enemy = card_effect(main_role,card,enemy)
                                    if main_role.hp <= 0:
                                        main_role.hp = 0
                                        GAME_CONTROL = False
                                case 'defense'|'heal'|'guard':
                                    enemy,main_role = card_effect(enemy,card,main_role)
                                    if enemy.hp > params.init_max_hp:
                                        enemy.hp = params.init_max_hp
                                case 'return'|'drop':
                                    pass    
                                case 'knife':
                                    little_knife = Card(-1,'小刀','little_knife',0,2,0,0,'0費小刀')
                                    main_role,enemy = card_effect(main_role,little_knife,enemy)
                                    main_role,enemy = card_effect(main_role,little_knife,enemy)
                                case 'turtle':
                                    enemy.buff.append({'turtle':[card.lasting,1]})
                                    check_person_buff(enemy,main_role,'turtle')
                            logging.info(enemy.name+' 打出 '+card.name+' '+str(max(card.do_to_other+enemy.damage_buff,card.do_for_self))+' | '
                                        +'剩餘卡牌:'+str(len(enemy_remain_deck))+' | 用過卡牌:'+str(len(enemy_used_cards))+' \n'
                                        +main_role.name+' 狀態: Hp '+str(main_role.hp)+' De '+str(main_role.de)+' Mp '+str(main_role.magic)+' Buff '+str(main_role.buff)+'\n'
                                        +enemy.name+' 狀態: Hp '+str(enemy.hp)+' De '+str(enemy.de)+' Mp '+str(enemy.magic)+' Buff '+str(enemy.buff))
                        else:
                            logging.info("Enemy not use current card, drop new one.")
                else:
                    player_turn = True
                    enemy.magic = enemy.max_magic
                    check_person_buff(main_role,enemy)

        elif not GAME_CONTROL and enemy.hp == 0:
            logging.warn('********* Next Round *********')
            rounds += 1
            chose_buff,add_value,new_card = choose_normal(win,font_list,rounds)
            if new_card != None:
                new_card.index = len(init_main_card_deck)
                init_main_card_deck.append(new_card)
                
            main_remain_deck = init_main_card_deck.copy()
            main_used_cards = []
            current_cards = random.sample(main_remain_deck,main_role.every_drop)
            
            init_enemy_card_deck = init_card_deck(True)
            if rounds % 3 != 0:
                new_add_enemy_card.append(random.choice(enemy_normal_deck))
            if rounds % 10 != 0:
                new_add_enemy_card.append(random.choice(enemy_high_level_deck))
            enemy_remain_deck = init_enemy_card_deck.copy()
            enemy_remain_deck = enemy_remain_deck+new_add_enemy_card
            enemy_used_cards = []

            enemy = set_enemy(enemy)
            main_role = set_player(main_role,chose_buff,add_value)
            GAME_CONTROL = True

        pygame.display.flip()