# from tutorial @
# http://rogueliketutorials.com/tutorials/tcod/part-1/ (parts 1-4)

import tcod as libtcod

from entity import Entity
from fov_functions import initialize_fov, recompute_fov
from input_handlers import handle_keys
from render_functions import clear_all, render_all
from map_objects.game_map import GameMap
from character.inventory import Inventory


def main():
    inventory = Inventory()

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

    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.dark_green)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.dark_red)
    entities = [npc, player]

    libtcod.console_set_custom_font('font_custom.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)

    libtcod.console_init_root(screen_width, screen_height, 'python game', False, vsync=False)

    con = libtcod.console.Console(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player)

    fov_recompute = True

    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

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
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)

                fov_recompute = True

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()