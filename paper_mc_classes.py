from paper_mc_constants import *
# CALCULATE  WHAT TO DROP AFTER A LEAF IS BROKEN
def calculate_leave_drops(random_number):
    rand = random_number
    if rand == 1:
        return "apple"
    elif rand < 6:
        return "sapling"
    else:
        return ""
#COUNT TIME IT TAKES BEFORE ITEM DESPAWN
import datetime


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
                for l in range(57):  # x position
                    for i in range(31):
                        blockya = None
                        if biome == "forest" or biome == "snowy forest":
                            blockya = forest(i, l, 0, number)
                            if blockya == "grass" and biome == "snowy forest":
                                blockya = "snow"
                        elif biome == "desert":
                            blockya = desert(i, l, 0, number)
                        all_blocks[0][number].append(
                            block(
                                x__=int(l * BLOCK_WIDTH + SPACE_SIZE),
                                y__=int(i * BLOCK_HEIGHT),
                                type_=blockya,
                            )
                        )
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
                            block(
                                x__=int(l * BLOCK_WIDTH + SPACE_SIZE),
                                y__=int(i * BLOCK_HEIGHT),
                                type_=blockya,
                            )
                        )


class block(pygame.sprite.Sprite):
    def __init__(self, type_="grass", x__=0, y__=0):
        super().__init__()
        self.growth=0
        self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT), pygame.SRCALPHA)
        rtye = block_color_list
        image_rtrt = block_image_list
        self.image_list = image_rtrt
        self.unbreakable_blocks = unbreakable_blocks
        self.rtye = rtye
        self.image_list = image_rtrt

        self.drop_list = drop_list
        drop_amount = {
            "copper ore": random.randint(1, 3),
            "lapis ore": random.randint(1, 8),
            "redstone ore": random.randint(1, 5),
            "snow": random.randint(1, 3),
            "nether gold ore": random.randint(2, 6),
            "quartz ore": random.randint(1, 3),
            "tall grass":random.choice(WHEAT_SEED_DECIDER)
        }
        self.health = 100
        self.tool_list = tool_list

        self.hardness_list = hardness_list
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
        if self._type_ == "air" or self._type_ in immortal_air_blocks or self._type_ in liquids:
            return True
        else:
            return False

    def give_type(self):
        return self._type_

    def change_type(self, new_type):
        self._type_ = new_type
        self.health=100
        self.growth=0
        if new_type in self.rtye:
            self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT), pygame.SRCALPHA)
            self.image.fill(self.block_colors[new_type])
        elif new_type in self.image_list:
            self.image = pygame.image.load(block_image_list[new_type])
            self.image = pygame.transform.scale(self.image, (BLOCK_WIDTH, BLOCK_HEIGHT))
        else:
            raise NoBlockError(
                f"Given type is not in any dictionary. No type or color mentioned. The failed type is : {new_type}"
            )

    def get_size(self):
        return self.rect.size

    def weaken(self, material, tool_type, break_speed):
        if self._type_ not in self.unbreakable_blocks:
            hardness = self.hardness_list.get(self._type_, 20)
            if tool_type == self.tool_list.get(self._type_, ""):
                self.health -= hardness
            self.health -= break_speed
        if self.health <= 0:
            self.broke(material, tool_type)

    def heal(self):
        if self.health < 99:
            self.health += 1
        else:
            self.health = 100
    def broke(self, material, tool):
        global wheat_amount
        global  multi_item_amount
        global carrot_amount
        drop_list["leaves"] = calculate_leave_drops(random.randint(1, 20))
        wheat_amount = [random.randint(1, 3), random.randint(1, 4)]
        carrot_amount = [random.randint(1, 3), random.randint(1, 4)]
        multi_item_amount["grown wheat plant"]=wheat_amount
        multi_item_amount["grown carrot plant"]=carrot_amount
        self.health=100
        self.growth=0
        global player_list
        original_type = self.give_type()
        self.change_type("air")
        if original_type in self.unbreakable_blocks:
            return
        if original_type not in self.drop_list:
            if original_type not in list(multi_item_drops.keys()):
                return
        min_mat = self.minimum_material.get(original_type, 0)
        correct_tool = self.tool_list.get(original_type, "")
        if min_mat == 0 or (material >= min_mat and tool == correct_tool):
            drop_name = self.drop_list.get(original_type,True)
            if not drop_name:
                if original_type not in list(multi_item_drops.keys()):
                    return
            if original_type in list(multi_item_amount.keys()):
                count_list=multi_item_amount[original_type]
                items_list=multi_item_drops[original_type]
                bz=0
                for a in count_list:
                    for _ in range(a):
                        drop_item(self.rect.x / BLOCK_WIDTH, self.rect.y / BLOCK_HEIGHT, items_list[bz],
                                  players_in_chunks[controlled_player_name],
                                  players_in_dimension[controlled_player_name])
                    bz += 1
            else:
                count = self.drop_amount.get(original_type, 1)
                item_to_drop = self.drop_list.get(original_type, original_type)
                for _ in range(count):
                    drop_item(self.rect.x / BLOCK_WIDTH, self.rect.y / BLOCK_HEIGHT, item_to_drop,
                              players_in_chunks[controlled_player_name], players_in_dimension[controlled_player_name])
    def grow(self,position,life):
        growable_items={"sapling":"tree","ungrown wheat plant":"grown wheat plant","ungrown carrot plant":"grown carrot plant","sugar cane":"up","cactus":"up"}
        if self._type_ in growable_items.keys():
            self.growth+=1
            if self.growth == 500:
                self.health=100
                if growable_items[self._type_]=="tree":
                    self.change_type("log")
                    try:
                        if all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])][life-1].give_type()=="air":
                            all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])][life-1].change_type("log")
                    except IndexError:
                        pass
                    try:
                        if all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])][life-2].give_type()=="air":
                            all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])][life-2].change_type("log")
                    except IndexError:
                        pass
                    try:
                        if all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])][life-3].give_type()=="air":
                            all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])][life-3].change_type("leaves")
                    except IndexError:
                        pass
                    try:
                        if all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])][life-4].give_type()=="air":
                            all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])][life-4].change_type("leaves")
                    except IndexError:
                        pass
                    try:
                        if all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])][life - 5].give_type() == "air":
                            all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])][life - 5].change_type("leaves")
                    except IndexError:
                        pass
                    try:
                        if all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])][life - 4-31].give_type() == "air":
                            all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])][life - 4-31].change_type("leaves")
                    except IndexError:
                        pass
                    try:
                        if all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])][life - 3-31].give_type() == "air":
                            all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])][life - 3-31].change_type("leaves")
                    except IndexError:
                        pass
                    try:
                        if all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])][life - 3+31].give_type() == "air":
                            all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])][life - 3+31].change_type("leaves")
                    except IndexError:
                        pass
                    try:
                        if all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])][life - 4+31].give_type() == "air":
                            all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])][life - 4+31].change_type("leaves")
                    except IndexError:
                        pass
                elif growable_items[self._type_]== "up":
                    try:
                        if all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])][life-1].give_type()=="air":
                            all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])][life-1].change_type(self._type_)
                    except IndexError:
                        pass
                else:
                    self.change_type(growable_items[self._type_])
        else:
            self.growth=0

