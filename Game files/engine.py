# from tutorial @
# http://rogueliketutorials.com/tutorials/tcod/part-1/ (parts 1-4)

import tcod as libtcod

from GamePlay.fighter import Fighter
from Objects.entity import Entity, get_blocking_entities_at_location
from Display.fov_functions import initialize_fov, recompute_fov
from Input.input_handlers import handle_keys
from Display.render_functions import clear_all, render_all
from Display.game_map import GameMap
from Objects.inventory import Inventory
from Display.render_functions import RenderOrder
from GamePlay.game_states import GameStates
from constants import *


def main():

    # variables for character visibility
    fov_algorithm = 0   # default algorithm for visibility range
    fov_light_walls = True  # determine if walls show up or not
    fov_radius = 8  # change this value to change visibility range

    # initialize inventory
    inventory = Inventory(10)

    player_char = 1
    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Entity(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2), player_char, libtcod.white, 'Player', blocks=True,
                    render_order=RenderOrder.ACTOR, inventory=inventory, fighter=fighter_component)
    entities = [player]

    libtcod.console_set_custom_font(FONT_FILE, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)

    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python game', False, vsync=False)

    con = libtcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT)

    game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
    game_map.load_random_map(player)
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

        render_all(con, entities, game_map, fov_map, fov_recompute, SCREEN_WIDTH, SCREEN_HEIGHT, libtcod.white,
                   game_state)

        fov_recompute = False

        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get('move')
        pickup = action.get('pickup')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        inventory = action.get('inventory')

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
                    print("There is a " + target.name + " here")
                else:
                    player.move(dx, dy)

                    fov_recompute = True
        # if player tries to pick something up
        elif pickup:
            for entity in entities:
                # if the entity is on the same tile as the player pick it up and remove it from the entity list
                if entity.item and entity.x == player.x and entity.y == player.y:
                    player.inventory.add_item(entity)
                    entities.remove(entity)

                    break
            # else dont pick it up and print to console
            else:
                print('Nothing to pickup')
        # if player presses the inventory key
        if inventory:
                prev_game_state = game_state
                game_state = GameStates.SHOW_INVENTORY

        if exit:
                if game_state == GameStates.SHOW_INVENTORY:
                    game_state = prev_game_state
                else:
                    return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()