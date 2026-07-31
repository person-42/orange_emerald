import datetime
import pygame
from biomes import *

pygame.init()
pygame.font.init()

class NoBlockError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("PAPER MINECRAFT")
player_list = {}
players_in_chunks = {}
players_in_dimension = {}
controlled_player_name = "player1"
sprites = pygame.sprite.Group()
dropped_items = []
SCREEN_X = screen.get_size()[0]
SCREEN_Y = screen.get_size()[1]
#SCREEN_X=1000#remove
#SCREEN_Y=500#remove
SPACE_SIZE = SCREEN_X / 9.6
STRIP_SIZE = SCREEN_Y / 7.2
BLOCK_WIDTH = int((SCREEN_X - SPACE_SIZE) / 57)
BLOCK_HEIGHT = int((SCREEN_Y - STRIP_SIZE) / 31)
DROP_WIDTH = BLOCK_WIDTH / 2 + BLOCK_WIDTH / 7
DROP_HEIGHT = BLOCK_HEIGHT / 2 + BLOCK_WIDTH / 7
HEART_SIZE = BLOCK_HEIGHT * 1.5
FALL_SPEED = BLOCK_WIDTH / 3
PLAYER_WIDTH, PLAYER_HEIGHT = ((BLOCK_WIDTH / 2) + (BLOCK_WIDTH / 15)) * 2, BLOCK_HEIGHT * 2.5
slot = 1


def calculate_leave_drops():
    rand = random.randint(1, 20)
    if rand == 1:
        return "apple"
    elif rand < 4:
        return "sapling"
    else:
        return ""


block_image_list = {"iron ore": "images/iron_ore.png", "coal ore": "images/coal_ore.png",
                    "copper ore": "images/copper_ore.png", "diamond ore": "images/diamond_ore.png",
                    "gold ore": "images/gold_ore.png", "emerald ore": "images/emerald_ore.png",
                    "lapis ore": "images/lapis_ore.png", "redstone ore": "images/redstone_ore.png",
                    "nether gold ore": "images/nether_gold_ore.png",
                    "quartz ore": "images/quartz_ore.png"}
block_color_list = {"netherack": "#842020", "sand": "#ccb46d", "air": "#0dcaf0", "dirt": "#653208", "leaves": "#486317",
                    "stone": "#585B5C", "planks": "lightsalmon",
                    "bedrock": "#22202c", "end stone": "#C4BF4F", "grass": "green", "water": "blue",
                    "snow": "#f0e9d2", "cactus": "#03550c", "log": "#5b1a17", "lava": "#b54d05",
                    "cobblestone": "dimgray"}


