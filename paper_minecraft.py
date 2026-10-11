import asyncio
import random

all_blocks = [[], [], [], [], [], []]  #-+-+-+ negative chunk,positive chunk
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
        elif randomizer<5:
            ere = "tall grass"
        elif randomizer==6:
            ere="grown carrot plant"
        else:
            ere="air"
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
        elif randomizer==3:
            ere="sugar cane"
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
import pygame
def init():
    pygame.init()
    pygame.font.init()

init()
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
def remove_minus_and_add_1(thing_):
    if str(thing_)[0] == "-":
        thing_ *= -1
        thing_ += 1
    return thing_
NEGATIVE_BORDER=-1
POSITIVE_BORDER=remove_minus_and_add_1(NEGATIVE_BORDER)
PLAYER_WIDTH, PLAYER_HEIGHT = (
    ((BLOCK_WIDTH / 2) + (BLOCK_WIDTH / 15)) * 2,
    BLOCK_HEIGHT * 2.5,
)
slot = 1
# BLOCKS FALLEN THOROUGH BUT BLOCKS CAN NOT BE PLACED OVER
immortal_air_blocks=["sapling","sugar cane","tall grass","ungrown wheat plant","grown wheat plant","ungrown carrot plant","grown carrot plant"]
# BLOCKS THAT CAN NOT LOSE HEALTH
unbreakable_blocks = ["bedrock", "air", "water", "lava"]
# IMAGES CONNECTED TO BLOCKS
block_image_list = {
    "iron ore": "images/iron_ore.png",
    "coal ore": "images/coal_ore.png",
    "copper ore": "images/copper_ore.png",
    "diamond ore": "images/diamond_ore.png",
    "gold ore": "images/gold_ore.png",
    "emerald ore": "images/emerald_ore.png",
    "lapis ore": "images/lapis_ore.png",
    "redstone ore": "images/redstone_ore.png",
    "nether gold ore": "images/nether_gold_ore.png",
    "quartz ore": "images/quartz_ore.png",
    "sapling":"images/sapling.png",
    "wool":"images/wool.png",
    "sugar cane": "images/sugar_cane.png",
    "tall grass":"images/tall_grass.png",
    "grown wheat plant":"images/grown_wheat_plant.png",
    "ungrown wheat plant":"images/ungrown_wheat_plant.png",
    "grown carrot plant":"images/grown_carrot_plant.png",
    "ungrown carrot plant":"images/ungrown_carrot_plant.png",
    "cobblestone bricks":"images/cobblestone_bricks.png",
    "blackstone bricks":"images/blackstone_bricks.png",
    "sand bricks":"images/sand_bricks.png",
    "nether bricks":"images/nether_bricks.png",
    "end bricks":"images/end_stone_bricks.png",



}
#COLORS OF BLOCKS WITH A SOLID COLOR
block_color_list = {
    "netherack": "#842020",
    "sand": "#ccb46d",
    "air": "#0dcaf0",
    "dirt": "#653208",
    "leaves": "#486317",
    "stone": "#585B5C",
    "planks": "lightsalmon",
    "end stone": "#f5f189",
    "grass": "green",
    "water": "blue",
    "snow": "#f0e9d2",
    "cactus": "#03550c",
    "log": "#5b1a17",
    "lava": "#b54d05",
    "cobblestone": "dimgray",
    "bedrock": "#22202c",
    "blackstone":"#11062d",
    "gold block":"gold",
    "diamond block":"#37dbda",
    "iron block":"ivory",
    "redstone block":"red",
    "coal block":"#070e01",
    "netherite block":"#221b2b",
    "lapis block":"MediumBlue",
    "copper block":"#fd6b10",
    "quartz block":"#d8cdd9",
    "emerald block":"chartreuse",
    "obsidian":"#2a1944",
    }
