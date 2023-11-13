import pygame,sys
import random
import time
import json
import logging
logging.basicConfig(level=logging.INFO)

from src.objects import *
from src.card_process import *
from src.choose import *
from src.params import *
from src.win_page import *

def set_enemy(enemy,log_text_list):
    e_index = random.randint(0,6)
    enemy.enemy_index = e_index
    enemy.name = enemy_name[enemy.enemy_index]
    x = random.randint(0,100)
    if x <= 35:
        enemy.max_hp += params.add_hp
        log_text = enemy.name+' 對於 hp 增強了!'
        logging.info(enemy.name+' 對於 hp 增強了!')
    if x > 40 and x < 65:
        enemy.damage_buff += params.add_value
        log_text = enemy.name+' 對於 damage 增強了!'
        logging.info(enemy.name+' 對於 damage 增強了!')
    if x >= 65:
        enemy.defense_buff += params.add_value
        enemy.heal_buff += params.add_value
        log_text = enemy.name+' 對於 defense & heal 增強了!'
        logging.info(enemy.name+' 對於 defense & heal 增強了!')
    if x > 35 and x < 40:
        enemy.max_magic += params.add_value
        log_text = enemy.name+' 對於 magic 增強了!'
        logging.info(enemy.name+' 對於 magic 增強了!')
    enemy.hp = enemy.max_hp
    enemy.magic = enemy.max_magic
    enemy.buff = []
    log_text_list.append(log_text)
    log_text_list = log_text_list[-params.log_text_len:]
    return enemy,log_text_list

def set_player(main_role,choose,add_value,log_text_list,new_card=None):
    if choose == 'hp':
        main_role.max_hp += add_value
        log_text = main_role.name+' 對於 Hp 增強了!'
        logging.info(main_role.name+' 對於 Hp 增強了!')
    elif choose == 'all':
        y = random.randint(1,4)
        match y:
            case 1:
                main_role.damage_buff += add_value
                choose = 'damage'
            case 2:
                main_role.defense_buff += add_value
                choose = 'defense'
            case 3:
                main_role.heal_buff += add_value
                choose = 'heal'
            case 4:
                log_text = main_role.name+' 對於 magic 增強了!'
                main_role.magic += add_value
                choose = 'magic'
        log_text = main_role.name+' 對於 '+choose+' 屬性增強了!'
        logging.info(main_role.name+' 對於 '+choose+' 屬性增強了!')
    elif choose == '':
        main_role.money += params.add_pass_money
        log_text = main_role.name+'放棄選擇 ， 獲得錢幣 '+str(params.add_pass_money)+' !'
        logging.info(main_role.name+'放棄選擇 ， 獲得錢幣 '+str(params.add_pass_money)+' !')
    else:
        log_text = main_role.name+' 選擇特殊卡 ! -> '+new_card.name
        logging.info(main_role.name+' 選擇特殊卡 ! -> '+new_card.name+'')
    main_role.hp = main_role.max_hp
    main_role.magic = main_role.max_magic
    main_role.buff = []
    log_text_list.append(log_text)
    log_text_list = log_text_list[-params.log_text_len:]
    return main_role,log_text_list

