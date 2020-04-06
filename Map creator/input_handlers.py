import tcod as libtcod
from draw_functions import *
import map_objects

from constants import *

# Global variables
able_to_click = True
drawX = 0
drawY = 0

draw_type = 0
current_char = 0

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

def change_draw_type(icon_char):
    global draw_type, current_char

    if icon_char == 47:
        draw_type = 0
        print("Draw Type: Line")
    elif icon_char == 8:
        draw_type = 1
        print("Draw Type: Box")
    elif icon_char == 250:
        draw_type = 2
        print("Draw Type: Char")
        current_char = 250



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

    # checks if mouse is over a ui element
    for x, y in ui_elements:
        if mouseX == x and mouseY == y:
            char = ui_elements[(x, y)]
            draw_char(con, x, y, char, libtcod.yellow)
            if mouse.lbutton_pressed:
                change_draw_type(char)
            break
    
    if mouse.lbutton and able_to_click and is_in_map_range(mouseX, mouseY):
        able_to_click = False
        drawX = mouseX
        drawY = mouseY

    if mouse.lbutton:
        if is_in_map_range(mouseX, mouseY):
            if draw_type == 0:
                draw_line(con, mouseX, mouseY, drawX, drawY, 176, libtcod.sepia)
            elif draw_type == 1:
                draw_box(con, mouseX, mouseY, drawX, drawY, 206, libtcod.sepia)
            elif draw_type == 2:
                draw_char(con, mouseX, mouseY, current_char, libtcod. white)

    if mouse.lbutton_pressed:
        able_to_click = True
        if is_in_map_range(mouseX, mouseY):
            if draw_type == 0:
                draw_line_objects(mouseX, mouseY, drawX, drawY, 'path', 176,
                                  libtcod.light_purple)
            if draw_type == 1:
                draw_box_objects(mouseX, mouseY, drawX, drawY, 'wall',
                                 libtcod.light_cyan)
            elif draw_type == 2:
                draw_char_object(con, mouseX, mouseY, current_char, libtcod. white)

    if mouse.wheel_up or mouse.wheel_down:
        if draw_type == 0:
            print('Draw Mode: Box')
            draw_type = 1
        elif draw_type == 1:
            print('Draw Mode: Straight Line')
            draw_type = 0


    if mouse.rbutton_pressed:
        # print(map_objects.objects, end='\n\n')
        print(mouseX, ", ", mouseY)
        



    