#RANDOM ONE CHOSEN EACH TIME A TALL GRASS IS BROKEN
WHEAT_SEED_DECIDER=[1,0]
# IMAGES FOR NON BLOCKS
item_list = {
    "raw gold": "images/raw_gold.png",
    "apple": "images/apple.png",
    "iron ingot": "images/iron_ingot.png",
    "gold ingot": "images/gold_ingot.png",
    "netherite ingot": "images/netherite_ingot.png",
    "copper ingot": "images/copper_ingot.png",
    "raw iron": "images/raw_iron.png",
    "emerald": "images/emerald.png",
    "diamond": "images/diamond.png",
    "raw copper": "images/raw_copper.png",
    "netherite scrap": "images/netherite_scrap.png",
    "snowball": "images/snowball.png",
    "coal": "images/coal.png",
    "gold nugget": "images/gold_nugget.png",
    "copper nugget": "images/copper_nugget.png",
    "iron nugget": "images/iron_nugget.png",
    "golden apple": "images/golden_apple.png",
    "enchanted golden apple": "images/enchanted_golden_apple.png",
    "redstone": "images/redstone.png",
    "glowstone": "images/glowstone.png",
    "gunpowder": "images/gunpowder.png",
    "lapis": "images/lapis.png",
    "wooden sword": "images/wooden_sword.png",
    "stone sword": "images/stone_sword.png",
    "iron sword": "images/iron_sword.png",
    "gold sword": "images/gold_sword.png",
    "diamond sword": "images/diamond_sword.png",
    "netherite sword": "images/netherite_sword.png",
    "wooden pickaxe": "images/wooden_pickaxe.png",
    "stone pickaxe": "images/stone_pickaxe.png",
    "iron pickaxe": "images/iron_pickaxe.png",
    "gold pickaxe": "images/gold_pickaxe.png",
    "diamond pickaxe": "images/diamond_pickaxe.png",
    "netherite pickaxe": "images/netherite_pickaxe.png",
    "wooden axe": "images/wooden_axe.png",
    "stone axe": "images/stone_axe.png",
    "iron axe": "images/iron_axe.png",
    "gold axe": "images/gold_axe.png",
    "diamond axe": "images/diamond_axe.png",
    "netherite axe": "images/netherite_axe.png",
    "wooden shovel": "images/wooden_shovel.png",
    "stone shovel": "images/stone_shovel.png",
    "iron shovel": "images/iron_shovel.png",
    "gold shovel": "images/gold_shovel.png",
    "diamond shovel": "images/diamond_shovel.png",
    "netherite shovel": "images/netherite_shovel.png",
    "wooden hoe": "images/wooden_hoe.png",
    "stone hoe": "images/stone_hoe.png",
    "iron hoe": "images/iron_hoe.png",
    "gold hoe": "images/gold_hoe.png",
    "diamond hoe": "images/diamond_hoe.png",
    "netherite hoe": "images/netherite_hoe.png",
    "wooden spear": "images/wooden_spear.png",
    "stone spear": "images/stone_spear.png",
    "iron spear": "images/iron_spear.png",
    "gold spear": "images/gold_spear.png",
    "diamond spear": "images/diamond_spear.png",
    "netherite spear": "images/netherite_spear.png",
    "totem of undying":"images/totem.png",
    "copper sword": "images/copper_sword.png",
    "copper pickaxe": "images/copper_pickaxe.png",
    "copper axe": "images/copper_axe.png",
    "copper shovel": "images/copper_shovel.png",
    "copper hoe": "images/copper_hoe.png",
    "copper spear": "images/copper_spear.png",
        "leather helmet": "images/leather_helmet.png",
        "leather chestplate": "images/leather_chestplate.png",
        "leather leggings": "images/leather_leggings.png",
        "leather boots": "images/leather_boots.png",
        "copper helmet": "images/copper_helmet.png",
        "copper chestplate": "images/copper_chestplate.png",
        "copper leggings": "images/copper_leggings.png",
        "copper boots": "images/copper_boots.png",
        "gold helmet": "images/gold_helmet.png",
        "gold chestplate": "images/gold_chestplate.png",
        "gold leggings": "images/gold_leggings.png",
        "gold boots": "images/gold_boots.png",
        "iron helmet": "images/iron_helmet.png",
        "iron chestplate": "images/iron_chestplate.png",
        "iron leggings": "images/iron_leggings.png",
        "iron boots": "images/iron_boots.png",
        "diamond helmet": "images/diamond_helmet.png",
        "diamond chestplate": "images/diamond_chestplate.png",
        "diamond leggings": "images/diamond_leggings.png",
        "diamond boots": "images/diamond_boots.png",
        "netherite helmet": "images/netherite_helmet.png",
        "netherite chestplate": "images/netherite_chestplate.png",
        "netherite leggings": "images/netherite_leggings.png",
        "netherite boots": "images/netherite_boots.png",
    "mace":"images/mace.png",
    "bucket":"images/bucket.png",
    "water bucket":"images/water_bucket.png",
    "lava bucket":"images/lava_bucket.png",
    "carrot":"images/carrot.png",
    "golden carrot":"images/golden_carrot.png",
    "elytra":"images/elytra.png",
    "ender pearl":"images/ender_pearl.png",
    "eye of ender":"images/eye_of_ender.png",
    "blaze rod":"images/blaze_rod.png",
    "breeze rod": "images/breeze_rod.png",
    "blaze powder": "images/blaze_powder.png",
    "wind charge":"images/wind_charge.png",
    "firework rocket":"images/rocket.png",
    "quartz":"images/quartz.png",
    "wheat seeds":"images/wheat_seed.png",
    "bow":"images/bow.png",
    "charged bow":"images/charged_bow.png",
    "charging bow":"images/charging_bow.png",
    "wheat":"images/wheat.png",
    "carrot seeds":"images/carrot_seeds.png",
    "arrow":"images/arrow.png",
    "sugar": "images/sugar.png",
    "paper":"images/paper.png",







}
# TOOL LEVEL NEEDED TO DROP 0=FIST 1=WOOD/GOLD 2=STONE/COPPER 3=IRON 4=DIAMOND/NETHERITE
minimum_material = {
    "log": 0,
    "leaves": 0,
    "cactus": 0,
    "snow": 1,
    "grass": 0,
    "dirt": 0,
    "sand": 0,
    "gravel": 0,
    "clay": 0,
    "moss block": 1,
    "mushroom": 0,
    "flower": 0,
    "coal ore": 1,
    "copper ore": 1,
    "iron ore": 2,
    "gold ore": 3,
    "diamond ore": 4,
    "emerald ore": 3,
    "ancient debris": 4,
    "lapis ore": 2,
    "redstone ore": 2,
    "stone": 1,
    "cobblestone": 1,
    "obsidian": 4,
    "gold block": 3,
    "iron block": 2,
    "diamond block": 4,
    "emerald block": 3,
    "lapis block": 2,
    "redstone block": 2,
    "glowstone": 1,
    "sandstone": 1,
    "cut sandstone": 1,
    "smooth sandstone": 1,
    "terracotta": 1,
    "hay bale": 0,
    "scaffolding": 0,
    "banner": 0,
    "furnace": 0,
    "crafting table": 0,
    "chest": 0,
    "barrel": 0,
    "anvil": 2,
    "enchanting table": 4,
    "dispenser": 0,
    "shulker box": 0,
    "ice": 1,
    "packed ice": 2,
    "blue ice": 2,
    "magma block": 2,
    "netherack": 1,
    "nether gold ore": 0,
    "quartz ore": 0,
    "end stone": 0,
    "tall grass": 0,
    "nether brick": 1,
    "end brick": 1,
    "stone brick": 1,
    "blackstone brick": 1,
    "blackstone": 1,
    "grown wheat plant":0,
    "ungrown wheat plant":0,
    "grown carrot plant":0,
    "ungrown carrot plant":0,
}
#TOOL USED FOR NON FIST BLOCKS TO DROP
tool_list = {
    "log": "axe",
    "grass": "shovel",
    "dirt": "shovel",
    "stone": "pickaxe",
    "leaves": "hoe",
    "netherack": "pickaxe",
    "snow": "shovel",
    "cactus": "axe",
    "cobblestone": "pickaxe",
    "planks": "axe",
    "sand": "shovel",
    "end stone": "pickaxe",
    "iron ore": "pickaxe",
    "coal ore": "pickaxe",
    "copper ore": "pickaxe",
    "diamond ore": "pickaxe",
    "gold ore": "pickaxe",
    "emerald ore": "pickaxe",
    "redstone ore": "pickaxe",
    "lapis ore": "pickaxe",
    "nether gold ore": "pickaxe",
    "quartz ore": "pickaxe",
    "moss block": "shovel",
    "gravel": "shovel",
    "obsidian": "pickaxe",
    "ancient debris": "pickaxe",
    "bricks": "pickaxe",
    "stone brick": "pickaxe",
    "hay bale": "hoe",
    "sandstone": "pickaxe",
    "terracotta": "pickaxe",
    "gold block": "pickaxe",
    "iron block": "pickaxe",
    "diamond block": "pickaxe",
    "emerald block": "pickaxe",
    "lapis block": "pickaxe",
    "redstone block": "pickaxe",
    "glowstone block": "pickaxe",
    "magma": "pickaxe",
    "soul sand": "shovel",
    "sugar cane": "hoe",
    "tall grass": "hoe",
    "ungrown wheat plant":"hoe",
    "grown wheat plant":"hoe",
    "ungrown carrot plant":"hoe",
    "grown carrot plant":"hoe",
}
#WHAT BLOCKS DROP
drop_list ={
    "sugar cane": "sugar cane",
    "sapling": "sapling",
    "log": "log",
    "stone": "cobblestone",
    "grass": "dirt",
    "coal ore": "coal",
    "netherack": "netherack",
    "sand": "sand",
    "dirt": "dirt",
    "snow": "snowball",
    "cactus": "cactus",
    "iron ore": "raw iron",
    "copper ore": "raw copper",
    "diamond ore": "diamond",
    "gold ore": "raw gold",
    "emerald ore": "emerald",
    "lapis ore": "lapis",
    "redstone ore": "redstone",
    "nether gold ore": "gold nugget",
    "quartz ore": "quartz",
    "cobblestone": "cobblestone",
    "end stone": "end stone",
    "planks": "planks",
    "tall grass": "wheat seeds",
    "ungrown wheat plant":"wheat seeds",
    "ungrown carrot plant":"carrot seeds",
    "nether bricks":"nether bricks",
    "end bricks":"end bricks",
    "sand bricks":"sand bricks",
    "cobblestone bricks":"cobblestone bricks",
    "blackstone bricks":"blackstone bricks",
    "gold block":"gold block",
    "diamond block":"diamond block",
    "redstone block":"redstone block",
    "emerald block": "emerald block",
    "quartz block": "quartz block",
    "copper block": "copper block",
    "iron block": "iron block",
    "lapis block": "lapis block",
    "coal block": "coal block",
    "netherite block": "netherite block",
    "obsidian":"obsidian"
}
 #HEALTH LOST WHEN A BLOCK IS DAMAGED