def remove_minus_and_add_1(thing_):
    if str(thing_)[0] == "-":
        thing_ *= -1
        thing_ += 1
    return thing_


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
                        blockya = None
                        if biome == "forest" or biome == "snowy forest":
                            blockya = forest(i, l, 0, number)
                            if blockya == "grass" and biome == "snowy forest":
                                blockya = "snow"
                        elif biome == "desert":
                            blockya = desert(i, l, 0, number)
                        all_blocks[0][number].append(
                            block(x__=int(l * BLOCK_WIDTH + SPACE_SIZE), y__=int(i * BLOCK_HEIGHT), type_=blockya))
            else:
                all_blocks[1].append([])
                for l in range(57):
                    for i in range(31):
                        blockya = None
                        if biome == "forest" or biome == "snowy forest":
                            blockya = forest(i, l, 1, number)
                            if blockya == "grass" and biome == "snowy forest":
                                blockya = "snow"
                        elif biome == "desert":
                            blockya = desert(i, l, 1, number)
                        all_blocks[1][number].append(
                            block(x__=int(l * BLOCK_WIDTH + SPACE_SIZE), y__=int(i * BLOCK_HEIGHT), type_=blockya))


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
                     "netherack": "netherack", "sand": "sand", "dirt": "dirt", }
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
        if new_type in self.rtye:
            self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT), pygame.SRCALPHA)
            self.image.fill(self.block_colors[new_type])
        elif new_type in self.image_list:
            self.image = pygame.image.load(block_image_list[new_type])
            self.image = pygame.transform.scale(self.image, (BLOCK_WIDTH, BLOCK_HEIGHT))
        else:
            raise NoBlockError("Given type is not in any dictionary. No type or color mentioned")

    def get_size(self):
        return self.rect.size

    def weaken(self, material, tool_type, player_name):
        if self._type_ not in self.unbreakable_blocks:
            if tool_type == self.tool_list[self._type_]:
                self.health -= self.hardness_list[self._type_]
                self.health -= material * 5
            else:
                self.health -= material * 3 + 5
        if self.health <= 0:
            self.broke(player_name, material, tool_type)

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
        self.image = pygame.image.load("images/player_character.png")
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.items = {
            "logs": 0,
            "planks": 0,
            "stone": 0,
            "grass": 0,
            "dirt": 0,
            "cobblestone": 0,
            "emerald": 0,
            "diamond": 0,
            "redstone": 0,
            "cactus": 0,
            "lapis": 0,
            "lapis ore": 0,
            "redstone ore": 0,
            "emerald ore": 0,
            "netherack": 0,
            "diamond ore": 0,
            "coal ore": 0,
            "coal": 0,
            "sand": 0,
            "end stone": 0,
            "nether gold ore": 0,
            "gold ingot": 0,
            "iron ingot": 0,
            "iron ore": 0,
            "obsidian": 0,
            "quartz": 0,
            "glowstone": 0,
            "slimeball": 0,
            "ender pearl": 0,
            "pumpkin": 0,
            "wool": 0,
            "snowball": 0,
            "potato": 0,
            "carrot": 0,
            "beetroot": 0,
            "bone": 0,
            "gunpowder": 0,
            "string": 0,
            "feather": 0,
            "nether wart": 0,
            "bamboo": 0,
            "clay": 0,
            "nether brick": 0,
            "soul sand": 0,
            "mushroom": 0,
            "sugar": 0,
            "rabbit hide": 0,
            "raw chicken": 0,
            "raw beef": 0,
            "raw mutton": 0,
            "cooked chicken": 0,
            "cooked beef": 0,
            "cooked mutton": 0,
            "leather": 0,
            "gold ore": 0,
            "copper ore":0,
            "quartz ore":0
        }
        self.hotbar_items = {}
        self.inventory_items = {}
        self.health = 1000
        self.gold_health = 0
        self.speed = BLOCK_WIDTH / 6
        self.jump_speed = BLOCK_HEIGHT / 6
        self.fall_speed = FALL_SPEED
        self.fall_velocity = 0
        self.spawn_point = (25, 10)
        self.x = self.spawn_point[0]
        self.y = self.spawn_point[1]
        self.name = name
        self.rect = self.image.get_rect(center=(PLAYER_WIDTH // 2, PLAYER_HEIGHT // 2))
        self.go(self.x, self.y)
        self.inventory_full = False

    def go(self, x, y):
        self.x = x
        self.y = y

    def pick_up_item(self, item):
        self.items[item] += 1
        if item in self.hotbar_items:
            self.hotbar_items[item] += 1
        elif item in self.inventory_items:
            self.inventory_items[item] += 1
        elif len(self.hotbar_items) <= 8:
            self.hotbar_items[item] = 1
        elif len(self.inventory_items) <= 35:
            self.inventory_items[item] = 1
        else:
            self.inventory_full = True
            drop_item(self.rect.x, self.rect.y, item, players_in_chunks[controlled_player_name],
                      players_in_dimension[controlled_player_name])
            self.items[item] -= 1

    def goto(self, x, y):
        self.go(x, y)

    def give_hotbar_slot_items(self, num):
        qws = list(self.hotbar_items.keys())
        try:
            return qws[num - 1]
        except IndexError:
            return 0

    def give_hotbar_slot_numbers(self, num):
        wq = list(self.hotbar_items.values())
        try:
            return wq[num -1]
        except IndexError:
            return 0

    def is_inventory_full(self):
        return self.inventory_full

    def fall(self, multiplier=1):
        self.y += self.fall_speed * multiplier / BLOCK_HEIGHT
        self.fall_velocity += self.fall_speed * multiplier

    def left(self, multiplier=1):
        self.x -= self.speed * multiplier / BLOCK_WIDTH

    def right(self, multiplier=1):
        self.x += self.speed * multiplier / BLOCK_WIDTH

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
        self.y -= self.jump_speed * 10 / BLOCK_HEIGHT

    def check_inventory(self):
        for red, it in self.inventory_items.items():
            if it == 0:
                del self.inventory_items[red]
        for red, it in self.hotbar_items.items():
            if it == 0:
                del self.hotbar_items[red]

    def heal(self, hp=1):
        if self.health < 1000 - hp:
            self.health += hp
        else:
            self.health = 1000

    def damage(self, hp=1):
        if self.gold_health > hp:
            self.gold_health -= hp
        elif self.gold_health == 0:
            self.health -= hp
        else:
            self.gold_health -= hp
        self.update_health()

    def update_health(self):
        if self.gold_health < 0:
            print(self.health + self.gold_health)
            self.health += self.gold_health
            self.gold_health = 0

    def gold_heart(self, hp):
        if self.get_gold_hearts() < hp:
            self.gold_health = hp

    def update_position(self):
        self.rect.x = self.x * BLOCK_WIDTH
        self.rect.y = self.y * BLOCK_HEIGHT


class drop(pygame.sprite.Sprite):
    def __init__(self, x, y, type_, chunk_, dimension_):
        super().__init__()
        global block_image_list
        global block_color_list
        self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(30 // 2, 30 // 2))
        self.block_image_list = block_image_list
        self.block_color_list = block_color_list
        self.goto(x + random.randint(-100, 100) / 5, y)
        self.type_ = type_
        self.timer = (datetime.datetime.now().minute + 5) % 60
        self.chunk_ = chunk_
        self.dimension_ = dimension_
        self.change_image(new_type=type_)

    def change_image(self, new_type):
        self.type_ = new_type
        if new_type in self.block_color_list:
            self.image = pygame.Surface((DROP_WIDTH, DROP_HEIGHT), pygame.SRCALPHA)
            self.image.fill(self.block_color_list[new_type])
        elif new_type in self.block_image_list:
            self.image = pygame.image.load(block_image_list[new_type])
            self.image = pygame.transform.scale(self.image, (DROP_WIDTH, DROP_HEIGHT))
        else:
            raise NoBlockError("Given type is not in any dictionary. No image or color mentioned")

    def x(self):
        return self.rect.x

    def fall(self):
        self.rect.y += FALL_SPEED / 2

    def y(self):
        return self.rect.y

    def goto(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def is_in_chunk(self, _chunk_):
        if self.chunk_ == _chunk_:
            return True
        else:
            return False

    def is_in_dimension(self, dimension___):
        if self.dimension_ == dimension___:
            return True
        else:
            return False

    def should_despawn(self):
        if self.timer == datetime.datetime.now().minute:
            return True
        else:
            return False

    def give_type(self):
        return self.type_


def add_player(name):
    players_in_chunks[name] = 0
    players_in_dimension[name] = "overworld"
    player_list[name] = player(name)


add_player("player1")
add_player("player2")
players = pygame.sprite.Group()


def drop_item(x, y, type_, chunk_, dimension):
    dropped_items.append(drop(x=x, y=y, type_=type_, chunk_=chunk_, dimension_=dimension))


# Phyton special words
#import as while for return is if else elif in not True False def class try except finally raise pass global async break lambda  assert del None or from
def is_collide(x1, x2, y1, y2, x_reach=PLAYER_WIDTH // 2, y_reach=PLAYER_HEIGHT):
    if -x_reach <= x1 - x2 <= x_reach:
        if -y_reach <= y1 - y2 <= y_reach:
            return True
        else:
            return False
    else:
        return False


overworld_biomes = ["snowy forest", "forest", "desert"]
nether_biomes = []
end_biomes = []


def add_chunks(position):
    if len(all_blocks[position]) < 2001:
        random_overworld_chunk(len(all_blocks[1]))
        random_overworld_chunk(len(all_blocks[0]) * -1 - 1)
        random_nether_chunk(len(all_blocks[3]))
        random_nether_chunk(len(all_blocks[2]) * -1 - 1)
        random_end_chunk(len(all_blocks[5]))
        random_end_chunk(len(all_blocks[4]) * -1 - 1)


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
class hotbar_slot(pygame.sprite.Sprite):
    def __init__(self, number):
        super().__init__()
        self.image = pygame.image.load("images/hotbar_slot.png")
        self.image = pygame.transform.scale(self.image, (BLOCK_WIDTH * 3, BLOCK_HEIGHT * 3))
        self.rect = self.image.get_rect()
        self.goto(SPACE_SIZE * 2.95 + number * BLOCK_WIDTH * 3, SCREEN_Y - STRIP_SIZE )
        self.number = number

    def goto(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def select(self):
        self.image = pygame.image.load("images/selected_hotbar.png")
        self.image = pygame.transform.scale(self.image, (BLOCK_WIDTH * 3, BLOCK_HEIGHT * 3))

    def unselect(self):
        self.image = pygame.image.load("images/hotbar_slot.png")
        self.image = pygame.transform.scale(self.image, (BLOCK_WIDTH * 3, BLOCK_HEIGHT * 3))

    def update_slot(self, slots):
        if slots == self.number:
            self.select()
        else:
            self.unselect()
    def get_number(self):
        return self.number
hotbar = pygame.sprite.Group()


class heart(pygame.sprite.Sprite):
    def __init__(self, player__, number):
        super().__init__()
        global player_list
        self.image = pygame.image.load("images/heart.png")
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (HEART_SIZE, HEART_SIZE))
        self.player__ = player__
        self.number = number
        self.hearts = 0
        self.hp = player_list[self.player__].get_hearts()
        self.update_health()
        self.number = number
        self.goto(y=SCREEN_Y - HEART_SIZE, x=SPACE_SIZE / 1.4 + ((HEART_SIZE + (HEART_SIZE // 10)) * number))

    def empty_heart(self):
        self.image = pygame.image.load("images/empty_heart.png")
        self.image = pygame.transform.scale(self.image, (HEART_SIZE, HEART_SIZE))

    def half_heart(self):
        self.image = pygame.image.load("images/half_heart.png")
        self.image = pygame.transform.scale(self.image, (HEART_SIZE, HEART_SIZE))

    def full_heart(self):
        self.image = pygame.image.load("images/heart.png")
        self.image = pygame.transform.scale(self.image, (HEART_SIZE, HEART_SIZE))

    def goto(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update_health(self):
        self.goto(y=SCREEN_Y - BLOCK_WIDTH * 2, x=SPACE_SIZE / 1.4 + ((HEART_SIZE + (HEART_SIZE // 10)) * self.number))
        self.hp = player_list[self.player__].get_hearts()
        player_list[self.player__].update_health()
        if 0 < self.hp <= 50:
            self.hearts = 1
        elif 50 < self.hp <= 100:
            self.hearts = 2
        elif 100 < self.hp <= 150:
            self.hearts = 3
        elif 150 < self.hp <= 200:
            self.hearts = 4
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
        elif 500 < self.hp <= 550:
            self.hearts = 11
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
        if self.hearts >= self.number * 2:
            self.full_heart()
        elif self.hearts + 1 == self.number * 2:
            self.half_heart()
        else:
            self.empty_heart()


class held_item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global player_list
        global block_color_list
        global block_image_list
        self.block_color_list = block_color_list
        self.block_image_list = block_image_list
        self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

    def goto(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def change_image(self, new_type):
        if new_type in self.block_color_list:
            self.image = pygame.Surface((BLOCK_WIDTH * 0.4, BLOCK_HEIGHT * 0.4), pygame.SRCALPHA)
            self.image.fill(self.block_color_list[new_type])
        elif new_type in self.block_image_list:
            self.image = pygame.image.load(block_image_list[new_type])
            self.image = pygame.transform.scale(self.image, (BLOCK_WIDTH * 0.4, BLOCK_HEIGHT * 0.4))
        else:
            self.image = pygame.Surface((0, 0), pygame.SRCALPHA)

    def update_image(self, slots):
        e = player_list[controlled_player_name].hotbar_items
        qws = list(e.keys())
        try:
            s = qws[slots]
        except IndexError:
            s = None
        self.change_image(s)
        self.goto_player()

    def goto_player(self):
        self.goto(player_list[controlled_player_name].rect.x + BLOCK_WIDTH,
                  player_list[controlled_player_name].rect.y + BLOCK_HEIGHT)


class hotbar_item(pygame.sprite.Sprite):
    def __init__(self, number):
        super().__init__()
        global player_list
        global block_color_list
        global block_image_list
        self.block_image_list = block_image_list
        self.block_color_list = block_color_list
        self.player_list = player_list
        self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.goto(SPACE_SIZE * 3.05 + number * BLOCK_WIDTH * 3, SCREEN_Y - STRIP_SIZE /1.22)
        self.change_image(new_type=player_list[controlled_player_name].give_hotbar_slot_items(number))
        self.number = number

    def goto(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def num(self):
        return self.number

    def change_image(self, new_type):
        if new_type in self.block_color_list:
            self.image = pygame.Surface((BLOCK_WIDTH * 1.5, BLOCK_HEIGHT * 1.5), pygame.SRCALPHA)
            self.image.fill(self.block_color_list[new_type])
        elif new_type in self.block_image_list:
            self.image = pygame.image.load(block_image_list[new_type])
            self.image = pygame.transform.scale(self.image, (BLOCK_WIDTH * 1.5, BLOCK_HEIGHT * 1.5))
        else:
            self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT), pygame.SRCALPHA)
            self.image.fill("black")


class gold_heart(pygame.sprite.Sprite):
    def __init__(self, player__, number):
        super().__init__()
        global player_list
        self.image = pygame.image.load("images/gold_heart.png")
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (HEART_SIZE, HEART_SIZE))
        self.player__ = player__
        self.number = number
        self.hearts = 0
        self.hp = player_list[self.player__].get_gold_hearts()
        self.update_health()
        self.number = int(number)
        self.goto(y=SCREEN_Y - HEART_SIZE * 3,
                  x=SPACE_SIZE / 1.4 + ((HEART_SIZE + (HEART_SIZE // 10)) * number))

    def half_heart(self):
        self.image = pygame.image.load("images/half_gold_heart.png")
        self.image = pygame.transform.scale(self.image, (HEART_SIZE, HEART_SIZE))

    def full_heart(self):
        self.image = pygame.image.load("images/gold_heart.png")
        self.image = pygame.transform.scale(self.image, (HEART_SIZE, HEART_SIZE))

    def empty_heart(self):
        self.image = pygame.Surface((HEART_SIZE, HEART_SIZE))
        self.image.fill("black")

    def goto(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update_health(self):
        self.hp = player_list[self.player__].get_gold_hearts()
        player_list[self.player__].update_health()
        if 0 < self.hp <= 50:
            self.hearts = 1
        elif 50 < self.hp <= 100:
            self.hearts = 2
        elif 100 < self.hp <= 150:
            self.hearts = 3
        elif 150 < self.hp <= 200:
            self.hearts = 4
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
        elif 500 < self.hp <= 550:
            self.hearts = 11
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
        if self.hearts >= self.number * 2:
            self.full_heart()
        elif self.hearts + 1 == self.number * 2:
            self.half_heart()
        else:
            self.empty_heart()
class text(pygame.sprite.Sprite):
    def __init__(self, content, font_size, color, position):
        super().__init__()
        self.content = content
        self.font_size = font_size
        self.color = color
        self.position = position
        self.font = pygame.font.Font(None, self.font_size)
        self.text_surface = self.font.render(self.content, True, self.color)
        self.image = self.text_surface
        self.rect = self.text_surface.get_rect(topleft=self.position)
for a in range(2):#remove
    drop_item(300, 0, "lapis ore", 0, "overworld")
    drop_item(300, 0, "redstone ore", 0, "overworld")
    drop_item(300, 0, "nether gold ore", 0, "overworld")
    drop_item(300, 0, "gold ore", 0, "overworld")
    drop_item(300, 0, "cactus", 0, "overworld")
    drop_item(300, 0, "diamond ore", 0, "overworld")
    drop_item(300, 0, "netherack", 0, "overworld")
    drop_item(300, 0, "sand", 0, "overworld")
    drop_item(300, 0, "grass", 0, "overworld")
    drop_item(300, 0, "dirt", 0, "overworld")
    drop_item(300, 0, "stone", 0, "overworld")
    drop_item(300, 0, "end stone", 0, "overworld")
def hotbar_text(number):
    content=player_list[controlled_player_name].give_hotbar_slot_numbers(number)
    if int(content) > 1:
        size = BLOCK_WIDTH*2
        color = "white"
        x = SPACE_SIZE * 3.1 +number*BLOCK_WIDTH*3
        y=SCREEN_Y - STRIP_SIZE / 3
        return text(str(content), size, color, (x,y))
    else:
        return text("", 0, "black", (SPACE_SIZE * 2.95 + number * BLOCK_WIDTH * 3, SCREEN_Y - STRIP_SIZE / 2))
hotbar_itemz = pygame.sprite.Group()
random_overworld_chunk(0)
random_nether_chunk(0)
random_end_chunk(0)
drp_sprites = pygame.sprite.Group()
heart_list = pygame.sprite.Group()
held_items = pygame.sprite.Group()
player_list[controlled_player_name].pick_up_item("copper ore")#remove
player_list[controlled_player_name].pick_up_item("quartz ore")#remove
hotbar_amount=pygame.sprite.Group()
