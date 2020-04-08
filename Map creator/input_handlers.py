import tcod as libtcod
from draw_functions import *
from map_objects import *
from constants import *

# Global variables & defaults
able_to_click = True
drawX = 0
drawY = 0
mouse_char = 218
mouse_color = libtcod.white
draw_type = 0
current_char = 7
current_color = libtcod.white


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
    global draw_type, current_char, mouse_char, mouse_color

    if icon_char == 218:
        draw_type = 0
        mouse_char = 218
        mouse_color = libtcod.white
        print("Draw Type: Pointer")
    elif icon_char == 47:
        draw_type = 1
        mouse_char = 47
        mouse_color = current_color
        print("Draw Type: Line")
    elif icon_char == 8:
        draw_type = 2
        mouse_char = 8
        mouse_color = current_color
        print("Draw Type: Box")
    elif icon_char == 7:
        draw_type = 3
        mouse_char = current_char
        mouse_color = current_color
        print("Draw Type: Char")
    elif icon_char == 88:
        draw_type = 4
        mouse_char = 88
        mouse_color = libtcod.red
        print("Draw Type: Erase")


def handle_mouse(con, mouse):
    global able_to_click, drawX, drawY, draw_type, current_char, mouse_char, mouse_color, current_color

    mouseX = int(mouse.x/CELL_SIZE)
    mouseY = int(mouse.y/CELL_SIZE)

    draw_borders(con)

    # checks if mouse is over a ui element
    for x, y in ui_elements:
        if mouseX == x and mouseY == y:
            char = ui_elements[(x, y)]
            draw_char(con, x, y, char, libtcod.dark_red)
            if mouse.lbutton_pressed:
                if y < 10:
                    change_draw_type(char)
                elif y > 10:
                    current_char = char
                    if draw_type == 3:
                        mouse_char = char
            break
        # Clear canvas button
        if mouseX == 111 and mouseY == 2:
            if mouse.lbutton_pressed:
                erase_all_map_objects()
                clear_canvas(con)
                break

    # checks if mouse is over a color menu choice
    for x, y in color_menu:
        if mouseX == x and mouseY == y:
            char, color = color_menu[(x, y)]
            if mouse.lbutton_pressed:
                current_color = color
                if draw_type in (1, 2, 3):
                    mouse_color = color

    if mouse.lbutton and able_to_click and is_in_map_range(mouseX, mouseY):
        able_to_click = False
        drawX = mouseX
        drawY = mouseY

    if mouse.lbutton:
        # clear screen to update the line position and prevent leftover chars
        # when the mouse is moved
        draw_all_map_objects(con)
        if is_in_map_range(mouseX, mouseY):
            if draw_type == 1:
                draw_line(con, mouseX, mouseY, drawX, drawY, current_char, libtcod.white)
            elif draw_type == 2:
                draw_box(con, mouseX, mouseY, drawX, drawY, 206, libtcod.white)
            elif draw_type == 3:
                draw_char(con, mouseX, mouseY, current_char, current_color)
            elif draw_type == 4:
                erase_map_object(con, mouseX, mouseY)

    if mouse.lbutton_pressed:
        able_to_click = True
        if is_in_map_range(mouseX, mouseY):
            if draw_type == 1:
                draw_line_objects(mouseX, mouseY, drawX, drawY, 'line', current_char,
                                  current_color)
                draw_all_map_objects(con)
            if draw_type == 2:
                draw_box_objects(mouseX, mouseY, drawX, drawY, 'box',
                                 current_color)
                draw_all_map_objects(con)
            elif draw_type == 3:
                draw_char_object(mouseX, mouseY, current_char, current_color)
                draw_all_map_objects(con)
            elif draw_type == 4:
                erase_map_object(con, mouseX, mouseY)
                draw_all_map_objects(con)

    if mouse.rbutton_pressed:
        # print(map_objects.objects, end='\n\n')
        print(mouseX, ", ", mouseY)

    draw_mouse(con, mouseX, mouseY, mouse_char, mouse_color)