def game_(win,font_list,GAME_CONTROL,main_role,enemy):
    bg = BG(900, 600)
    rounds = 0
    clock = pygame.time.Clock()
    main_role.reset(params.player_value)
    enemy.reset(params.enemy_max_hp,params.enemy_max_de,params.enemy_max_magic)
    
    chose_buff = ''
    with open('source/rankings.json') as f:
        rank_list = json.load(f)
    running = True 
    player_turn,show_history = True,False

    init_enemy_card_deck = init_card_deck(True)
    init_main_card_deck = init_card_deck()

    main_remain_deck = init_main_card_deck.copy()
    main_used_cards = []
    current_cards = random.sample(main_remain_deck,main_role.every_drop)
    
    enemy_remain_deck = init_enemy_card_deck.copy()
    enemy_normal_deck = Special_card.normal_deck.copy()
    enemy_high_level_deck = Special_card.high_level_deck.copy()
    enemy_current_cards = random.sample(enemy_remain_deck,5)
    enemy_used_cards = []
    new_add_enemy_card = []
    
    test,current_card_index,log_text_list = 0,0,[]
    while running:
        win.blit(bg.bg_big, bg.rect)
        Rounds_text = font_list[0].render("關卡: "+str(rounds), True, BLACK)
        win.blit(Rounds_text, (10, 10))

        main_role.draw(win,230,300)
        enemy.draw(win,700,300)

        player_hp_text = font_list[0].render("HP: "+str(main_role.hp), True, RED)
        player_de_text = font_list[0].render("Def: "+str(main_role.de), True, BLUE)
        player_mp_text = font_list[0].render("MP: "+str(main_role.magic), True, BLACK)
        player_money_text = font_list[0].render("Money: "+str(main_role.money), True, YELLOW)
        player_value_text = font_list[0].render("Damage: "+str(main_role.damage_buff)+'\nDef: '
                                        +str(main_role.defense_buff)+'\nHeal: '+str(main_role.heal_buff), True, PURPLE)
        player_name_text = font_list[0].render(main_role.name, True, Coconut_Brown)
        player_job_text = font_list[0].render(job_dict[main_role.main_job], True, Coconut_Brown)
        win.blit(player_hp_text, (200, 10))
        win.blit(player_de_text, (200, 40))
        win.blit(player_mp_text, (200, 70))
        win.blit(player_money_text, (15, 375))
        win.blit(player_value_text, (10, 200))
        win.blit(player_name_text, (200, 100))
        win.blit(player_job_text, (125, 100))
        start_y = 200
        if len(list(main_role.buff)) > 0:
            for i,buff in enumerate(main_role.buff):
                start_y += 50*i
                main_buff_text = font_list[0].render(list(buff.keys())[0], True, Coconut_Brown)
                win.blit(main_buff_text, (300, start_y))

        enemy_hp_text = font_list[0].render("HP: "+str(enemy.hp), True, RED)
        enemy_de_text = font_list[0].render("Def: "+str(enemy.de), True, BLUE)
        enemy_mp_text = font_list[0].render("MP: "+str(enemy.magic), True, BLACK)
        enemy_value_text = font_list[0].render("Damage: "+str(enemy.damage_buff)+'\nDef: '
                                        +str(enemy.defense_buff)+'\nHeal: '+str(enemy.heal_buff), True, PURPLE)
        enemy_name_text = font_list[0].render(enemy.name, True, Coconut_Brown)
        win.blit(enemy_hp_text, (685, 10))
        win.blit(enemy_de_text, (685, 40))
        win.blit(enemy_mp_text, (685, 70))
        win.blit(enemy_value_text, (780, 200))
        win.blit(enemy_name_text, (685, 100))
        start_y_e = 200
        if len(list(enemy.buff)) > 0:
            for i,ebuff in enumerate(enemy.buff):
                start_y_e += 50*i
                enemy_buff_text = font_list[0].render(list(ebuff.keys())[0], True, Coconut_Brown)
                win.blit(enemy_buff_text, (550, start_y_e))

        next_turn_btn = pygame.Rect(775, 425, 110, 30) 
        pygame.draw.rect(win, RED , next_turn_btn)
        btn_text = font_list[0].render("回合結束", True, BLACK)
        win.blit(btn_text, (780, 425))
        quit_btn = pygame.Rect(820, 20, 65, 30) 
        pygame.draw.rect(win, BLACK , quit_btn)
        quit_text = font_list[0].render("Quit", True, WHITE)
        win.blit(quit_text, (825, 20))
        history_btn = pygame.Rect(800, 500, 70, 70) 
        pygame.draw.rect(win, Wisteria , history_btn)
        history_text = font_list[0].render("戰鬥\n歷程", True, BLACK)
        win.blit(history_text, (810, 500))

        if show_history:
            history_surface = pygame.Surface((500,350))
            history_surface.fill(Wisteria)
            for i, text in enumerate(log_text_list):
                log_text = font_list[0].render(text, True, BLACK)
                history_surface.blit(log_text, (30, 10+i*30))
            win.blit(history_surface, (200, 30))
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                write_game_records(rank_list,main_role,rounds)
                logging.warning(main_role.name+' 用 '+ job_dict[main_role.main_jpb] + ' 打到 關卡: '+str(rounds))
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]==1:
                pos = pygame.mouse.get_pos()
                if next_turn_btn.collidepoint(pos):
                    player_turn = False
                if history_btn.collidepoint(pos):
                    if not show_history:
                        show_history = True
                    else:
                        show_history = False
                if quit_btn.collidepoint(pos):
                    write_game_records(rank_list,main_role,rounds)
                    logging.warning(main_role.name+' 用 '+ job_dict[main_role.main_jpb] + ' 打到 關卡: '+str(rounds))
                    running = False
                end_x = (len(current_cards)+1)*100
                if GAME_CONTROL and 100<=pos[0]<= end_x and player_turn and 430<=pos[1]<=540:
                    card_index = pos[0] // 100 -1
                    if len(current_cards)<=5:
                        if card_index>=4:
                            card_index = 4
                    else:
                        if card_index>=(len(current_cards)-1):
                            card_index = len(current_cards)-1
                    main_card = current_cards[card_index]
                    if (main_role.magic - main_card.cost) >= 0:
                        current_cards.pop(card_index)
                        main_role.magic -= main_card.cost
                        if main_card.index != -1:
                            main_used_cards.append(main_card)
                            usedcardindex = [x.index for x in main_remain_deck].index(main_card.index)
                            main_remain_deck.pop(usedcardindex)
                        GAME_CONTROL,current_cards,log_text_list = use_card_effect(main_card,enemy,main_role,GAME_CONTROL,main_remain_deck,main_used_cards,current_cards,log_text_list)
        if GAME_CONTROL:
            if player_turn:
                turn_index = pygame.image.load('source/mainrole_turn.png')
                win.blit(turn_index,(280,150))
                for i in range(len(current_cards)):
                    current_cards[i].draw(win,BLACK,WHITE,i,font_list[0])
                    current_card_index += 1
                pygame.display.update()
                current_card_index = 0
                if test == 0:
                    test = 1
                    log_text = '---------------Player Turn---------------'
                    log_text_list.append(log_text)
                    log_text_list = log_text_list[-params.log_text_len:]
                    logging.info('---------------Player Turn---------------')
                if len(enemy_remain_deck) < 5:
                    enemy_return_cards = random.sample(enemy_used_cards,5-len(enemy_remain_deck))
                    enemy_remain_deck.extend(enemy_return_cards)
                    enemy_current_cards = random.sample(enemy_remain_deck,5)
                    enemy_remain_deck.extend(enemy_used_cards)
                    enemy_used_cards = []
                else:
                    enemy_current_cards = random.sample(enemy_remain_deck,5)
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
                    log_text = '---------------Enemy Turn---------------'
                    log_text_list.append(log_text)
                    log_text_list = log_text_list[-params.log_text_len:]
                    logging.info('---------------Enemy Turn---------------')
                    test = 0
                enemy_turn_index = pygame.image.load('source/enemy_turn.png')
                win.blit(enemy_turn_index,(550,150))
                pygame.display.update()
                if enemy.magic > 0:
                    card = enemy.use_cardAI(enemy_current_cards)
                    if (enemy.magic - card.cost) >= 0:
                        time.sleep(0.5)
                        enemy.magic -= card.cost
                        if card.index != -1:
                            enemy_cardindex = [x.index for x in enemy_remain_deck].index(card.index)
                            enemy_remain_deck.pop(enemy_cardindex)
                            enemy_current_cardindex = [x.index for x in enemy_current_cards].index(card.index)
                            enemy_current_cards.pop(enemy_current_cardindex)
                            enemy_used_cards.append(card)

                        GAME_CONTROL,enemy_current_cards,log_text_list = use_card_effect(card,main_role,enemy,GAME_CONTROL,enemy_remain_deck,enemy_used_cards,enemy_current_cards,log_text_list)
                        
                        card.draw(win,BLACK,WHITE,0,font_list[0],400,100)
                        enemy_use_card_text = font_list[0].render("敵人使用了 "+card.name, True, BLACK)
                        win.blit(enemy_use_card_text, (370, 50))
                        pygame.display.update()
                        time.sleep(0.5)
                    else:
                        logging.info('Enemy drops new card ! ...')
                else:
                    time.sleep(1)
                    player_turn = True
                    enemy.magic = enemy.max_magic
                    main_role.magic = main_role.max_magic
                    check_person_buff(main_role,enemy)
        elif not GAME_CONTROL and enemy.hp == 0:
            mm = random.randint(50,100)
            main_role.money += mm
            logging.info('勝利！獲得 '+str(mm)+' 金錢')
            rounds += 1
            if rounds % 5 == 0 and rounds != 0:
                new_card_deck = random.sample(normal_deck+high_level_deck,k=3)
            else:
                new_card_deck = random.sample(normal_deck,k=3)
            chose_buff,add_value,new_card,main_role = win_surface(win,font_list,rounds,main_role,new_card_deck)
            
            log_text = '********* Next Round *********'
            log_text_list.append(log_text)
            log_text_list = log_text_list[-params.log_text_len:]
            logging.warning('********* Next Round *********')
            if new_card != None:
                new_card.index = len(init_main_card_deck)
                init_main_card_deck.append(new_card)
                
            main_remain_deck = init_main_card_deck.copy()
            main_used_cards = []
            current_cards = random.sample(main_remain_deck,main_role.every_drop)

            init_enemy_card_deck = init_card_deck(True)
            if rounds % 5 == 0 and rounds != 0 and rounds % 10 != 0:
                new_add_enemy_card.append(random.choice(enemy_normal_deck))
            if rounds % 10 == 0 and rounds != 0:
                new_add_enemy_card.append(random.choice(enemy_high_level_deck))
            enemy_remain_deck = init_enemy_card_deck.copy()
            for new_e_card in new_add_enemy_card:
                new_e_card.index = len(init_enemy_card_deck)
                enemy_remain_deck.append(new_e_card)
            enemy_used_cards = []
            enemy_current_cards = random.sample(enemy_remain_deck,5)

            enemy = set_enemy(enemy)
            main_role,log_text_list = set_player(main_role,chose_buff,add_value,log_text_list,new_card)
            GAME_CONTROL = True
        else:
            over_bg = pygame.Rect(200, 225, 500, 150) 
            pygame.draw.rect(win, BLACK , over_bg)
            over_font = pygame.font.Font(params.Font, 150)
            over_text = over_font.render("Game Over", True, RED)
            win.blit(over_text, (225, 230))
            pygame.display.update()
            time.sleep(3)
            running = False
            write_game_records(rank_list,main_role,rounds)
            logging.warning(main_role.name+' 用 '+ job_dict[main_role.main_jpb] + ' 打到 關卡: '+str(rounds))
        pygame.display.flip()
        clock.tick(40)

def write_game_records(rank_list,main_role,rounds):
    if not any(player['name'] == main_role.name for player in rank_list) and not any(player['job'] == main_role.main_job for player in rank_list):
        rank_list.append({"name":main_role.name,"job":params.player_value[main_role.main_job]['name'],"score":str(rounds)})
    else:
        for player in rank_list:
            if player['name'] == main_role.name and player['job'] == main_role.main_job and int(player['score']) < rounds:
                player['score'] = str(rounds)
    rank_list = sorted(rank_list, key=lambda k: k['score'], reverse=True)
    if len(rank_list) > 9:
        rank_list.pop(-1)
    with open('source/rankings.json','w') as f:
        json.dump(rank_list, f)
