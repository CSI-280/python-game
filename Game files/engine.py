# from tutorial @
# http://rogueliketutorials.com/tutorials/tcod/part-1/ (parts 1-4)

import tcod as libtcod

from Objects.entity import *
from GamePlay.fighter import Fighter
from GamePlay.death_functions import kill_monster, kill_player
from Display.fov_functions import initialize_fov, recompute_fov
from Input.input_handlers import handle_keys
from Display.render_functions import clear_all, render_all, RenderOrder, refresh_screen
from Display.game_map import *
from Objects.inventory import Inventory
from GamePlay.game_states import GameStates
from constants import *
from Display.menus import *


def main():

    # variables for character visibility
    fov_algorithm = 0   # default algorithm for visibility range
    fov_light_walls = True  # determine if walls show up or not
    fov_radius = 8  # change this value to change visibility range

    # initialize inventory
    inventory = Inventory(10)
    fighter_player = Fighter(hp=30, defense=2, power=5)
    player_char = 1
    fighter_component = Fighter(hp=30, defense=2, power=5)

    player = Entity(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2), player_char, libtcod.white, 'Player', blocks=True,
                    render_order=RenderOrder.ACTOR, inventory=inventory, fighter=fighter_component)
    entities = Entity.entities
    entities.append(player)

    libtcod.console_set_custom_font(FONT_FILE, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)

    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python game', False, vsync=False)

    bar_width = 20
    panel_height = 7
    panel_y = SCREEN_HEIGHT - panel_height

    con = libtcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT)
    panel = libtcod.console_new(SCREEN_WIDTH, panel_height)



    game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
    # pass in first and last map
    game_map.generate_map_list("beginning.json", "end.json")
    game_map.load_next_map(player, entities)
    # returns a tuple, (entrance, exit)
    exit_stairs = game_map.get_stairs()[1]
    entrance_stairs = game_map.get_stairs()[0]

    # game_map.make_map(max_rooms, room_min_size, room_max_size, MAP_WIDTH, MAP_HEIGHT, player, entities,
    #                  max_items_per_room)

    fov_recompute = True

    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()
    game_state = GameStates.PLAYERS_TURN
    prev_game_state = game_state

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius,
                          fov_light_walls, fov_algorithm)

        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, SCREEN_WIDTH, SCREEN_HEIGHT, bar_width, panel_height, panel_y, libtcod.white, game_state)

        fov_recompute = False

        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key, game_state)

        move = action.get('move')
        pickup = action.get('pickup')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        inventory = action.get('inventory')
        inventory_index = action.get('inventory_index')
        drop_inventory = action.get('drop_inventory')

        player_turn_results = []

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            # If some the destination is not blocked
            if not game_map.is_blocked(destination_x, destination_y):
                # Gets any entity that might be blocking the player
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                # If something is blocking hte player print to console, else moves the player
                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)

                    fov_recompute = True

                # set game state to enemies turn
                game_state = GameStates.ENEMY_TURN

        # if player tries to pick something up
        elif pickup:
            # look for exit stairs
            if player.x == exit_stairs[0] and player.y == exit_stairs[1]:
                # remove all entities from prior map
                entities = [player]
                # generate next map
                game_map.load_next_map(player, entities)
                # refresh fov
                fov_recompute = True
                fov_map = initialize_fov(game_map)
                # get new pos of exit_stairs and entrance_stairs
                exit_stairs = game_map.get_stairs()[1]
                entrance_stairs = game_map.get_stairs()[0]
                # refresh the screen to delete leftover characters
                refresh_screen(con, game_map)

            # look for entrance stairs
            if player.x == entrance_stairs[0] and player.y == entrance_stairs[1]:
                # remove all entities from prior map
                entities = [player]
                # generate next map
                game_map.load_previous_map(player, entities)
                # refresh fov
                fov_recompute = True
                fov_map = initialize_fov(game_map)
                # get new pos of exit_stairs and entrance_stairs
                exit_stairs = game_map.get_stairs()[1]
                entrance_stairs = game_map.get_stairs()[0]
                # refresh the screen to delete leftover characters
                refresh_screen(con, game_map)

            for entity in entities:
                # if the entity is on the same tile as the player pick it up and remove it from the entity list
                if entity.item and entity.x == player.x and entity.y == player.y:
                    if entity.name == "Health":
                        player.fighter.heal(5)
                    else:
                        player.inventory.add_item(entity)
                    entities.remove(entity)
                    game_map.reset_tile(entity.x, entity.y)
                    break
            # else dont pick it up and print to console
            else:
                print('Nothing to pickup')
        # if player presses the inventory key
        if inventory:
                prev_game_state = game_state
                game_state = GameStates.SHOW_INVENTORY

        if drop_inventory:
            prev_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        if inventory_index is not None and prev_game_state != GameStates.PLAYER_DEAD \
                and inventory_index < len(player.inventory.items):
            item = player.inventory.items[inventory_index]

            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))

        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                game_state = prev_game_state
            else:
                return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            item_dropped = player_turn_result.get('item_dropped')

            if message:
                print(message)

            if item_consumed:
                game_state = GameStates.ENEMY_TURN

            if item_dropped:
                entities.append(item_dropped)
                game_state = GameStates.ENEMY_TURN

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                print(message)

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map,
                                                             game_map,
                                                             entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            print(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            print(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                            break
            else:
                # set game state to players turn
                game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()
