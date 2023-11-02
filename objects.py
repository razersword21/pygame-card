import pygame

RED = (255,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
PURPLE = (116,0,179)
YELLOW = (255,255,0)

class Intro(pygame.sprite.Sprite):
  def __init__(self,x,y):
    super(Intro, self).__init__()
    background = pygame.image.load('draw_source/start.png').convert_alpha()
    self.bg_big = pygame.transform.scale(background, (x, y))
    self.rect = self.bg_big.get_rect(left=0, top=0)

class BG(pygame.sprite.Sprite):
  def __init__(self,x,y):
    super(BG, self).__init__()
    background = pygame.image.load('draw_source/bg.png').convert_alpha()
    self.bg_big = pygame.transform.scale(background, (x, y))
    self.rect = self.bg_big.get_rect(left=0, top=0)

class Main_role(pygame.sprite.Sprite):
  def __init__(self, hp,de,magic,money):
    self.name = '玩家'
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

  def draw(self, screen,x,y):
    role = pygame.image.load('draw_source/eney2.png').convert_alpha()
    self.mainrole = pygame.transform.scale(role, (400, 400))
    self.rect = self.mainrole.get_rect(center = (x,y))
    screen.blit(self.mainrole,self.rect)
      
class Enemy(pygame.sprite.Sprite):

  def __init__(self, hp,de,magic):
    self.name = '敵人'
    self.max_hp = hp
    self.hp = self.max_hp
    self.de = de
    self.damage_buff = 0
    self.defense_buff = 0
    self.heal_buff = 0
    self.max_magic = magic
    self.magic = self.max_magic
    self.buff = []
    
  def draw(self, screen,x,y, index):
    # 繪製敵人
    enemy1 = pygame.image.load('draw_source/eney1.png').convert_alpha()
    self.enemy1 = pygame.transform.scale(enemy1, (410, 410))
    self.rect = self.enemy1.get_rect(center = (x,y))
    screen.blit(self.enemy1,self.rect)
    
  def use_card(self,card):
    use_cards = True
    if self.hp <= self.max_hp/2:
      if card.type == 'defense' or card.type == 'heal':
        use_cards = True
    elif card.type not in ['attack','defense','heal']:
      use_cards = True
    else:
      use_cards = True
    return use_cards
  
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
      
    def draw(self,win,bgcolor,color,index,FONT,statr_x=100):
        next_card = index*100
        pygame.draw.rect(win,bgcolor,(statr_x+next_card, 400, 110, 150))
        pygame.draw.rect(win,color,(statr_x+next_card+5, 400+5, 100, 140)) 
        card_name_text = FONT.render(str(self.name), True, BLACK)
        win.blit(card_name_text,(statr_x+20+next_card+5,430+5))
        card_cost_text = FONT.render('Cost '+str(self.cost), True, BLACK)
        win.blit(card_cost_text,(statr_x+20+next_card+5,460+5))
        match self.type:
          case 'attack':
            card_number_text = FONT.render(str(self.do_to_other), True, RED)
            win.blit(card_number_text,(statr_x+45+next_card+5,490+5))
          case 'defense'|'heal':
            card_number_text = FONT.render(str(self.do_for_self), True, GREEN)
            win.blit(card_number_text,(statr_x+45+next_card+5,490+5))
          case 'fire':
            card_number_text = FONT.render(str(self.do_to_other), True, RED)
            win.blit(card_number_text,(statr_x+45+next_card+5,490+5))
            card_last_text = FONT.render('Last: '+str(self.lasting), True, BLACK)
            win.blit(card_last_text,(statr_x+20+next_card+5,530+5))
          case 'vampire'|'absorb':
            card_number_text = FONT.render('吸: '+str(self.do_to_other), True, PURPLE)
            win.blit(card_number_text,(statr_x+10+next_card+5,490+5))
            card_last_text = FONT.render('Get: '+str(self.do_to_other), True, BLUE)
            win.blit(card_last_text,(statr_x+10+next_card+5,510+5))
          case 'little_knife'|'knife':
            card_number_text = FONT.render(self.special, True, RED)
            win.blit(card_number_text,(statr_x+10+next_card+5,480+5))
          case 'turtle':
            card_last_text = FONT.render('Last: '+str(self.lasting), True, BLACK)
            win.blit(card_last_text,(statr_x+20+next_card+5,490+5))

# class Pet(pygame.sprite.Sprite):
#   def __init__(self,cost,hp,de,damage,shield,heal):
#     self.name = 'Pet'
#     self.image = pygame.image.load('draw_source/bg.png').convert_alpha()
#     self.rect = self.image.get_rect()
#     self.damage = damage
#     self.cost = cost
#     self.max_hp = hp
#     self.hp = self.max_hp
#     self.max_de = de
#     self.de = self.max_de
#     self.shield = shield
#     self.heal = heal
  
#   def attack_enemy(self,person):
#     if person.de > 0:
#         person.de -= self.damage
#     if person.de < 0:
#         person.hp -= person.de
#         person.de = 0
#     else:
#         person.hp -= self.damage
#   def shield_main(self,person):
#         person.de += self.de
#   def heal_main(self,person):
#         person.hp += self.heal
#         if person.hp > person.max_hp:
#            person.hp = person.max_hp