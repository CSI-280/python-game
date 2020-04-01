import tcod as libtcod
from draw_functions import *
import map_objects

from constants import *

def handle_keys(key):
    """
    returns a dictionary depending on key inputted
    """
    # press alt + enter to go into fullscreen
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    return {}



def is_in_map_range(x, y):
    return x > MAP_BOX_SIZE[0][0] and x < MAP_BOX_SIZE[1][0] and \
       y > MAP_BOX_SIZE[0][1] and y < MAP_BOX_SIZE[1][1]

def is_in_picker_range(x, y):
    return x > PICKER_BOX_SIZE[0][0] and x < PICKER_BOX_SIZE[1][0] and \
       y > PICKER_BOX_SIZE[0][1] and y < PICKER_BOX_SIZE[1][1]

able_to_click = True
drawX = 0
drawY = 0

draw_type = 0

def handle_mouse(con, mouse):
    global able_to_click, drawX, drawY, draw_type
    
    mouseX = int(mouse.x/CELL_SIZE)
    mouseY = int(mouse.y/CELL_SIZE)

    draw_borders(con)

    if is_in_map_range(mouseX, mouseY):
        libtcod.console_set_default_foreground(con, libtcod.white)
        libtcod.console_put_char(con, mouseX, mouseY, 218, libtcod.BKGND_NONE)

    if is_in_picker_range(mouseX, mouseY):
        libtcod.console_set_default_foreground(con, libtcod.white)
        libtcod.console_put_char(con, mouseX, mouseY, 218, libtcod.BKGND_NONE)

    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

   
    
    if mouse.lbutton and able_to_click and is_in_map_range(mouseX, mouseY):
        able_to_click = False
        drawX = mouseX
        drawY = mouseY

    if mouse.lbutton:
        if is_in_map_range(mouseX, mouseY):
            if draw_type == 0:
                draw_line(con, mouseX, mouseY, drawX, drawY, 186, libtcod.sepia)
            elif draw_type == 1:
                draw_box(con, mouseX, mouseY, drawX, drawY, 186, libtcod.sepia)

    if mouse.lbutton_pressed:
        able_to_click = True
        if is_in_map_range(mouseX, mouseY):
            if draw_type == 0:
                draw_line_objects(mouseX, mouseY, drawX, drawY, 'path', 186,
                                  libtcod.light_purple)
            if draw_type == 1:
                draw_box_objects(mouseX, mouseY, drawX, drawY, 'wall', 35,
                                 libtcod.light_cyan)

    if mouse.wheel_up or mouse.wheel_down:
        if draw_type == 0:
            print('Box drawing')
            draw_type = 1
        elif draw_type == 1:
            print('Line drawing')
            draw_type = 0

    if mouse.rbutton_pressed:
        print(map_objects.objects, end='\n\n')
        



    

