from paper_mc_classes import *
slot=1
running=True
while running:
    for i in heart_list:
        heart_list.remove(i)
    for u in held_items:
        held_items.remove(u)
    for e in hotbar_itemz:
        hotbar_itemz.remove(e)
    for f in players:
        players.remove(f)
    for r in sprites:
        sprites.remove(r)
    for w in drp_sprites:
        drp_sprites.remove(w)
    for i in hotbar:
        hotbar.remove(i)
    for r in hotbar_amount:
        hotbar_amount.remove(r)
    for a in range(1,10):
        hotbar_amount.add(hotbar_text(a))
    for a in range(1, 11):
        heart_list.add(heart(controlled_player_name, a))
    for a in range(1, 9):
        heart_list.add(gold_heart(controlled_player_name, a))
    for a in range(1, 10):
        hotbar.add(hotbar_slot(a))
    for a in range(1,10):
        hotbar_itemz.add(hotbar_item(a))
    held_items.add(held_item())
    for e in held_items:
        e.update_image(slot-1)
    for ae in hotbar_itemz:
        ae.change_image(player_list[controlled_player_name].give_hotbar_slot_items(ae.num()))
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
    lava_burner = 0
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
    if does_fall == 1:
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
                if -2000 < players_in_chunks[controlled_player_name] < 1999:
                    add_chunks(position)
                    add_chunks(position)
                    players_in_chunks[controlled_player_name] -= 1
                else:
                    players_in_chunks[controlled_player_name] = 1999
                player_list[controlled_player_name].goto((56 * BLOCK_WIDTH + SPACE_SIZE) / BLOCK_WIDTH,
                                                         player_list[controlled_player_name].y )
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
                if -2000 < players_in_chunks[controlled_player_name] < 1999:
                    add_chunks(position)
                    add_chunks(position)
                    players_in_chunks[controlled_player_name] += 1
                else:
                    players_in_chunks[controlled_player_name] = -2000
                player_list[controlled_player_name].goto(SPACE_SIZE/BLOCK_WIDTH,
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
        if drp.is_in_chunk(players_in_chunks[controlled_player_name]):
            if drp.is_in_dimension(players_in_dimension[controlled_player_name]):
                drp_sprites.add(drp)
        if drop.should_despawn(drp) or destroyer == 1:
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
            if event.button == 1:
                mouse_x,mouse_y=event.pos
                for e in hotbar:
                    if is_collide(mouse_x,e.rect.x,mouse_y,e.rect.y,BLOCK_WIDTH*1.5,BLOCK_HEIGHT*1.5):
                        slot=e.get_number()
    player_list[controlled_player_name].check_inventory()
    player_list[controlled_player_name].heal(1)
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
    hotbar_amount.draw(screen)
    pygame.display.flip()
pygame.quit()
