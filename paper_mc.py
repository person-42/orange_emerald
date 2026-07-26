import datetime
import random

import pygame

pygame.init()
class NoBlockError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
all_blocks = [[], [], [], [], [], []]  #-+-+-+ negative chunk,positive chunk
pygame.display.set_caption("PAPER MINECRAFT")
player_list = {}
players_in_chunks = {}
players_in_dimension = {}
controlled_player_name = "player1"
sprites = pygame.sprite.Group()
dropped_items=[]
SCREEN_X=screen.get_size()[0]
SCREEN_Y=screen.get_size()[1]
SPACE_SIZE=SCREEN_X/9.6
STRIP_SIZE=SCREEN_Y/7.2
BLOCK_WIDTH=(SCREEN_X-SPACE_SIZE)/57
BLOCK_HEIGHT=(SCREEN_Y-STRIP_SIZE)/31
DROP_SIZE=BLOCK_WIDTH / 2 + BLOCK_WIDTH / 7
HEART_SIZE = BLOCK_WIDTH * 1.5
FALL_SPEED = BLOCK_WIDTH / 3
PLAYER_WIDTH,PLAYER_HEIGHT= ((BLOCK_WIDTH / 2) + (BLOCK_WIDTH / 15)) * 2, BLOCK_WIDTH * 2.5
def calculate_leave_drops():
    rand = random.randint(1, 20)
    if rand == 1:
        return "apple"
    elif rand <4:
        return "sapling"
    else:
        return ""
block_image_list={"iron ore": "images/iron_ore.png", "coal ore": "images/coal_ore.png",
                      "copper ore": "images/copper_ore.png", "diamond ore": "images/diamond_ore.png",
                      "gold ore": "images/gold_ore.png", "emerald ore": "images/emerald_ore.png",
                      "lapis ore": "images/lapis_ore.png", "redstone ore": "images/redstone_ore.png",
                      "nether gold ore": "images/nether_gold_ore.png",
                      "quartz ore": "images/quartz_ore.png"}
block_color_list={"netherack": "#842020", "sand": "#ccb46d", "air": "#0dcaf0", "dirt": "#653208", "leaves": "#486317",
                "stone": "#585B5C", "planks": "lightsalmon",
                "bedrock": "#22202c", "end stone": "#C4BF4F", "grass": "green", "water": "blue",
                "snow": "#f0e9d2", "cactus": "#03550c", "log": "#5b1a17", "lava": "#b54d05", "cobblestone": "dimgray"}
def remove_minus_and_add_1(thing_):
    if str(thing_)[0]=="-":
        thing_*=-1
        thing_+=1
    return thing_
def forest(level, x_pos=0, chunk_list=1, chunk_number=0):
    if level < 12:
        ere = "air"
    elif level == 12:
        randomizer = random.randint(1, 9)
        if randomizer == 2:
            try:
                ere = "air"
                if x_pos != 1:
                    all_blocks[chunk_list][chunk_number][(31 * x_pos - 1) + level - 30].change_type("log")
                    all_blocks[chunk_list][chunk_number][(31 * x_pos - 1) + level - 31].change_type("log")
                    all_blocks[chunk_list][chunk_number][(31 * x_pos - 1) + level - 32].change_type("log")
                    all_blocks[chunk_list][chunk_number][(31 * x_pos - 1) + level - 33].change_type("leaves")
                    all_blocks[chunk_list][chunk_number][(31 * x_pos - 1) + level - 34].change_type("leaves")
                    all_blocks[chunk_list][chunk_number][(31 * x_pos - 1) + level - 64].change_type("leaves")
                    all_blocks[chunk_list][chunk_number][(31 * x_pos - 1) + level - 65].change_type("leaves")
                    all_blocks[chunk_list][chunk_number][(31 * x_pos - 1) + level - 2].change_type("leaves")
                    all_blocks[chunk_list][chunk_number][(31 * x_pos - 1) + level - 3].change_type("leaves")
                    all_blocks[chunk_list][chunk_number][(31 * x_pos - 1) + level - 35].change_type("leaves")
            except IndexError:
                ere = "air"
        else:
            ere = "air"
    elif level == 13:
        ere = "grass"
    elif level < 17:
        ere = "dirt"
        if level == 14:
            randomizer = random.randint(1, 60)
            if randomizer == 1:
                try:
                    if x_pos != 1:
                        ere = "water"
                        all_blocks[chunk_list][chunk_number][(31 * x_pos - 1) + level].change_type("water")
                        all_blocks[chunk_list][chunk_number][(31 * x_pos - 31) + level].change_type("water")
                        all_blocks[chunk_list][chunk_number][(31 * x_pos - 32) + level].change_type("water")
                        all_blocks[chunk_list][chunk_number][(31 * x_pos - 62) + level].change_type("water")
                        all_blocks[chunk_list][chunk_number][(31 * x_pos - 63) + level].change_type("water")
                    else:
                        ere = "dirt"
                except IndexError:
                    ere = "dirt"
    elif level < 30:
        randomizer = random.randint(0, 600)
        if randomizer < 2:
            ere = "emerald ore"
        elif randomizer < 5:
            ere = "diamond ore"
        elif randomizer < 12:
            ere = "iron ore"
        elif randomizer < 18:
            ere = "gold ore"
        elif randomizer < 24:
            ere = "coal ore"
        elif randomizer < 31:
            ere = "copper ore"
        elif randomizer < 36:
            ere = "lapis ore"
        elif randomizer < 40:
            ere = "redstone ore"
        elif randomizer < 44:
            ere = "lava"
        else:
            ere = "stone"
    else:
        ere = "bedrock"
    return ere