class player(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.image = pygame.image.load("images/player_character.png")
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.hotbar_items = {
            "1": "",
            "2": "",
            "3": "",
            "4": "",
            "5": "",
            "6": "",
            "7": "",
            "8": "",
            "9": ""
        }
        self.hotbar_amount = {
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 0,
            "5": 0,
            "6": 0,
            "7": 0,
            "8": 0,
            "9": 0
        }
        self.inventory_items = {
            "1": "",
            "2": "",
            "3": "",
            "4": "",
            "5": "",
            "6": "",
            "7": "",
            "8": "",
            "9": "",
            "10": "",
            "11": "",
            "12": "",
            "13": "",
            "14": "",
            "15": "",
            "16": "",
            "17": "",
            "18": "",
            "19": "",
            "20": "",
            "21": "",
            "22": "",
            "23": "",
            "24": "",
            "25": "",
            "26": "",
            "27": "",
            "28": "",
            "29": "",
            "30": "",
            "31": "",
            "32": "",
            "33": "",
            "34": "",
            "35": "",
            "36": ""
        }
        self.unstackable_items=unstackable_items
        self.inventory_amount = {
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 0,
            "5": 0,
            "6": 0,
            "7": 0,
            "8": 0,
            "9": 0,
            "10": 0,
            "11": 0,
            "12": 0,
            "13": 0,
            "14": 0,
            "15": 0,
            "16": 0,
            "17": 0,
            "18": 0,
            "19": 0,
            "20": 0,
            "21": 0,
            "22": 0,
            "23": 0,
            "24": 0,
            "25": 0,
            "26": 0,
            "27": 0,
            "28": 0,
            "29": 0,
            "30": 0,
            "31": 0,
            "32": 0,
            "33": 0,
            "34": 0,
            "35": 0,
            "36": 0
        }
        self.health = 1000
        self.gold_health = 0
        self.speed = BLOCK_WIDTH / 6
        self.jump_speed = BLOCK_HEIGHT / 6
        self.fall_speed = FALL_SPEED
        self.fall_velocity = 0
        self.fall_start_y = None
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
        # Stack onto existing hotbar slot
        for slots, slot_item in self.hotbar_items.items():
            if item == slot_item:
                if slot_item not in self.unstackable_items:
                    if self.hotbar_amount[slots] < 64:
                        self.hotbar_amount[slots] += 1
                        return
        # Stack onto existing inventory slot
        for slots, slot_item in self.inventory_items.items():
            if item == slot_item:
                if slot_item not in self.unstackable_items:
                    if self.inventory_amount[slots] < 64:
                        self.inventory_amount[slots] += 1
                        return
        # Place in first free hotbar slot
        for slots, slot_item in self.hotbar_items.items():
            if slot_item == "":
                self.hotbar_items[slots] = item
                self.hotbar_amount[slots] = 1
                return
        # Place in first free inventory slot
        for slots, slot_item in self.inventory_items.items():
            if slot_item == "":
                self.inventory_items[slots] = item
                self.inventory_amount[slots] = 1
                return
        # Both full — drop the item

        self.inventory_full = True
        drop_item(
            self.x,
            self.y,
            item,
            players_in_chunks[controlled_player_name],
            players_in_dimension[controlled_player_name],
        )

    def remove_item(self, number, area="hotbar"):
        if area == "inventory":
            if self.inventory_amount[str(number)] > 1:
                self.inventory_amount[str(number)] -= 1
            elif self.inventory_amount[str(number)] == 1:
                self.inventory_amount[str(number)] -= 1
                self.inventory_items[str(number)] = ""
            else:
                # TRIED TO REMOVE NON EXISTENT ITEM
                pass
        else:
            if self.hotbar_amount[str(number)] > 1:
                self.hotbar_amount[str(number)] -= 1
            elif self.hotbar_amount[str(number)] == 1:
                self.hotbar_amount[str(number)] -= 1
                self.hotbar_items[str(number)] = ""
            else:
                # TRIED TO REMOVE NON EXISTENT ITEM
                pass
    def put_in_slot(self,slots,item,area="hotbar",amount=1):
        if area == "inventory":
            self.inventory_amount[str(slots)] = amount
            self.inventory_items[str(slots)] = item
        else:
            self.hotbar_amount[str(slots)] = amount
            self.hotbar_items[str(slots)] = item
            print(self.hotbar_amount,self.hotbar_items)
    def goto(self, x, y):
        self.go(x, y)

    def give_hotbar_slot_items(self, num):
        if self.hotbar_items[str(num)] == "":
            return 0
        else:
            return self.hotbar_items[str(num)]

    def give_hotbar_slot_numbers(self, num):
        return self.hotbar_amount[str(num)]

    def is_inventory_full(self):
        return self.inventory_full

    def fall(self, multiplier=1):
        if self.fall_start_y is None:
            self.fall_start_y = self.y
        self.fall_velocity += self.fall_speed * multiplier * 0.15
        if self.fall_velocity > FALL_SPEED * 4:
            self.fall_velocity = FALL_SPEED * 4
        self.y += self.fall_velocity / BLOCK_HEIGHT

    def land(self, no_fall_damage=False):
        if self.fall_start_y is not None:
            if not no_fall_damage:
                blocks_fallen = self.y - self.fall_start_y
                if blocks_fallen > 3:
                    damage_hp = int((blocks_fallen - 3) * 25)
                    self.damage(damage_hp)
            self.fall_start_y = None
        self.fall_velocity = 0

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


    def size(self):
        return self.rect.size

    def jump(self):
        self.y -= self.jump_speed * 10 / BLOCK_HEIGHT

    def check_inventory(self):
        for slot in self.hotbar_items:
            if self.hotbar_amount[slot] == 0:
                self.hotbar_items[slot] = ""
        for slot in self.inventory_items:
            if self.inventory_amount[slot] == 0:
                self.inventory_items[slot] = ""

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
        self.goto(x + random.randint(-10, 10) / 10, y)
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
        elif new_type in item_list:
            self.image = pygame.image.load(item_list[new_type])
            self.image = pygame.transform.scale(self.image, (DROP_WIDTH, DROP_HEIGHT))
        elif new_type in self.block_image_list:
            self.image = pygame.image.load(block_image_list[new_type])
            self.image = pygame.transform.scale(self.image, (DROP_WIDTH, DROP_HEIGHT))
        else:
            # fallback: magenta so missing drops are visible but don't crash
            self.image = pygame.Surface((DROP_WIDTH, DROP_HEIGHT), pygame.SRCALPHA)
            self.image.fill("#FF00FF")

    def fall(self):
        self.y += FALL_SPEED / 2 / BLOCK_HEIGHT

    def goto(self, x, y):
        self.x = x
        self.y = y

    def update_position(self):
        self.rect.x = int(self.x * BLOCK_WIDTH)
        self.rect.y = int(self.y * BLOCK_HEIGHT)

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


def drop_item(x, y, type_, chunk_, dimension,number=1):
    if type_ in drops:
        type_=drops[type_]
    for a in range(number):
        dropped_items.append(
            drop(x=x, y=y, type_=type_, chunk_=chunk_, dimension_=dimension)
        )


# Phyton special words
# import as while for return is if else elif in not True False def class try except finally raise pass global async break lambda  assert del None or from
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
    if len(all_blocks[position]) < POSITIVE_BORDER+2:
        random_overworld_chunk(len(all_blocks[1]))
        random_overworld_chunk((len(all_blocks[0]) * -1) - 1)
        random_nether_chunk(len(all_blocks[3]))
        random_nether_chunk((len(all_blocks[2]) * -1 )- 1)
        random_end_chunk(len(all_blocks[5]))
        random_end_chunk((len(all_blocks[4]) * -1 )- 1)


def random_overworld_chunk(position__):
    if str(position__)[0] == "-":
        p_n = "-"
    else:
        p_n = "+"
    bi = random.choice(overworld_biomes)
    remove_minus_and_add_1(position__)
    chunk(number=position__, pos_neg=p_n, dimension="overworld", biome=bi)


def random_nether_chunk(position__):
    pass


def random_end_chunk(position__):
    pass


# BAD_CHARACTERS LOL
# !£$?؟
class hotbar_slot(pygame.sprite.Sprite):
    def __init__(self, number):
        super().__init__()
        self.image = pygame.image.load("images/hotbar_slot.png")
        self.image = pygame.transform.scale(
            self.image, (BLOCK_WIDTH * 3, BLOCK_HEIGHT * 3)
        )
        self.rect = self.image.get_rect()
        self.goto(SPACE_SIZE * 2.95 + number * BLOCK_WIDTH * 3, SCREEN_Y - STRIP_SIZE)
        self.number = number

    def goto(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def select(self):
        self.image = pygame.image.load("images/selected_hotbar.png")
        self.image = pygame.transform.scale(
            self.image, (BLOCK_WIDTH * 3, BLOCK_HEIGHT * 3)
        )

    def unselect(self):
        self.image = pygame.image.load("images/hotbar_slot.png")
        self.image = pygame.transform.scale(
            self.image, (BLOCK_WIDTH * 3, BLOCK_HEIGHT * 3)
        )

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
        self.goto(
            y=SCREEN_Y - HEART_SIZE,
            x=SPACE_SIZE / 1.4 + ((HEART_SIZE + (HEART_SIZE // 10)) * number),
        )

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
        self.goto(
            y=SCREEN_Y - BLOCK_WIDTH * 2,
            x=SPACE_SIZE / 1.4 + ((HEART_SIZE + (HEART_SIZE // 10)) * self.number),
        )
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
            self.image = pygame.Surface(
                (BLOCK_WIDTH * 0.4, BLOCK_HEIGHT * 0.4), pygame.SRCALPHA
            )
            self.image.fill(self.block_color_list[new_type])
        elif new_type in item_list:
            self.image = pygame.image.load(item_list[new_type])
            self.image = pygame.transform.scale(self.image, (BLOCK_WIDTH * 0.4, BLOCK_HEIGHT * 0.4))
        elif new_type in self.block_image_list:
            self.image = pygame.image.load(block_image_list[new_type])
            self.image = pygame.transform.scale(
                self.image, (BLOCK_WIDTH * 0.4, BLOCK_HEIGHT * 0.4)
            )
        else:
            self.image = pygame.Surface((0, 0), pygame.SRCALPHA)

    def update_image(self, slots):
        # slots is 0-indexed (slot-1); give_hotbar_slot_items expects 1-indexed
        self.change_image(player_list[controlled_player_name].give_hotbar_slot_items(slots))
        self.goto_player()

    def goto_player(self):
        self.goto(
            player_list[controlled_player_name].rect.x + BLOCK_WIDTH,
            player_list[controlled_player_name].rect.y + BLOCK_HEIGHT,
        )


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
        self.goto(
            SPACE_SIZE * 3.05 + number * BLOCK_WIDTH * 3, SCREEN_Y - STRIP_SIZE / 1.22
        )
        self.change_image(
            new_type=player_list[controlled_player_name].give_hotbar_slot_items(number)
        )
        self.number = number

    def goto(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def num(self):
        return self.number

    def change_image(self, new_type):
        if new_type in self.block_color_list:
            self.image = pygame.Surface(
                (BLOCK_WIDTH * 1.5, BLOCK_HEIGHT * 1.5), pygame.SRCALPHA
            )
            self.image.fill(self.block_color_list[new_type])
        elif new_type in item_list:
            self.image = pygame.image.load(item_list[new_type])
            self.image = pygame.transform.scale(
                self.image, (BLOCK_WIDTH * 1.5, BLOCK_HEIGHT * 1.5)
            )
        elif new_type in self.block_image_list:
            self.image = pygame.image.load(block_image_list[new_type])
            self.image = pygame.transform.scale(
                self.image, (BLOCK_WIDTH * 1.5, BLOCK_HEIGHT * 1.5)
            )
            self.image = pygame.transform.scale(
                self.image, (BLOCK_WIDTH * 1.5, BLOCK_HEIGHT * 1.5)
            )
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
        self.goto(
            y=SCREEN_Y - HEART_SIZE * 3,
            x=SPACE_SIZE / 1.4 + ((HEART_SIZE + (HEART_SIZE // 10)) * number),
        )

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
        self.font_size = int(font_size)
        self.color = color
        self.position = position
        self.font = pygame.font.Font(None, self.font_size)
        self.text_surface = self.font.render(self.content, True, self.color)
        self.image = self.text_surface
        self.rect = self.text_surface.get_rect(topleft=self.position)


def hotbar_text(number):
    content = player_list[controlled_player_name].give_hotbar_slot_numbers(number)
    if int(content) > 1:
        size = BLOCK_WIDTH * 2
        color = "white"
        x = SPACE_SIZE * 3.1 + number * BLOCK_WIDTH * 3
        y = SCREEN_Y - STRIP_SIZE / 3
        return text(str(content), size, color, (x, y))
    else:
        return text(
            "",
            0,
            "black",
            (SPACE_SIZE * 2.95 + number * BLOCK_WIDTH * 3, SCREEN_Y - STRIP_SIZE / 2),
        )


def held_item_text(slots):
    content = player_list[controlled_player_name].give_hotbar_slot_items(slots)
    content=names.get(content,content)
    if content == 0:
        return text(
            "",
            0,
            "black",
            (0, 0),
        )
    else:
        size = BLOCK_WIDTH * 2
        color = "darkgreen"
        x, y = SCREEN_X / 2, SCREEN_Y - STRIP_SIZE * 1.2
        return text(str(content), int(size), color, (x, y))

def coord_text():
    content = f"chunk: {round(players_in_chunks[controlled_player_name])}  x: {round(player_list[controlled_player_name].x)-7} y:{round(player_list[controlled_player_name].y)}"
    size=BLOCK_HEIGHT
    color = "gold"
    x,y = 0,0
    return text(content, size, color, (x, y))

hotbar_itemz = pygame.sprite.Group()
random_overworld_chunk(0)
random_nether_chunk(0)
random_end_chunk(0)
drp_sprites = pygame.sprite.Group()
heart_list = pygame.sprite.Group()
held_items = pygame.sprite.Group()
hotbar_amount = pygame.sprite.Group()
hotbar_top = pygame.sprite.Group()
coords = pygame.sprite.Group()
def give_item(item,amount=1):
    for _ in range(amount):
       player_list[controlled_player_name].pick_up_item(item)
"""give_item("netherite sword")
give_item("mace")
give_item("wind charge",64)
give_item("golden apple",64)
give_item("bow")
give_item("ender pearl",64)
give_item("netherite spear")
give_item("firework rocket",64)
give_item("elytra")"""
