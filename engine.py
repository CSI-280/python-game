# this code is from http://rogueliketutorials.com/tutorials/tcod/part-1/

import tcod as libtcod


def main():
    screen_width = 80
    screen_height = 50

    # set the font (arial10x10.png is in project folder, can be changed)
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # create the screen
    libtcod.console_init_root(screen_width, screen_height, 'title', False)

    # game loop
    while not libtcod.console_is_window_closed():
        # set the color for the @ symbol
        libtcod.console_set_default_foreground(0, libtcod.white)

        # arg 1: console we're printing to
        # arg 2: x coordinate
        # arg 3: y coordinate
        # arg 4: symbol to print
        # arg 5: background (set to none)
        libtcod.console_put_char(0, 1, 1, '@', libtcod.BKGND_NONE)
        libtcod.console_flush()

        # check for keyboard input
        key = libtcod.console_check_for_keypress()

        # if escape is pressed, quit game loop
        if key.vk == libtcod.KEY_ESCAPE:
            return True


if __name__ == '__main__':
    main()