def snowy_forest(level, x_pos=0, chunk_list=1, chunk_number=0):
    if level < 12:
        ere = "air"
    elif level == 12:
        randomizer = random.randint(1, 7)
        if randomizer == 5:
            try:
                ere = "air"
                if x_pos > 1:
                    all_blocks[chunk_list][chunk_number][(31 * x_pos - 1) + level - 30].change_type("log")
                    all_blocks[chunk_list][chunk_number][(31 * x_pos - 1) + level - 31].change_type("log")
                    all_blocks[chunk_list][chunk_number][(31 * x_pos - 1) + level - 32].change_type("log")
                    all_blocks[chunk_list][chunk_number][(31 * x_pos - 1) + level - 33].change_type("leaves")
                    all_blocks[chunk_list][chunk_number][(31 * x_pos - 1) + level - 34].change_type("leaves")
                    all_blocks[chunk_list][chunk_number][(31 * x_pos - 1) + level - 64].change_type("leaves")
                    all_blocks[chunk_list][chunk_number][(31 * x_pos - 1) + level - 65].change_type("leaves")
                    all_blocks[chunk_list][chunk_number][(31 * x_pos - 1) + level - 2].change_type("leaves")
                    all_blocks[chunk_list][chunk_number][(31 * x_pos - 1) + level - 3].change_type("leaves")
                    all_blocks[chunk_list][chunk_number][(31 * x_pos - 1) + level - 35].change_type("leaves")
            except IndexError:
                ere = "air"
        else:
            ere = "air"
    elif level == 13:
        ere = "snow"
    elif level < 17:
        ere = "dirt"
        if level == 14:
            randomizer = random.randint(2, 60)
            if randomizer == 1:
                try:
                    if x_pos != 1:
                        ere = "water"
                        all_blocks[chunk_list][chunk_number][(31 * x_pos - 1) + level].change_type("water")
                        all_blocks[chunk_list][chunk_number][(31 * x_pos - 31) + level].change_type("water")
                        all_blocks[chunk_list][chunk_number][(31 * x_pos - 32) + level].change_type("water")
                        all_blocks[chunk_list][chunk_number][(31 * x_pos - 62) + level].change_type("water")
                        all_blocks[chunk_list][chunk_number][(31 * x_pos - 63) + level].change_type("water")
                    else:
                        ere = "dirt"
                except IndexError:
                    ere = "dirt"
    elif level < 30:
        randomizer = random.randint(0, 600)
        if randomizer < 2:
            ere = "emerald ore"
        elif randomizer < 5:
            ere = "diamond ore"
        elif randomizer < 12:
            ere = "iron ore"
        elif randomizer < 18:
            ere = "gold ore"
        elif randomizer < 24:
            ere = "coal ore"
        elif randomizer < 31:
            ere = "copper ore"
        elif randomizer < 36:
            ere = "lapis ore"
        elif randomizer < 40:
            ere = "redstone ore"
        elif randomizer < 44:
            ere = "lava"
        else:
            ere = "stone"
    else:
        ere = "bedrock"
    return ere
