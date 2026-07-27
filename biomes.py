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
