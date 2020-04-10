import tcod as libtcod
from draw_functions import *
from map_objects import *
from constants import *

# Global variables & defaults
init = True
able_to_click = True
drawX = 0
drawY = 0
mouse_char = 218
mouse_color = libtcod.white
draw_type = 0
current_char = 219
current_color = libtcod.white
highlighted_tool = (list(ui_elements.keys())[0][0], list(ui_elements.keys())[0][1])
highlighted_char = (86, 18)
highlighted_color = (list(color_menu.keys())[0][0], list(color_menu.keys())[0][1])


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


def change_draw_type(con, icon_char):
    global draw_type, current_char, mouse_char, mouse_color

    if icon_char == 218:
        draw_type = 0
        mouse_char = 218
        mouse_color = libtcod.white
        display_message(con, "Tool: Pointer", libtcod.white)
        print("Tool: Pointer")
    elif icon_char == 47:
        draw_type = 1
        mouse_char = 47
        mouse_color = current_color
        display_message(con, "Draw Type: Line", libtcod.white)
        print("Draw Type: Line")
    elif icon_char == 8:
        draw_type = 2
        mouse_char = 8
        mouse_color = current_color
        display_message(con, "Draw Type: Wall", libtcod.white)
        print("Draw Type: Wall")
    elif icon_char == 219:
        draw_type = 3
        mouse_char = 219
        mouse_color = current_color
        display_message(con, "Draw Type: Box", libtcod.white)
        print("Draw Type: Box")
    elif icon_char == 7:
        draw_type = 4
        mouse_char = current_char
        mouse_color = current_color
        display_message(con, "Draw Type: Char", libtcod.white)
        print("Draw Type: Char")
    elif icon_char == 88:
        draw_type = 5
        mouse_char = 88
        mouse_color = libtcod.red
        display_message(con, "Tool: Erase", libtcod.white)
        print("Tool: Erase")


def handle_mouse(con, mouse):
    global able_to_click, drawX, drawY, draw_type, current_char, mouse_char,\
        mouse_color, current_color, highlighted_tool, highlighted_char, highlighted_color, init

    mouseX = int(mouse.x/CELL_SIZE)
    mouseY = int(mouse.y/CELL_SIZE)

    draw_borders(con)
    # Functions to run on startup
    if init:
        refresh_tools(con, highlighted_tool, highlighted_char, highlighted_color)
        display_message(con, "Welcome", libtcod.white)
        init = False

    # checks if mouse is over a ui element
    for x, y in ui_elements:
        if mouseX == x and mouseY == y:
            char = ui_elements[(x, y)]
            if mouse.lbutton_pressed:
                if y < 10:
                    change_draw_type(con, char)
                    if (x, y) is not highlighted_tool:
                        highlight_ui(con, x, y, 249, libtcod.white)
                        highlighted_tool = (x, y)
                        refresh_tools(con, highlighted_tool, highlighted_char,
                                      highlighted_color)
                elif y > 10:
                    current_char = char
                    if (x, y) is not highlighted_char:
                        highlight_ui(con, x, y, 249, libtcod.white)
                        highlighted_char = (x, y)
                        refresh_tools(con, highlighted_tool, highlighted_char,
                                      highlighted_color)
                    if draw_type == 4:
                        mouse_char = char
            break

    # checks if mouse is over a color menu choice
    for x, y in color_menu:
        if mouseX == x and mouseY == y:
            char, color = color_menu[(x, y)]
            if mouse.lbutton_pressed:
                current_color = color
                if draw_type in (1, 2, 3, 4):
                    mouse_color = color
                if (x, y) is not highlighted_color:
                    highlight_ui(con, x, y, 249, libtcod.white)
                    highlighted_color = (x, y)
                    refresh_tools(con, highlighted_tool, highlighted_char,
                                  highlighted_color)

        # Big Buttons
        for element in button_menu.items():
            x, y = element[0]
            change_background(con, x, y, x + button_size[0],
                              y + button_size[1], libtcod.black)
            if element[0][0] <= mouseX <= element[0][0] + button_size[0] and \
               element[0][1] <= mouseY <= element[0][1] + button_size[1] and \
               element[1] == 'CLEAR':
                change_background(con, x, y, x + button_size[0],
                                  y + button_size[1], libtcod.darker_red)
                display_message(con, "Clear Canvas", libtcod.red)
                if mouse.lbutton:
                    erase_all_map_objects()
                    clear_canvas(con)
            if element[0][0] <= mouseX <= element[0][0] + button_size[0] and \
               element[0][1] <= mouseY <= element[0][1] + button_size[1] and \
               element[1] == 'EXPORT':
                display_message(con, "Export map", libtcod.white)
                change_background(con, x, y, x + button_size[0],
                                  y + button_size[1], libtcod.dark_amber)
                if mouse.lbutton:
                    export_map()
            if element[0][0] <= mouseX <= element[0][0] + button_size[0] and \
               element[0][1] <= mouseY <= element[0][1] + button_size[1] and \
               element[1] == 'IMPORT':
                change_background(con, x, y, x + button_size[0],
                                  y + button_size[1], libtcod.dark_amber)
                display_message(con, "Import map", libtcod.white)
                if mouse.lbutton:
                    import_map()

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
                draw_wall(con, mouseX, mouseY, drawX, drawY, libtcod.white)
            elif draw_type == 3:
                draw_box(con, mouseX, mouseY, drawX, drawY, current_char, libtcod.white)
            elif draw_type == 4:
                draw_char(con, mouseX, mouseY, current_char, current_color)
            elif draw_type == 5:
                erase_map_object(con, mouseX, mouseY)

    if mouse.lbutton_pressed:
        able_to_click = True
        if is_in_map_range(mouseX, mouseY):
            if draw_type == 1:
                draw_line_objects(mouseX, mouseY, drawX, drawY, 'line', current_char, current_color)
                draw_all_map_objects(con)
            elif draw_type == 2:
                draw_wall_objects(mouseX, mouseY, drawX, drawY, 'wall', current_color)
                draw_all_map_objects(con)
            elif draw_type == 3:
                draw_box_objects(mouseX, mouseY, drawX, drawY, 'box', current_char, current_color)
                draw_all_map_objects(con)
            elif draw_type == 4:
                draw_char_object(mouseX, mouseY, current_char, current_color)
                draw_all_map_objects(con)
            elif draw_type == 5:
                erase_map_object(con, mouseX, mouseY)
                draw_all_map_objects(con)

    if mouse.rbutton:
        erase_map_object(con, mouseX, mouseY)

    draw_mouse(con, mouseX, mouseY, mouse_char, mouse_color)