def desert(level, x_pos=0, chunk_list=1, chunk_number=0):
    if level == 30:
        ere = "bedrock"
    elif level < 13:
        ere = "air"
    elif level == 13:
        randomizer = random.randint(1, 9)
        if randomizer == 2:
            ere = "cactus"
            all_blocks[chunk_list][chunk_number][(31 * x_pos - 1) + level].change_type("cactus")
        else:
            ere = "air"
    elif level < 17:
        ere = "sand"
        if level == 15:
            randomizer = random.randint(1, 40)
            if randomizer == 1:
                try:
                    if x_pos != 1:
                        ere = "water"
                        all_blocks[chunk_list][chunk_number][(31 * x_pos - 1) + level].change_type("water")
                        all_blocks[chunk_list][chunk_number][(31 * x_pos - 31) + level].change_type("water")
                        all_blocks[chunk_list][chunk_number][(31 * x_pos - 32) + level].change_type("water")
                        all_blocks[chunk_list][chunk_number][(31 * x_pos - 62) + level].change_type("water")
                        all_blocks[chunk_list][chunk_number][(31 * x_pos - 63) + level].change_type("water")
                    else:
                        ere = "sand"
                except IndexError:
                    ere = "sand"
    else:
        randomizer = random.randint(0, 600)
        if randomizer < 2:
            ere = "emerald ore"
        elif randomizer < 5:
            ere = "diamond ore"
        elif randomizer < 12:
            ere = "iron ore"
        elif randomizer < 18:
            ere = "gold ore"
        elif randomizer < 24:
            ere = "coal ore"
        elif randomizer < 31:
            ere = "copper ore"
        elif randomizer < 36:
            ere = "lapis ore"
        elif randomizer < 40:
            ere = "redstone ore"
        elif randomizer < 44:
            ere = "lava"
        else:
            ere = "stone"
    return ere
class chunk:
    def __init__(self, number, pos_neg="+", dimension="overworld", biome="forest"):
        super().__init__()
        global all_blocks
        if dimension == "end":
            pass
        elif dimension == "nether":
            pass
        else:
            if pos_neg == "-":
                all_blocks[0].append([])
                for l in range(57):  #x position
                    for i in range(31):
                        if biome == "forest":
                            blockya = forest(i, l, 0, number)
                        if biome == "desert":
                            blockya = desert(i, l, 0, number)
                        if biome=="snowy forest":
                            blockya = snowy_forest(i, l, 0, number)
                        all_blocks[0][number].append(block(x__ =int(l * BLOCK_WIDTH + SPACE_SIZE), y__= int(i * BLOCK_WIDTH), type_=blockya))
            else:
                all_blocks[1].append([])
                for l in range(57):
                    for i in range(31):
                        if biome == "forest":
                            tyry = forest(i, l, 1, number)
                        if biome == "desert":
                            tyry = desert(i, l, 1, number)
                        if biome=="snowy forest":
                            tyry = snowy_forest(i, l, 0, number)
                        all_blocks[1][number].append(block(x__=int(l * BLOCK_WIDTH + SPACE_SIZE), y__=int(i * BLOCK_WIDTH), type_=tyry))

