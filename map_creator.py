# this code is from http://rogueliketutorials.com/tutorials/tcod/part-1/

import tcod as libtcod
import time as time

SCREEN_WIDTH = 16*5
SCREEN_HEIGHT = 9*5


def main():
    # set the font (arial10x10.png is in project folder, can be changed)
    libtcod.console_set_custom_font('arial10x10.png', \
                                    libtcod.FONT_TYPE_GREYSCALE | \
                                    libtcod.FONT_LAYOUT_TCOD)

    # create the screen
    libtcod.console_init_root(SCREEN_WIDTH, \
                              SCREEN_HEIGHT, \
                              'Map Creator by Michael Leonard', \
                              False)

    # don't show mouse
    libtcod.mouse_show_cursor(False)

    # game loop
    while not libtcod.console_is_window_closed():
        # set the color for the symbols
        libtcod.console_set_default_foreground(0, libtcod.red)

        

        # check for keyboard input
        key = libtcod.console_check_for_keypress()

        libtcod.console_put_char(0, \
                                 int(libtcod.mouse_get_status().x / 10), \
                                 int(libtcod.mouse_get_status().y / 10), \
                                 '#', \
                                 libtcod.BKGND_NONE)

        libtcod.console_flush()

        libtcod.console_put_char(0, \
                                 int(libtcod.mouse_get_status().x / 10), \
                                 int(libtcod.mouse_get_status().y / 10), \
                                 ' ', \
                                 libtcod.BKGND_NONE)
        

        # if escape is pressed, quit game loop
        if key.vk == libtcod.KEY_ESCAPE:
            return True


if __name__ == '__main__':
    main()
