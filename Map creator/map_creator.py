# some of this code is from http://rogueliketutorials.com/tutorials/tcod/part-1/

import tcod as libtcod
from input_handlers import handle_keys
from draw_functions import draw_borders

from constants import *

def main():
    # set the font (arial10x10.png is in project folder, can be changed)
    libtcod.console_set_custom_font('../arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # create the screen
    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Map Creator by Michael Leonard', False)

    # create a console
    con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

    # keyboard and mouse input variables
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # game loop
    while not libtcod.console_is_window_closed():
        # update key and mouse variables for event
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        mouseX = int(mouse.x/CELL_SIZE)
        mouseY = int(mouse.y/CELL_SIZE)

        # define coords for map and picker boxes
        map_box_size = ((1, 1), (MAP_WIDTH + 2, MAP_HEIGHT + 2))
        picker_box_size = ((MAP_WIDTH + 2 + 2, 1), (SCREEN_WIDTH - 2, SCREEN_HEIGHT - 2))
        
        draw_borders(con, map_box_size, picker_box_size)

        # temporary, add to input handler or another file that manages the mouse,
        # what's selected, etc.   ===============================================
        if mouseX > map_box_size[0][0] and mouseX < map_box_size[1][0] and \
           mouseY > map_box_size[0][1] and mouseY < map_box_size[1][1]:
            libtcod.console_set_default_foreground(con, libtcod.blue)
            libtcod.console_put_char(con, mouseX, mouseY, '#', libtcod.BKGND_NONE)
        libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

        if mouseX > picker_box_size[0][0] and mouseX < picker_box_size[1][0] and \
           mouseY > picker_box_size[0][1] and mouseY < picker_box_size[1][1]:
            libtcod.console_set_default_foreground(con, libtcod.green)
            libtcod.console_put_char(con, mouseX, mouseY, '$', libtcod.BKGND_NONE)
        libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
        # =======================================================================
        
        libtcod.console_flush()

        # check for keyboard input
        action = handle_keys(key)

        exit_game = action.get('exit')
        fullscreen = action.get('fullscreen')

        if fullscreen:
            # toggle fullscreen
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        
        if exit_game:
            return True
        


if __name__ == '__main__':
    main()