class block(pygame.sprite.Sprite):
    def __init__(self, type_="grass", x__=0, y__=0):
        super().__init__()
        self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT), pygame.SRCALPHA)
        global block_color_list
        global block_image_list
        rtye = block_color_list
        image_rtrt = block_image_list
        self.image_list = image_rtrt
        drop_list = {"log": "log", "stone": "cobblestone",
                     "grass": "dirt", "coal ore": "coal",
                     "netherack": "netherack", "sand": "sand", "dirt": "dirt",}
        unbreakable_blocks = ["bedrock", "air", "water", "lava"]
        self.unbreakable_blocks = unbreakable_blocks
        self.rtye = rtye
        self.image_list = image_rtrt
        drop_list = {"log": "log", "stone": "cobblestone",
                     "grass": "dirt", "coal ore": "coal",
                     "netherack": "netherack", "sand": "sand", "dirt": "dirt",
                     "leaves": f"{calculate_leave_drops()}", "snow": "snowball",
                     "cactus": "cactus", "iron ore": "raw iron", "copper ore": "raw copper", "diamond ore": "diamond",
                     "gold ore": "raw gold",
                     "emerald ore": "emerald", "lapis ore": "lapis",
                     "redstone ore": "redstone", "nether gold ore": "gold nugget", "quartz ore": "nether quartz",
                     "cobblestone": "cobblestone", "end stone": "end stone"}
        self.drop_list = drop_list
        drop_amount = {"copper ore": random.randint(1, 3),
                       "lapis ore": random.randint(1, 8), "redstone ore": random.randint(1, 5),
                       "snow": random.randint(1, 3),
                       "nether gold ore": random.randint(2, 6),
                       "quartz ore": random.randint(1, 3)}
        self.health = 100
        tool_list = {"log": "axe", "grass": "shovel", "dirt": "shovel", "stone": "pickaxe", "leaves": "hoe",
                     "netherack": "pickaxe", "snow": "shovel", "cactus": "axe", "cobblestone": "pickaxe",
                     "planks": "axe",
                     "sand": "shovel", "end stone": "pickaxe", "iron ore": "pickaxe",
                     "coal ore": "pickaxe", "copper ore": "pickaxe",
                     "diamond ore": "pickaxe", "gold ore": "pickaxe", "emerald ore": "pickaxe",
                     "redstone ore": "pickaxe",
                     "lapis ore": "pickaxe", "nether gold ore": "pickaxe", "quartz ore": "pickaxe"}
        self.tool_list = tool_list
        hardness_list = {"log": 25, "netherack": 35}
        self.hardness_list = hardness_list
        # 0=fist,1=wood/gold,2=stone/copper,3=iron,4=diamond/netherite
        minimum_material = {"log": 0, "stone": 1, "plank": 0, "coal ore": 1, "copper ore": 1, "iron ore": 2,
                            "leaves": 0, "cactus": 0,
                            "gold ore": 3, "snow": 1}
        self.minimum_material = minimum_material
        self.drop_amount = drop_amount
        self.rect = self.image.get_rect(center=(30 // 2, 30 // 2))
        self._type_ = type_
        self.rect.y = y__
        self.block_colors = block_color_list
        self.rect.x = x__
        self.change_type(type_)
    def go(self, x, y):
        self.rect.y = y
        self.rect.x = x
    def block_colors(self):
        return self.rtye
    def block_images(self):
        return self.image_list
    def is_air(self):
        if self._type_ == "air":
            return True
        else:
            return False
    def give_type(self):
        return self._type_
    def change_type(self, new_type):
        self._type_ = new_type
        if new_type in self.rtye :
            self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_WIDTH), pygame.SRCALPHA)
            self.image.fill(self.block_colors[new_type])
        elif new_type in self.image_list :
            self.image=pygame.image.load(block_image_list[new_type])
            self.image=pygame.transform.scale(self.image, (BLOCK_WIDTH, BLOCK_WIDTH))
        else:
            raise NoBlockError("Given type is not in any dictionary. No type or color mentioned")
    def get_size(self):
        return self.rect.size
    def weaken(self, material, tool_type,player_name):
        if self._type_ not in self.unbreakable_blocks:
            if tool_type == self.tool_list[self._type_]:
                self.health -= self.hardness_list[self._type_]
                self.health -= material * 5
            else:
                self.health -= material * 3 + 5
        if self.health <=0:
            self.broke(player_name,material,tool_type)
    def heal(self):
        if self.health < 95:
            self.health += 5
        else:
            self.health = 100
    def broke(self, player_name, material, tool):
        global player_list
        self.change_type("air")
        if (self.minimum_material[self._type_] == 0 or
                (self.minimum_material[self._type_] >= material and self.tool_list[self._type_] == tool)):
            if self._type_ not in self.unbreakable_blocks:
                if not self._type_ in self.drop_amount:
                    player_list[player_name].items[self.drop_list[self._type_]] += 1
                else:
                    player_list[player_name].items[self.drop_list[self._type_]] += self.drop_amount[self._type_]
