import pygame
import random

RED = (255,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
PURPLE = (116,0,179)
YELLOW = (230,230,0)
Coconut_Brown = (77,31,0)
Camel = (161,107,71)
Wisteria = (201,160,220)
Bisque = (255,228,196)
Silver = (192,192,192)
enemy_name = {0:'惡魔',1:'史萊姆-女',2:'史萊姆-男',3:'魷魚監察者',4:'機器人',5:'獵人',6:'猩猩',7:'雷電球',8:'風鳥',9:'惡魔法師',10:'石怪'}
job_dict = {1:'騎士',2:'魔法師',3:'弓箭手',4:'凡人',5:'盜賊',6:'牧師'}
job_image = {1:['source/player/knight.png','source/player/knight2.png','source/player/knight3.png'],
             2:['source/player/magic.png','source/player/magic2.png','source/player/magic3.png'],
             3:['source/player/archer.png','source/player/archer2.png','source/player/archer3.png'],
             4:['source/player/people.png'],
             5:['source/player/thief.png','source/player/thief2.png','source/player/thief3.png'],
             6:['source/player/priest.png','source/player/priest2.png','source/player/priest3.png']}

class Person(pygame.sprite.Sprite):
    def __init__(self, hp, de, magic):
        super().__init__()
        self.max_hp = hp
        self.hp = self.max_hp
        self.de = de
        self.damage_buff = -1
        self.defense_buff = 0
        self.heal_buff = 0
        self.max_magic = magic
        self.magic = self.max_magic
        self.buff = []
    
    def reset(self, hp, de, magic):
        """重設角色屬性，子類可以重寫此方法"""
        self.max_hp = hp
        self.hp = self.max_hp
        self.de = de
        self.damage_buff = -1
        self.defense_buff = 0
        self.heal_buff = 0
        self.max_magic = magic
        self.magic = self.max_magic
        self.buff = []

    def reset_buff(self):
        for i, buff in enumerate(self.buff):
            key = list(buff.keys())[0]
            match key:
                case 'turtle':
                    self.defense_buff-=2
                    self.heal_buff-=2
                    self.damage_buff+=2
                case 'sword':
                    self.damage_buff-=2
                case 'dragon':
                    self.defense_buff-=4
                    self.heal_buff-=4
                    self.damage_buff-=4
        self.buff = []

class Main_role(Person):
    def __init__(self, hp, de, magic, money):
        super().__init__(hp, de, magic)
        self.name = ''
        self.money = money
        self.every_drop = 5
        self.max_card = 9
        self.main_job = 1
        self.role_index = 0

    def draw(self, screen,x,y):
        role = pygame.image.load(job_image[self.main_job][self.role_index]).convert_alpha()
        self.mainrole = pygame.transform.scale(role, (300, 350))
        self.rect = self.mainrole.get_rect(center = (x,y))
        screen.blit(self.mainrole,self.rect)
    
    def reset(self,job_dict):
        job_value = job_dict[self.main_job]
        super().reset(job_value['max_hp'], job_value['max_de'], job_value['magic'])
        
        # 設定 Main_role 特有的屬性
        self.max_de = job_value['max_de']
        self.de = self.max_de
        self.damage_buff = job_value['damage_b']
        self.defense_buff = job_value['defense_b']
        self.heal_buff = job_value['heal_b']
        self.money = job_value['money']
        self.every_drop = 5
        self.max_card = 9
      
class Enemy(Person):
    def __init__(self, hp, de, magic):
        super().__init__(hp, de, magic)
        self.enemy_index = 0
        self.name = enemy_name[self.enemy_index]
        
    def draw(self, screen,x,y):
        # 繪製敵人
        enemy1 = pygame.image.load('source/eney/eney_'+str(self.enemy_index)+'.png').convert_alpha()
        self.enemy1 = pygame.transform.scale(enemy1, (300, 400))
        self.rect = self.enemy1.get_rect(center = (x,y))
        screen.blit(self.enemy1,self.rect)
        
    def use_cardAI(self, enemy_current_cards):
        use_cards = random.choice(enemy_current_cards)
        for i,card in enumerate(enemy_current_cards):
            if card.cost > self.magic:
                continue
            if card.cost == 0:
                return card
            elif self.hp <= self.max_hp/3:
                if self.defense_buff+card.do_for_self > self.heal_buff+card.do_for_self:
                    if card.type == 'defense':
                        return card
                elif i == (len(enemy_current_cards)-1) and card.type == 'heal':
                    return card
                else:
                    if card.type == 'heal':
                        return card
                    elif i == (len(enemy_current_cards)-1) and card.type == 'defense':
                        return card
            elif card.type not in ['attack','defense','heal']:
                return card
        return use_cards
    
    def reset(self, hp,de,magic):
        super().__init__(hp, de, magic)
  
class Card(pygame.sprite.Sprite):
    def __init__(self, index, name, card_type,cost,do_to_other=4, do_for_self=2, Lasting=0, special=None):
        self.index = index
        self.name = name
        self.type = card_type
        self.do_to_other = do_to_other
        self.do_for_self = do_for_self
        self.lasting = Lasting
        self.cost = cost
        self.special = special
      
    def draw(self,win,index,statr_x=70,start_y=500,width=100,height=150):
        next_card = index*100
        card = pygame.image.load('source/card/'+self.type+'.png').convert_alpha()
        self.maincard = pygame.transform.scale(card, (width, height))
        self.rect = self.maincard.get_rect(center = (statr_x+next_card,start_y))
        win.blit(self.maincard,self.rect)