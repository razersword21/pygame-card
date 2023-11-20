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
enemy_name = {0:'惡魔',1:'史萊姆-女',2:'史萊姆-男',3:'魷魚監察者',4:'機器人',5:'獵人',6:'猩猩'}
job_dict = {1:'騎士',2:'魔法師',3:'弓箭手',4:'凡人',5:'盜賊',6:'牧師'}
job_image = {1:'source/player/knight.png',2:'source/player/magic.png',3:'source/player/archer.png',4:'source/player/people.png',5:'source/player/thief.png',6:'source/player/priest.png'}

class Intro_animation(pygame.sprite.Sprite):
  def __init__(self,x,y):
    super(Intro_animation, self).__init__()
    self.background = pygame.image.load('source/info.png').convert_alpha()
    self.bg_big = pygame.transform.scale(self.background, (x, y))
    self.rect = self.bg_big.get_rect(center=(450,300))
  def fadeout_animation(self,win,clock,a):
    while a > 0:
      background=pygame.Surface((win.get_rect().width, win.get_rect().height))
      background.fill(BLACK)
      self.background.set_alpha(a)
      self.bg_big = pygame.transform.scale(self.background, (300,300))
      win.blit(background, background.get_rect())
      win.blit(self.bg_big, self.rect)
      pygame.display.update()
      clock.tick(20)
      a -= 5

class Intro(pygame.sprite.Sprite):
  def __init__(self,x,y):
    super(Intro, self).__init__()
    background = pygame.image.load('source/start.png').convert_alpha()
    self.bg_big = pygame.transform.scale(background, (x, y))
    self.rect = self.bg_big.get_rect(left=0, top=0)

class BG(pygame.sprite.Sprite):
  def __init__(self,x,y):
    super(BG, self).__init__()
    background = pygame.image.load('source/bg.png').convert_alpha()
    self.bg_big = pygame.transform.scale(background, (x, y))
    self.rect = self.bg_big.get_rect(left=0, top=0)

class chose_BG(pygame.sprite.Sprite):
  def __init__(self,x,y):
    super(chose_BG, self).__init__()
    background = pygame.image.load('source/start2.jpg').convert_alpha()
    self.bg_big = pygame.transform.scale(background, (x, y))
    self.rect = self.bg_big.get_rect(left=0, top=0)

class shop_BG(pygame.sprite.Sprite):
  def __init__(self,x,y):
    super(shop_BG, self).__init__()
    background = pygame.image.load('source/shop.png').convert_alpha()
    self.bg_big = pygame.transform.scale(background, (x, y))
    self.rect = self.bg_big.get_rect(left=0, top=0)

class job_BG(pygame.sprite.Sprite):
  def __init__(self,x,y):
    super(job_BG, self).__init__()
    background = pygame.image.load('source/job.png').convert_alpha()
    self.bg_big = pygame.transform.scale(background, (x, y))
    self.rect = self.bg_big.get_rect(left=0, top=0)

class Main_role(pygame.sprite.Sprite):
  def __init__(self,hp,de,magic,money):
    self.name = ''
    self.max_hp = hp
    self.hp = self.max_hp
    self.max_de = de
    self.de = self.max_de
    self.damage_buff = 0
    self.defense_buff = 0
    self.heal_buff = 0
    self.max_magic = magic
    self.magic = self.max_magic
    self.money = money
    self.every_drop = 5
    self.max_card = 9
    self.buff = []
    self.main_job = 1

  def draw(self, screen,x,y):
    role = pygame.image.load(job_image[self.main_job]).convert_alpha()
    self.mainrole = pygame.transform.scale(role, (300, 350))
    self.rect = self.mainrole.get_rect(center = (x,y))
    screen.blit(self.mainrole,self.rect)
  
  def reset(self,job_dict):
    job_value = job_dict[self.main_job]
    self.max_hp = job_value['max_hp']
    self.hp = self.max_hp
    self.max_de = job_value['max_de']
    self.de = self.max_de
    self.damage_buff = job_value['damage_b']
    self.defense_buff = job_value['defense_b']
    self.heal_buff = job_value['heal_b']
    self.max_magic = job_value['magic']
    self.magic = self.max_magic
    self.money = job_value['money']
    self.every_drop = 5
    self.max_card = 9
    self.buff = []
      
class Enemy(pygame.sprite.Sprite):

  def __init__(self, hp,de,magic):
    self.max_hp = hp
    self.hp = self.max_hp
    self.de = de
    self.damage_buff = -1
    self.defense_buff = 0
    self.heal_buff = 0
    self.max_magic = magic
    self.magic = self.max_magic
    self.buff = []
    self.enemy_index = 0
    self.name = enemy_name[self.enemy_index]
    
  def draw(self, screen,x,y):
    # 繪製敵人
    enemy1 = pygame.image.load('source/eney/eney_'+str(self.enemy_index)+'.png').convert_alpha()
    self.enemy1 = pygame.transform.scale(enemy1, (300, 400))
    self.rect = self.enemy1.get_rect(center = (x,y))
    screen.blit(self.enemy1,self.rect)
    
  def use_cardAI(self,enemy_current_cards):
    use_cards = random.choice(enemy_current_cards)
    for card in enemy_current_cards:
      if card.cost == 0:
        return card
      elif self.hp <= self.max_hp/3:
        if self.defense_buff+card.do_for_self > self.heal_buff+card.do_for_self:
          if card.type == 'defense':
              return card
        else:
          if card.type == 'heal':
            return card
      elif card.type not in ['attack','defense','heal']:
        return card
    return use_cards
  
  def reset(self, hp,de,magic):
    self.max_hp = hp
    self.hp = self.max_hp
    self.de = de
    self.damage_buff = -1
    self.defense_buff = 0
    self.heal_buff = 0
    self.max_magic = magic
    self.magic = self.max_magic
    self.buff = []
  
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