class player(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.image = pygame.image.load("../orange_emerald/images/player_character.png")
        self.image=pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.items = {"logs": 0, "planks": 0, "stone": 0, "grass": 0, "dirt": 0,
                      "cobblestone": 0, "emerald": 0,
                      "diamond": 0, "redstone": 0, "cactus": 0}
        self.health = 1000
        self.gold_health = 0
        self.speed = 5
        self.fall_speed = FALL_SPEED
        self.fall_velocity = 0
        self.name = name
        self.rect = self.image.get_rect(center=(PLAYER_WIDTH// 2, PLAYER_HEIGHT // 2))
        self.go(500, 20)#
    def go(self, x, y):
        self.rect.x = x
        self.rect.y = y
    def goto(self, x, y):
        self.go(x, y)
    def is_inventory_full(self):
        pass
    def fall(self, multiplier=1):
        self.rect.y += self.fall_speed * multiplier
        self.fall_velocity += self.fall_speed * multiplier
    def left(self, multiplier=1):
        self.rect.x -= self.speed * multiplier
    def right(self, multiplier=1):
        self.rect.x += self.speed * multiplier
    def get_hearts(self):
        return self.health
    def get_gold_hearts(self):
        return self.gold_health
    def get_name(self):
        return self.name
    def amount_of_item(self, item):
        return self.items[item]
    def size(self):
        return self.rect.size
    def jump(self):
        self.rect.y -= self.speed * 10
    def heal(self,hp=1):
        if self.health < 1000-hp:
            self.health += hp
        else:
            self.health=1000
    def damage(self,hp=1):
        if self.gold_health > hp:
            self.gold_health-=hp
        elif self.gold_health==0:
            self.health-=hp
        else:
            self.gold_health-=hp
        self.update_health()
    def update_health(self):
        if self.gold_health<0:
            print(self.health+self.gold_health)
            self.health+=self.gold_health
            self.gold_health=0
    def gold_heart(self,hp):
        if self.get_gold_hearts() < hp:
            self.gold_health=hp
class drop(pygame.sprite.Sprite):
    def __init__(self, x, y,type_,chunk_,dimension_):
        super().__init__()
        global block_image_list
        global block_color_list
        self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
        self.rect=self.image.get_rect(center=(30 // 2, 30 // 2))
        self.block_image_list=block_image_list
        self.block_color_list=block_color_list
        self.goto(x+random.randint(-100,100)/5, y)
        self.type_=type_
        self.timer = (datetime.datetime.now().minute + 5)%60
        self.chunk_=chunk_
        self.dimension_=dimension_
        self.change_image(new_type=type_)
    def change_image(self,new_type):
        self.type_ = new_type
        if new_type in self.block_color_list:
            self.image = pygame.Surface((DROP_SIZE, DROP_SIZE), pygame.SRCALPHA)
            self.image.fill(self.block_color_list[new_type])
        elif new_type in self.block_image_list:
            self.image = pygame.image.load(block_image_list[new_type])
            self.image = pygame.transform.scale(self.image, (DROP_SIZE, DROP_SIZE))
        else:
            raise NoBlockError("Given type is not in any dictionary. No image or color mentioned")
    def x(self):
        return self.rect.x
    def fall(self):
        self.rect.y += 5
    def y(self):
        return self.rect.y
    def goto(self, x, y):
        self.rect.x=x
        self.rect.y=y
    def is_in_chunk(self,_chunk_):
        if self.chunk_ == _chunk_:
            return True
        else:
            return False
    def is_in_dimension(self,dimension___):
        if self.dimension_ == dimension___:
            return True
        else:
            return False
    def should_despawn(self):
        if self.timer==datetime.datetime.now().minute:
            return True
        else:
            return False
def add_player(name):
    players_in_chunks[name]=0
    players_in_dimension[name]="overworld"
    player_list[name]=player(name)
add_player("player1")
add_player("player2")
players=pygame.sprite.Group()
def drop_item(x,y,type_,chunk_,dimension):
    dropped_items.append(drop(x=x, y=y,type_=type_,chunk_=chunk_,dimension_=dimension))
# Phyton special words
#import as while for return is if else elif in not True False def class try except finally raise pass global async break lambda  assert del None or
def is_collide(x1, x2, y1, y2, x_reach=PLAYER_WIDTH//2, y_reach=PLAYER_HEIGHT):
    if -x_reach <= x1 - x2 <= x_reach:
        if -y_reach <= y1 - y2 <= y_reach:
            return True
        else:
            return False
    else:
        return False
overworld_biomes = ["forest",'desert',"snowy forest"]
nether_biomes = []
end_biomes = []
def add_chunks():
        if len(all_blocks[position]) < 2001:
            random_overworld_chunk(len(all_blocks[1]))
            random_overworld_chunk(len(all_blocks[0])*-1-1)
            random_nether_chunk(len(all_blocks[3]))
            random_nether_chunk(len(all_blocks[2])*-1-1)
            random_end_chunk(len(all_blocks[5]))
            random_end_chunk(len(all_blocks[4])*-1-1)
def random_overworld_chunk(position__):
    if str(position__)[0] == "-":
        p_n = "-"
    else:
        p_n = "+"
    bi = random.choice(overworld_biomes)
    remove_minus_and_add_1(position__)
    chunk(number=position__, pos_neg=p_n, dimension="overworld", biome=bi)
def random_nether_chunk(pos):
    pass
def random_end_chunk(pos):
    pass
# BAD_CHARACTERS LOL
#!£$?؟
class hotbar(pygame.sprite.Sprite):
    def __init__(self,number):
        super().__init__()

class heart(pygame.sprite.Sprite):
    def __init__(self,player__,number):
        super().__init__()
        global player_list
        self.image=pygame.image.load("../orange_emerald/images/heart.png")
        self.rect=self.image.get_rect()
        self.image=pygame.transform.scale(self.image, ( HEART_SIZE, HEART_SIZE))
        self.player__ = player__
        self.number=number
        self.hearts = 0
        self.hp=player_list[self.player__].get_hearts()
        self.update_health()
        self.number=number
        self.goto(y=screen.get_size()[1] - BLOCK_WIDTH * 2.6, x=SPACE_SIZE / 1.4 + ((HEART_SIZE + (HEART_SIZE // 10)) * number))
    def empty_heart(self):
        self.image=pygame.image.load("../orange_emerald/images/empty_heart.png")
        self.image=pygame.transform.scale(self.image, ( HEART_SIZE, HEART_SIZE))
    def half_heart(self):
        self.image=pygame.image.load("../orange_emerald/images/half_heart.png")
        self.image=pygame.transform.scale(self.image, ( HEART_SIZE, HEART_SIZE))
    def full_heart(self):
        self.image=pygame.image.load("../orange_emerald/images/heart.png")
        self.image=pygame.transform.scale(self.image, ( HEART_SIZE, HEART_SIZE))
    def goto(self,x,y):
        self.rect.x=x
        self.rect.y=y
    def update_health(self):
        self.hp=player_list[self.player__].get_hearts()
        player_list[self.player__].update_health()
        if 0 < self.hp <= 50 :
            self.hearts=1
        elif 50 < self.hp <= 100 :
            self.hearts=2
        elif 100 < self.hp <= 150 :
            self.hearts=3
        elif 150 < self.hp <= 200 :
            self.hearts=4
        elif 200 < self.hp <= 250:
            self.hearts = 5
        elif 250 < self.hp <= 300:
            self.hearts = 6
        elif 300 < self.hp <= 350:
            self.hearts = 7
        elif 350 < self.hp <= 400:
            self.hearts = 8
        elif 400 < self.hp <= 450:
            self.hearts = 9
        elif 450 < self.hp <= 500:
            self.hearts = 10
        elif 500 < self.hp <= 550 :
            self.hearts=11
        elif 550 < self.hp <= 600:
            self.hearts = 12
        elif 600 < self.hp <= 650:
            self.hearts = 13
        elif 650 < self.hp <= 700:
            self.hearts = 14
        elif 700 < self.hp <= 750:
            self.hearts = 15
        elif 750 < self.hp <= 800:
            self.hearts = 16
        elif 800 < self.hp <= 850:
            self.hearts = 17
        elif 850 < self.hp <= 900:
            self.hearts = 18
        elif 900 < self.hp <= 950:
            self.hearts = 19
        elif 950 < self.hp <= 1000:
            self.hearts = 20
        if self.hearts>=self.number*2:
            self.full_heart()
        elif self.hearts +1 ==self.number*2:
            self.half_heart()
        else:
            self.empty_heart()
class gold_heart(pygame.sprite.Sprite):
    def __init__(self,player__,number):
        super().__init__()
        global player_list
        self.image=pygame.image.load("../orange_emerald/images/gold_heart.png")
        self.rect=self.image.get_rect()
        self.image=pygame.transform.scale(self.image, ( HEART_SIZE, HEART_SIZE))
        self.player__ = player__
        self.number=number
        self.hearts = 0
        self.hp=player_list[self.player__].get_gold_hearts()
        self.update_health()
        self.number=int(number)
        self.goto(y=screen.get_size()[1] - BLOCK_WIDTH * 4.1, x=SPACE_SIZE / 1.4 + ((HEART_SIZE + (HEART_SIZE // 10)) * number))
    def half_heart(self):
        self.image=pygame.image.load("../orange_emerald/images/half_gold_heart.png")
        self.image=pygame.transform.scale(self.image, ( HEART_SIZE, HEART_SIZE))
    def full_heart(self):
        self.image=pygame.image.load("../orange_emerald/images/gold_heart.png")
        self.image=pygame.transform.scale(self.image, ( HEART_SIZE, HEART_SIZE))
    def empty_heart(self):
        self.image = pygame.Surface((HEART_SIZE, HEART_SIZE))
        self.image.fill("black")
    def goto(self,x,y):
        self.rect.x=x
        self.rect.y=y
    def update_health(self):
        self.hp=player_list[self.player__].get_gold_hearts()
        player_list[self.player__].update_health()
        if 0 < self.hp <= 50 :
            self.hearts=1
        elif 50 < self.hp <= 100 :
            self.hearts=2
        elif 100 < self.hp <= 150 :
            self.hearts=3
        elif 150 < self.hp <= 200 :
            self.hearts=4
        elif 200 < self.hp <= 250:
            self.hearts = 5
        elif 250 < self.hp <= 300:
            self.hearts = 6
        elif 300 < self.hp <= 350:
            self.hearts = 7
        elif 350 < self.hp <= 400:
            self.hearts = 8
        elif 400 < self.hp <= 450:
            self.hearts = 9
        elif 450 < self.hp <= 500:
            self.hearts = 10
        elif 500 < self.hp <= 550 :
            self.hearts=11
        elif 550 < self.hp <= 600:
            self.hearts = 12
        elif 600 < self.hp <= 650:
            self.hearts = 13
        elif 650 < self.hp <= 700:
            self.hearts = 14
        elif 700 < self.hp <= 750:
            self.hearts = 15
        elif 750 < self.hp <= 800:
            self.hearts = 16
        if self.hearts>=self.number*2:
            self.full_heart()
        elif self.hearts +1 ==self.number*2:
            self.half_heart()
        else:
            self.empty_heart()
for a in range(5):
    drop_item(300,0,"lapis ore",0,"overworld")
random_overworld_chunk(0)
random_nether_chunk(0)
random_end_chunk(0)
drp_sprites=pygame.sprite.Group()
running = True
heart_list=pygame.sprite.Group()
while running:
    for i in heart_list:
        heart_list.remove(i)
    for f in players:
        players.remove(f)
    for r in sprites:
        sprites.remove(r)
    for w in drp_sprites:
        drp_sprites.remove(w)
    for a in range(1, 10):
        heart_list.add(heart(controlled_player_name, a))
    for a in range (1,8):
        heart_list.add(gold_heart(controlled_player_name, a))
    controlled_player = player_list[controlled_player_name]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if players_in_dimension[controlled_player_name] == "end":
        position = 4
    elif players_in_dimension[controlled_player_name] == "nether":
        position = 2
    else:
        position = 0
    if players_in_dimension[controlled_player_name] == "end":
        position = 5
    elif players_in_dimension[controlled_player_name] == "nether":
        position = 3
    else:
        position = 1
    for bl in all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])]:
        sprites.add(bl)
    does_fall = 1
    cactus_killer = 0
    lava_burner=0
    for i in all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])]:
        if is_collide(i.rect.x, player_list[controlled_player_name].rect.x, player_list[controlled_player_name].rect.y, i.rect.y) and not i.is_air():
            does_fall = 0
        if is_collide(i.rect.x, player_list[controlled_player_name].rect.x, player_list[controlled_player_name].rect.y, i.rect.y) and i.give_type() == "cactus":
            cactus_killer=1
        if is_collide(i.rect.x, player_list[controlled_player_name].rect.x, player_list[controlled_player_name].rect.y, i.rect.y) and i.give_type() == "lava":
            lava_burner=1
    if does_fall == 1:
        player_list[controlled_player_name].fall()
    if cactus_killer==1:
        player_list[controlled_player_name].damage(7)
    if lava_burner==1:
        player_list[controlled_player_name].damage(20)
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        jumper = 0
        for i in all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])]:
            if is_collide(i.rect.x, controlled_player.rect.x, controlled_player.rect.y, i.rect.y, 15,
                          15) and i.is_air():
                jumper = 1
        if jumper == 1:
            if controlled_player.rect.x + controlled_player.speed > SPACE_SIZE:
                player_list[controlled_player_name].left()
            else:
                if -2000 < players_in_chunks[controlled_player_name] < 1999:
                    add_chunks()
                    add_chunks()
                    players_in_chunks[controlled_player_name]-=1
                else:
                    players_in_chunks[controlled_player_name] = 1998
                player_list[controlled_player_name].goto(56 * 30 + SPACE_SIZE - 15, player_list[controlled_player_name].rect.y)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        jumper = 0
        for i in all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])]:
            if is_collide(i.rect.x, controlled_player.rect.x, controlled_player.rect.y, i.rect.y, 15,
                          15) and i.is_air():
                jumper = 1
        if jumper == 1:
            if controlled_player.rect.x + controlled_player.speed < 56 * 30 + SPACE_SIZE:
                player_list[controlled_player_name].right()
            else:
                if -2000 < players_in_chunks[controlled_player_name] < 1999:
                    add_chunks()
                    add_chunks()
                    players_in_chunks[controlled_player_name]+=1
                else:
                    players_in_chunks[controlled_player_name] = -1999
                player_list[controlled_player_name].goto(SPACE_SIZE+BLOCK_WIDTH//6, player_list[controlled_player_name].rect.y)
    for key, player4 in player_list.items():
        if players_in_dimension[key] == players_in_dimension[controlled_player_name]:
            if players_in_chunks[key] == players_in_chunks[controlled_player_name]:
                players.add(player4)
    if keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]:
        jumper = 0
        for i in all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])]:
            if is_collide(i.rect.x, controlled_player.rect.x, controlled_player.rect.y, i.rect.y) and not i.is_air():
                jumper = 2
        if jumper == 2:
            for i in all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])]:
                if is_collide(i.rect.x, controlled_player.rect.x, controlled_player.rect.y, i.rect.y, 15,
                              15) and i.is_air():
                    jumper = 1
        if jumper == 1:
            player_list[controlled_player_name].jump()
    reeee=-1
    destroyer=0
    for drp in dropped_items:
        reeee+=1
        drp_fall=1
        for i in all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])]:
            if is_collide(i.rect.x, drp.rect.x, drp.rect.y, i.rect.y,DROP_SIZE,DROP_SIZE) and not i.is_air():
                drp_fall = 0
            if is_collide(i.rect.x, drp.rect.x,drp.rect.y, i.rect.y) and i.give_type() == "cactus":
                destroyer=1
            if is_collide(i.rect.x, drp.rect.x,drp.rect.y, i.rect.y) and i.give_type() == "lava":
                destroyer= 1
        if drp_fall==1:
            drp.fall()
        if drp.is_in_chunk(players_in_chunks[controlled_player_name]):
            if drp.is_in_dimension(players_in_dimension[controlled_player_name]):
                drp_sprites.add(drp)
        if drop.should_despawn(drp) or destroyer==1:
            del dropped_items[reeee]
    player_list[controlled_player_name].heal(1)
    screen.fill("black")
    sprites.draw(screen)
    for hearts in heart_list:
        hearts.update_health()
    drp_sprites.draw(screen)
    players.draw(screen)
    heart_list.draw(screen)
    pygame.display.flip()