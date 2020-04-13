# from tutorial @
# http://rogueliketutorials.com/tutorials/tcod/part-1/ (parts 1-4)

import tcod as libtcod

from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from input_handlers import handle_keys
from render_functions import clear_all, render_all
from map_objects.game_map import GameMap
from character.inventory import Inventory
from render_functions import RenderOrder


def main():

    # variables for screen size
    screen_width = 80
    screen_height = 50

    # variables to determine map generation within the screen
    map_width = 80
    map_height = 50

    # variables for number of rooms and the sizes they can be
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    # variables for character visibility
    fov_algorithm = 0   # default algorithm for visibility range
    fov_light_walls = True  # determine if walls show up or not
    fov_radius = 8  # change this value to change visibility range

    # set colors for floors and walls
    colors = {
        'dark_wall': libtcod.Color(75, 75, 75),
        'dark_ground': libtcod.Color(125, 125, 125),
        'light_wall': libtcod.Color(180, 200, 200),
        'light_ground': libtcod.Color(220, 240, 240)
    }

    # initialize inventory
    inventory = Inventory(10)

    player = Entity(0, 0, '@', libtcod.dark_green, 'Player', blocks=True,
                    render_order=RenderOrder.ACTOR, inventory=inventory)
    entities = [player]

    # set max enemies per room
    max_monsters_per_room = 3
    # set max items per room
    max_items_per_room = 2

    libtcod.console_set_custom_font('font_custom.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)

    libtcod.console_init_root(screen_width, screen_height, 'python game', False, vsync=False)

    con = libtcod.console_new(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities,
                      max_monsters_per_room, max_items_per_room )

    fov_recompute = True

    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius,
                          fov_light_walls, fov_algorithm)

        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)

        fov_recompute = False

        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get('move')
        pickup = action.get('pickup')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

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
                    # change fov
                    fov_recompute = True
                    # set turn to entity's turn
                    game_state = GameStates.ENEMY_TURN

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

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity != player:
                    print(
                        'The ' + entity.name + ' ponders the meaning of its existence.')

            # set turn back to player's turn
            game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()