hardness_list = {
            "sugar cane":100,
            "tall grass":100,
            "log": 30,
            "plank": 50,
            "leaves": 50,
            "cactus": 50,
            "snow": 50,
            "grass": 50,
            "dirt": 50,
            "sand": 50,
            "gravel": 50,
            "clay": 50,
            "moss block": 40,
            "coal ore": 30,
            "copper ore": 30,
            "iron ore": 25,
            "gold ore": 20,
            "diamond ore": 15,
            "emerald ore": 15,
            "ancient debris": 10,
            "redstone ore": 30,
            "stone": 40,
            "cobblestone": 40,
            "cobblestone bricks": 30,
            "nether bricks": 30,
            "obsidian": 10,
            "gold block": 20,
            "iron block": 25,
            "diamond block": 15,
            "emerald block": 15,
            "lapis block": 30,
            "redstone block": 30,
            "glowstone": 30,
            "hay bale": 50,
            "furnace": 30,
            "crafting table": 30,
            "chest": 30,
            "barrel": 30,
            "anvil": 15,
            "enchanting table": 15,
            "dispenser": 30,
            "end stone": 20,
            "netherack": 30,
            "lapis ore": 30,
            "nether gold ore": 25,
            "quartz ore": 30,
            "planks": 50,
            "ungrown wheat plant":100,
            "grown wheat plant":100,
            "ungrown carrot plant":100,
            "grown carrot plant":100,
            "netherite block":12,
}
# ITEMS THAT DO NOT STACK TOGETHER
unstackable_items = [
    "copper helmet",
    "copper chestplate",
    "copper leggings",
    "copper boots"
    "totem of undying",
    "mace",
    "elytra",
    "bow",
    "crossbow",
    "wooden sword",
    "stone sword",
    "iron sword",
    "gold sword",
    "diamond helmet",
    "iron helmet",
    "gold helmet",
    "leather helmet",
    "diamond chestplate",
    "iron chestplate",
    "gold chestplate",
    "leather chestplate",
    "diamond leggings",
    "iron leggings",
    "gold leggings",
    "leather leggings",
    "diamond boots",
    "iron boots",
    "gold boots",
    "leather boots",
    "flint and steel",
    "splash potion",
    "water bucket",
    "lava bucket",
    "milk bucket",
    "fishing rod",
    "cake",
    "pumpkin pie",
    "suspicious stew",
    "netherite pickaxe",
    "netherite axe",
    "netherite shovel",
    "netherite hoe",
    "netherite sword",
    "netherite helmet",
    "netherite chestplate",
    "netherite leggings",
    "netherite boots",
    "elytra",
    "wooden pickaxe",
    "stone pickaxe",
    "iron pickaxe",
    "golden pickaxe",
    "diamond pickaxe",
    "wooden axe",
    "stone axe",
    "iron axe",
    "golden axe",
    "diamond axe",
    "wooden shovel",
    "stone shovel",
    "iron shovel",
    "golden shovel",
    "diamond shovel",
    "wooden hoe",
    "stone hoe",
    "iron hoe",
    "golden hoe",
    "diamond hoe",
    "diamond sword",
    "potion",
    "wooden spear",
    "stone spear",
    "iron spear",
    "copper spear",
    "gold spear",
    "diamond spear",
    "netherite spear",
    "copper sword",
    "copper pickaxe",
    "copper axe",
    "copper shovel",
    "copper hoe",
    "bucket",
    "lava bucket"
    "water bucket",
    "charging bow",
    "charged bow",
    "charging crossbow",
    "charged crossbow",
]
# WHAT TO DROP IF DROPPED FROM PLAYER
drops={"charged bow":"bow","charging bow":"bow","charging crossbow":"crossbow","charged crossbow":"crossbow"}
# WHAT NAMES TO SHOW IF HELD
names={"charged bow":"bow","charging bow":"bow","charging crossbow":"crossbow","charged crossbow":"crossbow"}
# CAN GO THOROUGH
liquids=["water","lava"]
# WHAT TO PLACE OTHER THAN ITSELF
placed_items={"wheat seeds":"ungrown wheat plant","carrot seeds":"ungrown carrot plant"}
# ITEMS THAT DROP MORE THAN ONE DIFFERENT ITEM
wheat_drops=["wheat seeds","wheat"]
wheat_amount=[random.randint(1,3),random.randint(1,4)]
carrot_drops=["carrot seeds","carrot"]
carrot_amount=[random.randint(1,3),random.randint(1,4)]
multi_item_drops={"grown wheat plant":wheat_drops,"grown carrot plant":carrot_drops}
multi_item_amount = {"grown wheat plant": wheat_amount,"grown carrot plant":carrot_amount}
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
def get_held_item():
    return player_list[controlled_player_name].give_hotbar_slot_items(slot)
