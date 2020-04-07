import tcod as libtcod
from draw_functions import *
import map_objects

from constants import *

# Global variables
able_to_click = True
drawX = 0
drawY = 0
mouse_char = 218
draw_type = 0
current_char = 0


def handle_keys(key):
    """
    returns a dictionary depending on key inputted
    """
    # press alt + enter to go into fullscreen
    if (key.vk == libtcod.KEY_ENTER and key.lalt) or (key.vk == libtcod.KEY_ENTER and key.ralt):
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    return {}


def is_in_map_range(x, y):
    return MAP_BOX_SIZE[0][0] < x < MAP_BOX_SIZE[1][0] and \
           MAP_BOX_SIZE[0][1] < y < MAP_BOX_SIZE[1][1]


def is_in_picker_range(x, y):
    return PICKER_BOX_SIZE[0][0] < x < PICKER_BOX_SIZE[1][0] and \
           PICKER_BOX_SIZE[0][1] < y < PICKER_BOX_SIZE[1][1]


def change_draw_type(icon_char):
    global draw_type, current_char, mouse_char

    if icon_char == 47:
        draw_type = 0
        mouse_char = 218
        print("Draw Type: Line")
    elif icon_char == 8:
        draw_type = 1
        mouse_char = 218
        print("Draw Type: Box")
    elif icon_char == 250:
        draw_type = 2
        mouse_char = 218
        print("Draw Type: Char")
        current_char = 250
    elif icon_char == 88:
        draw_type = 3
        mouse_char = 88
        print("Draw Type: Erase")


def handle_mouse(con, mouse):
    global able_to_click, drawX, drawY, draw_type, current_char, mouse_char

    mouseX = int(mouse.x/CELL_SIZE)
    mouseY = int(mouse.y/CELL_SIZE)

    draw_borders(con)

    # checks if mouse is over a ui element
    for x, y in ui_elements:
        if mouseX == x and mouseY == y:
            char = ui_elements[(x, y)]
            draw_char(con, x, y, char, libtcod.dark_red)
            if mouse.lbutton_pressed:
                change_draw_type(char)
            break

    # checks if mouse is over a ui char
    char_x = CHAR_X_START
    char_y = CHAR_Y_START
    if mouseX == char_x and mouseY == char_y:
        draw_char()
        if mouse.lbutton_pressed:
            current_char = 1

    if mouse.lbutton and able_to_click and is_in_map_range(mouseX, mouseY):
        able_to_click = False
        drawX = mouseX
        drawY = mouseY

    if mouse.lbutton:
        # clear screen to update the line position and prevent leftover chars
        # when the mouse is moved

        #TODO: fix this, at the moment it's very laggy
        clear_screen(con)
        draw_all_map_objects(con)
        draw_borders(con)
        if is_in_map_range(mouseX, mouseY):
            if draw_type == 0:
                draw_line(con, mouseX, mouseY, drawX, drawY, 176, libtcod.sepia)
            elif draw_type == 1:
                draw_box(con, mouseX, mouseY, drawX, drawY, 206, libtcod.sepia)
            elif draw_type == 2:
                draw_char(con, mouseX, mouseY, current_char, libtcod. white)
            elif draw_type == 3:
                draw_char_object(con, mouseX, mouseY, 0, libtcod.black)

    if mouse.lbutton_pressed:
        able_to_click = True
        if is_in_map_range(mouseX, mouseY):
            if draw_type == 0:
                draw_line_objects(mouseX, mouseY, drawX, drawY, 'path', 176,
                                  libtcod.light_sepia)
            if draw_type == 1:
                draw_box_objects(mouseX, mouseY, drawX, drawY, 'wall',
                                 libtcod.white)
            elif draw_type == 2:
                draw_char_object(con, mouseX, mouseY, current_char, libtcod.BKGND_NONEe)

    if mouse.wheel_up or mouse.wheel_down:
        if draw_type == 0:
            print('Draw Mode: Box')
            draw_type = 1
        elif draw_type == 1:
            print('Draw Mode: Line')
            draw_type = 0

    if mouse.rbutton_pressed:
        # print(map_objects.objects, end='\n\n')
        print(mouseX, ", ", mouseY)


    draw_mouse(con, mouseX, mouseY)
