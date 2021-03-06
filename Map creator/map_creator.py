# some of this code is from http://rogueliketutorials.com/tutorials/tcod/part-1/

import tcod as libtcod
from input_handlers import handle_keys, handle_mouse
from draw_functions import *

from constants import *


def main():
    # Sets font to file path, this specifies the chars we are able to use
    libtcod.console_set_custom_font('../font_custom.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)

    # create the screen
    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Map Creator', False, vsync=False)

    # create a console
    con = libtcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT)

    # limit fps so the game doesn't take up 100% cpu
    libtcod.sys_set_fps(60)

    # don't show mouse
    libtcod.mouse_show_cursor(False)

    # keyboard and mouse input variables
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # game loop
    while not libtcod.console_is_window_closed():
        # update key and mouse variables for event
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        # draws the JSON map that's defined already
        draw_all_map_objects(con)

        # also draws borders, handles JSON map drawing
        handle_mouse(con, mouse)

        libtcod.console_flush()

        # check for keyboard input
        action = handle_keys(con, key)

        exit_game = action.get('exit')
        fullscreen = action.get('fullscreen')

        if fullscreen:
            # toggle fullscreen
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        if exit_game:
            return True


if __name__ == '__main__':
    main()