position=0
def update_position():
    global position
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
slot = 1
clock = pygame.time.Clock()

async def main():
    running = True
    while running:
        heart_list.empty()
        held_items.empty()
        hotbar_itemz.empty()
        players.empty()
        sprites.empty()
        drp_sprites.empty()
        hotbar.empty()
        hotbar_amount.empty()
        hotbar_top.empty()
        coords.empty()
        hotbar_top.add(held_item_text(slot))
        coords.add(coord_text())
        for a in range(1, 10):
            hotbar_amount.add(hotbar_text(a))
        for a in range(1, 11):
            heart_list.add(heart(controlled_player_name, a))
        for a in range(1, 9):
            heart_list.add(gold_heart(controlled_player_name, a))
        for a in range(1, 10):
            hotbar.add(hotbar_slot(a))
        for a in range(1, 10):
            hotbar_itemz.add(hotbar_item(a))
        held_items.add(held_item())
        for e in held_items:
            e.update_image(slot)
        for ae in hotbar_itemz:
            ae.change_image(player_list[controlled_player_name].give_hotbar_slot_items(ae.num()))
        controlled_player = player_list[controlled_player_name]
        update_position()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        for bl in all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])]:
            sprites.add(bl)
        does_fall = 1
        cactus_killer = 0
        lava_burner = 0
        water_lander = 0
        for i in all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])]:
            if is_collide(i.rect.x, player_list[controlled_player_name].rect.x, player_list[controlled_player_name].rect.y,
                          i.rect.y) and not i.is_air():
                does_fall = 0
            if is_collide(i.rect.x, player_list[controlled_player_name].rect.x, player_list[controlled_player_name].rect.y,
                          i.rect.y) and i.give_type() == "cactus":
                cactus_killer = 1
            if is_collide(i.rect.x, player_list[controlled_player_name].rect.x, player_list[controlled_player_name].rect.y,
                          i.rect.y) and i.give_type() == "lava":
                lava_burner = 1
            if is_collide(i.rect.x, player_list[controlled_player_name].rect.x, player_list[controlled_player_name].rect.y,
                          i.rect.y) and i.give_type() == "water":
                water_lander = 1
        if does_fall == 0:
            player_list[controlled_player_name].land(no_fall_damage=water_lander == 1)
        else:
            player_list[controlled_player_name].fall()
        if cactus_killer == 1:
            player_list[controlled_player_name].damage(7)
        if lava_burner == 1:
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
                    if NEGATIVE_BORDER < players_in_chunks[controlled_player_name]:
                        add_chunks(position)
                        add_chunks(position)
                        players_in_chunks[controlled_player_name] -= 1
                    else:
                        players_in_chunks[controlled_player_name] = POSITIVE_BORDER
                    player_list[controlled_player_name].goto((56 * BLOCK_WIDTH + SPACE_SIZE) / BLOCK_WIDTH,
                                                             player_list[controlled_player_name].y)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            jumper = 0
            for i in all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])]:
                if is_collide(i.rect.x, controlled_player.rect.x, controlled_player.rect.y, i.rect.y, 15,
                              15) and i.is_air():
                    jumper = 1
            if jumper == 1:
                if controlled_player.rect.x + controlled_player.speed < 56 * BLOCK_WIDTH + SPACE_SIZE:
                    player_list[controlled_player_name].right()
                else:
                    if players_in_chunks[controlled_player_name] < POSITIVE_BORDER:
                        add_chunks(position)
                        add_chunks(position)
                        players_in_chunks[controlled_player_name] += 1
                    else:
                        players_in_chunks[controlled_player_name] = NEGATIVE_BORDER
                    player_list[controlled_player_name].goto(SPACE_SIZE / BLOCK_WIDTH,
                                                             player_list[controlled_player_name].y)
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
        # SLOT MANAGEMENT
        reeee = -1
        if keys[pygame.K_z]:
            slot += -1
        if keys[pygame.K_x]:
            slot += 1
        if slot == 0:
            slot = 9
        if slot == 10:
            slot = 1
        if keys[pygame.K_1]:
            slot = 1
        if keys[pygame.K_2]:
            slot = 2
        if keys[pygame.K_3]:
            slot = 3
        if keys[pygame.K_4]:
            slot = 4
        if keys[pygame.K_5]:
            slot = 5
        if keys[pygame.K_6]:
            slot = 6
        if keys[pygame.K_7]:
            slot = 7
        if keys[pygame.K_8]:
            slot = 8
        if keys[pygame.K_9]:
            slot = 9
        for tr in hotbar:
            tr.update_slot(slot)
        destroyer = 0
        # DETECT DROPPED ITEM COLLISION
        for drp in dropped_items:
            reeee += 1
            drp_fall = 1
            for i in all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])]:
                if is_collide(i.rect.x, drp.rect.x, drp.rect.y, i.rect.y, DROP_WIDTH, DROP_WIDTH) and not i.is_air():
                    drp_fall = 0
                if is_collide(i.rect.x, drp.rect.x, drp.rect.y, i.rect.y) and i.give_type() == "cactus":
                    destroyer = 1
                if is_collide(i.rect.x, drp.rect.x, drp.rect.y, i.rect.y) and i.give_type() == "lava":
                    destroyer = 1
            if drp_fall == 1:
                drp.fall()
            drp.update_position()
            if drp.is_in_chunk(players_in_chunks[controlled_player_name]):
                if drp.is_in_dimension(players_in_dimension[controlled_player_name]):
                    drp_sprites.add(drp)
            if drp.should_despawn() or destroyer == 1:
                del dropped_items[reeee]
            if is_collide(player_list[controlled_player_name].rect.x, drp.rect.x, drp.rect.y,
                          player_list[controlled_player_name].rect.y) and drp.is_in_chunk(
                players_in_chunks[controlled_player_name]) and drp.is_in_dimension(
                players_in_dimension[controlled_player_name]):
                player_list[controlled_player_name].pick_up_item(drp.give_type())
                try:
                    del dropped_items[reeee]
                except IndexError:
                    pass
        for p in players:
            p.update_position()
        # DETECT CLICKS
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 or event.button==3:
                    mouse_x, mouse_y = event.pos
                    # LEFT CLICKS
                    if event.button == 1:
                        # Hotbar slot selection
                        for e in hotbar:
                            if is_collide(mouse_x, e.rect.x, mouse_y, e.rect.y, BLOCK_WIDTH * 1.5, BLOCK_HEIGHT * 1.5):
                                slot = e.get_number()
                        # Block breaking
                        player_rect = player_list[controlled_player_name].rect
                        for bl in all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])]:
                            if( not bl.is_air()) or bl.give_type() in immortal_air_blocks:
                                if is_collide(mouse_x, bl.rect.x, mouse_y, bl.rect.y, BLOCK_WIDTH, BLOCK_HEIGHT):
                                    if is_collide(player_list[controlled_player_name].rect.x, bl.rect.x,
                                                  player_list[controlled_player_name].rect.y, bl.rect.y, BLOCK_WIDTH * 6,
                                                  BLOCK_HEIGHT * 6):
                                        bl.weaken(4, "pickaxe",10000)
                                        break
                    #RIGHT CLICKS
                    elif event.button == 3:
                        for bl in all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])]:
                            if is_collide(mouse_x, bl.rect.x, mouse_y, bl.rect.y, BLOCK_WIDTH, BLOCK_HEIGHT):
                                if is_collide(player_list[controlled_player_name].rect.x, bl.rect.x,
                                              player_list[controlled_player_name].rect.y, bl.rect.y, BLOCK_WIDTH * 6,
                                              BLOCK_HEIGHT * 6) and bl.is_air() and bl not in immortal_air_blocks:
                                    if get_held_item() in block_image_list.keys() or  get_held_item() in block_color_list.keys() or get_held_item() in placed_items.keys():
                                        if bl.give_type() not in immortal_air_blocks:
                                            #PLACE HELD BLOCK
                                            try:
                                                bl.change_type(placed_items.get(get_held_item(),get_held_item()))
                                                player_list[controlled_player_name].remove_item(slot)
                                            except NoBlockError:
                                                pass
                                        break
                                    elif get_held_item()=="bucket":
                                        if bl.give_type()=="lava":
                                            player_list[controlled_player_name].remove_item(slot)
                                            player_list[controlled_player_name].put_in_slot(slot,"lava bucket")
                                            bl.change_type("air")
                                            break
                                        elif bl.give_type() == "water":
                                            player_list[controlled_player_name].remove_item(slot)
                                            player_list[controlled_player_name].put_in_slot(slot,"water bucket")
                                            bl.change_type("air")
                                            break
                                    elif get_held_item() == "water bucket":
                                        if bl.give_type()=="air":
                                            bl.change_type("water")
                                            player_list[controlled_player_name].remove_item(slot)
                                            player_list[controlled_player_name].put_in_slot(slot,"bucket")
                                            break
                                    elif get_held_item() == "lava bucket":
                                        if bl.give_type()=="air":
                                            bl.change_type("lava")
                                            player_list[controlled_player_name].remove_item(slot)
                                            player_list[controlled_player_name].put_in_slot(slot,"bucket")
                                            break
                            if is_collide(player_list[controlled_player_name].rect.x, bl.rect.x,
                                                                  player_list[controlled_player_name].rect.y, bl.rect.y, BLOCK_WIDTH * 6,
                                                                  BLOCK_HEIGHT * 6) and is_collide(mouse_x, bl.rect.x, mouse_y, bl.rect.y, BLOCK_WIDTH, BLOCK_HEIGHT):
                                                        if bl.give_type() == "water" and get_held_item() =="lava bucket":
                                                            bl.change_type("obsidian")
                                                            player_list[controlled_player_name].remove_item(slot)
                                                            player_list[controlled_player_name].put_in_slot(slot,"bucket")
                                                            break
                                                        elif bl.give_type() == "lava" and get_held_item() =="water bucket":
                                                            bl.change_type("obsidian")
                                                            player_list[controlled_player_name].remove_item(slot)
                                                            player_list[controlled_player_name].put_in_slot(slot,"bucket")
                                                            break
        # BLOCK REVIVING
        for bl in all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])]:
            bl.heal()
        # PLANT GROWING
        block_count=0
        for bl in all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])]:
            bl.grow(position,block_count)
            block_count += 1
        # PLAYER SUFFOCATING
        damager = 1
        for i in all_blocks[position][remove_minus_and_add_1(players_in_chunks[controlled_player_name])]:
            if is_collide(i.rect.x, controlled_player.rect.x, controlled_player.rect.y, i.rect.y, 15,
                          15) and i.is_air():
                damager = 0
        if damager == 1:
            player_list[controlled_player_name].damage(5)
        player_list[controlled_player_name].check_inventory()
        player_list[controlled_player_name].heal(1)
        # SCREEN DRAWING
        screen.fill("black")
        sprites.draw(screen)
        for hearts in heart_list:
            hearts.update_health()
        drp_sprites.draw(screen)
        players.draw(screen)
        held_items.draw(screen)
        hotbar.draw(screen)
        heart_list.draw(screen)
        hotbar_itemz.draw(screen)
        hotbar_top.draw(screen)
        coords.draw(screen)
        hotbar_amount.draw(screen)
        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(60)
await main()
