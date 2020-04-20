import tcod as libtcod
from draw_functions import *
from map_objects import *
from constants import *

# Global variables & defaults
init = True
able_to_click = True
drawX = 0
mouseX = 0
mouseY = 0
drawY = 0
mouse_char = 218
mouse_color = libtcod.white
draw_type = 0
current_char = 219
current_attributes = "c"
current_color = libtcod.white
highlighted_tool = (list(tools_menu.keys())[0][0], list(tools_menu.keys())[0][1])
highlighted_char = (102, 12)  # Coords of default highlighted char
highlighted_color = (list(color_menu.keys())[0][0], list(color_menu.keys())[0][1])
hide_mouse = False


def handle_keys(con, key):
    global highlighted_tool, mouseX, mouseY
    """
    returns a dictionary depending on key inputted
    """

    # Press alt + enter to go into fullscreen
    if (key.vk == libtcod.KEY_ENTER and key.lalt) or (key.vk == libtcod.KEY_ENTER and key.ralt):
        return {'fullscreen': True}
    # Esc to exit
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    # Tab to print current mouse coords
    elif key.vk == libtcod.KEY_TAB:
        update_map()
        print("Mouse Position: ({}, {})".format(mouseX, mouseY))
    # Insert to edit a chars attributes
    elif key.vk == libtcod.KEY_INSERT:
        display_message(con, "Continue in console...", libtcod.red)
        edit_element_attributes(con, mouseX, mouseY)

    tool_changed = False
    # Binds numbers to tools based on coords in constants.py
    if key.vk == libtcod.KEY_1:
        # Pointer tool
        x = 4
        y = 6
        tool_changed = True
    elif key.vk == libtcod.KEY_2:
        # Single wall draw
        x = 7
        y = 6
        tool_changed = True
    elif key.vk == libtcod.KEY_3:
        # Double wall draw
        x = 10
        y = 6
        tool_changed = True
    elif key.vk == libtcod.KEY_4:
        # Hollow box draw
        x = 13
        y = 6
        tool_changed = True
    elif key.vk == libtcod.KEY_5:
        # Box draw
        x = 16
        y = 6
        tool_changed = True
    elif key.vk == libtcod.KEY_6:
        # Line draw
        x = 19
        y = 6
        tool_changed = True
    elif key.vk == libtcod.KEY_7:
        # Char draw
        x = 22
        y = 6
        tool_changed = True
    elif key.vk == libtcod.KEY_8:
        # Free draw
        x = 25
        y = 6
        tool_changed = True
    elif key.vk == libtcod.KEY_9:
        # Erase
        x = 28
        y = 6
        tool_changed = True

    # If tool was changed then switch to new tool
    if tool_changed:
        char = tools_menu[(x, y)]
        change_draw_type(con, char)
        highlighted_tool = (x, y)
        refresh_tools(con, highlighted_tool, highlighted_char, highlighted_color)

    return {}


def is_in_map_range(x, y):
    map_start_x, map_start_y = MAP_BOX[0]
    map_end_x, map_end_y = MAP_BOX[1]
    return map_start_x < x < map_end_x and \
        map_start_y < y < map_end_y


def is_in_picker_range(x, y):
    char_start_x, char_start_y = CHAR_MENU_BOX[0]
    char_end_x, char_end_y = CHAR_MENU_BOX[1]
    return char_start_x < x < char_end_x and \
        char_start_y < y < char_end_y


def change_draw_type(con, icon_char):
    global draw_type, current_char, mouse_char, mouse_color

    if icon_char == 218:
        draw_type = 0
        mouse_char = 218
        mouse_color = libtcod.white
        display_message(con, "Tool: Pointer", libtcod.white)
        print("Tool: Pointer")
    elif icon_char == 241:
        draw_type = 1
        mouse_char = 241
        mouse_color = current_color
        display_message(con, "Draw Type: Single Wall", libtcod.white)
        print("Draw Type: Single Wall")
    elif icon_char == 244:
        draw_type = 2
        mouse_char = 244
        mouse_color = current_color
        display_message(con, "Draw Type: Double Wall", libtcod.white)
        print("Draw Type: Double Wall")
    elif icon_char == 245:
        draw_type = 3
        mouse_char = 245
        mouse_color = current_color
        display_message(con, "Draw Type: Hollow Box", libtcod.white)
        print("Draw Type: Hollow Box")
    elif icon_char == 219:
        draw_type = 4
        mouse_char = 219
        mouse_color = current_color
        display_message(con, "Draw Type: Box", libtcod.white)
        print("Draw Type: Box")
    elif icon_char == 47:
        draw_type = 5
        mouse_char = 47
        mouse_color = current_color
        display_message(con, "Draw Type: Line", libtcod.white)
        print("Draw Type: Line")
    elif icon_char == 240:
        draw_type = 6
        mouse_char = current_char
        mouse_color = current_color
        display_message(con, "Draw Type: Char", libtcod.white)
        print("Draw Type: Char")
    elif icon_char == 83:
        draw_type = 7
        mouse_char = current_char
        mouse_color = current_color
        display_message(con, "Draw Type: Free Draw", libtcod.white)
        print("Draw Type: Free Draw")
    elif icon_char == 88:
        draw_type = 8
        mouse_char = 88
        mouse_color = libtcod.red
        display_message(con, "Tool: Erase", libtcod.red)
        print("Tool: Erase")


def handle_mouse(con, mouse):
    global able_to_click, drawX, drawY, draw_type, current_char, mouse_char, \
        mouse_color, current_color, highlighted_tool, highlighted_char, \
        highlighted_color, init, hide_mouse, mouseX, mouseY, current_attributes

    # Functions to run on startup
    if init:
        refresh_tools(con, highlighted_tool, highlighted_char,
                      highlighted_color)
        refresh_chars(con, highlighted_tool, highlighted_char,
                      highlighted_color)
        display_message(con, "Welcome", libtcod.white)
        init = False

    mouseX = int(mouse.x/CELL_SIZE)
    mouseY = int(mouse.y/CELL_SIZE)

    draw_borders(con)

    # checks if mouse is over a tool
    for tool_x, tool_y in tools_menu:
        if mouseX == tool_x and mouseY == tool_y:
            char = tools_menu[(tool_x, tool_y)]
            draw_char(con, tool_x, tool_y, char, libtcod.red)
            if mouse.lbutton_pressed:
                change_draw_type(con, char)
                if (tool_x, tool_y) is not highlighted_tool:
                    highlight_ui(con, tool_x, tool_y, 249, libtcod.white)
                    highlighted_tool = (tool_x, tool_y)
                    refresh_tools(con, highlighted_tool, highlighted_char,
                                  highlighted_color)
            break

    # checks if mouse is over a char
    for char_x, char_y in chars_menu:
        if mouseX == char_x and mouseY == char_y:
            char, attr = chars_menu[(char_x, char_y)]
            draw_char(con, char_x, char_y, char, libtcod.red)
            if mouse.lbutton_pressed:
                current_char = char
                current_attributes = attr
                if (char_x, char_y) is not highlighted_char:
                    highlight_ui(con, char_x, char_y, 249, libtcod.white)
                    highlighted_char = (char_x, char_y)
                    refresh_chars(con, highlighted_tool,
                                  highlighted_char,
                                  highlighted_color)
                if draw_type == 6 or draw_type == 7:
                    mouse_char = char
            break

    # checks if mouse is over a color menu choice
    for x, y in color_menu:
        if mouseX == x and mouseY == y:
            char, color = color_menu[(x, y)]
            if mouse.lbutton_pressed:
                current_color = color
                print(draw_type)
                if draw_type not in (0, 8):
                    mouse_color = color
                if (x, y) is not highlighted_color:
                    highlight_ui(con, x, y, 249, libtcod.white)
                    highlighted_color = (x, y)
                    refresh_chars(con, highlighted_tool, highlighted_char,
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
            if mouse.lbutton_pressed:
                erase_all_map_objects()
                clear_canvas(con)
                break
        elif element[0][0] <= mouseX <= element[0][0] + button_size[0] and \
                element[0][1] <= mouseY <= element[0][1] + button_size[1] and \
                element[1] == 'EXPORT':
            display_message(con, "Export map", libtcod.white)
            change_background(con, x, y, x + button_size[0],
                              y + button_size[1], libtcod.dark_amber)
            if mouse.lbutton_pressed:
                display_message(con, "Exporting...", libtcod.white)
                export_map()
                display_message(con, "Export Complete", libtcod.dark_green)
                break
        elif element[0][0] <= mouseX <= element[0][0] + button_size[0] and \
                element[0][1] <= mouseY <= element[0][1] + button_size[1] and \
                element[1] == 'IMPORT':
            change_background(con, x, y, x + button_size[0],
                              y + button_size[1], libtcod.dark_amber)
            display_message(con, "Import map", libtcod.white)
            if mouse.lbutton_pressed:
                import_map()
                break
        elif element[0][0] <= mouseX <= element[0][0] + button_size[0] and \
                element[0][1] <= mouseY <= element[0][1] + button_size[1] and \
                element[1] == 'UPDATE':
            change_background(con, x, y, x + button_size[0],
                              y + button_size[1], libtcod.dark_amber)
            display_message(con, "Update Map Attributes", libtcod.white)
            if mouse.lbutton_pressed:
                display_message(con, "Updating...", libtcod.white)
                update_map()
                display_message(con, "Attributes updated", libtcod.dark_green)
                break

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
                draw_wall(con, mouseX, mouseY, drawX, drawY, libtcod.white, "single")
                hide_mouse = True
            elif draw_type == 2:
                draw_wall(con, mouseX, mouseY, drawX, drawY, libtcod.white, "double")
                hide_mouse = True
            elif draw_type == 3:
                draw_hollow_box(con, mouseX, mouseY, drawX, drawY, current_char, current_color)
                hide_mouse = True
            elif draw_type == 4:
                draw_box(con, mouseX, mouseY, drawX, drawY, current_char, libtcod.white)
                hide_mouse = True
            elif draw_type == 5:
                draw_line(con, mouseX, mouseY, drawX, drawY, current_char, libtcod.white)
                hide_mouse = True
            elif draw_type == 6:
                draw_char(con, mouseX, mouseY, current_char, current_color)
                hide_mouse = False
            elif draw_type == 7:
                draw_char_object(mouseX, mouseY, current_attributes, current_char, current_color)
                hide_mouse = False
            elif draw_type == 8:
                erase_map_object(con, mouseX, mouseY)
                hide_mouse = False
    else:
        hide_mouse = False

    if mouse.lbutton_pressed:
        able_to_click = True
        if is_in_map_range(mouseX, mouseY):
            if draw_type == 0:
                display_map_object_properties(con, mouseX, mouseY)
            elif draw_type == 1:
                draw_wall_objects(mouseX, mouseY, drawX, drawY, current_attributes, current_color, "single")
                draw_all_map_objects(con)
            elif draw_type == 2:
                draw_wall_objects(mouseX, mouseY, drawX, drawY, current_attributes, current_color, "double")
                draw_all_map_objects(con)
            elif draw_type == 3:
                draw_hollow_box_objects(mouseX, mouseY, drawX, drawY, current_attributes, current_char, current_color)
                draw_all_map_objects(con)
            elif draw_type == 4:
                draw_box_objects(mouseX, mouseY, drawX, drawY, current_attributes, current_char, current_color)
                draw_all_map_objects(con)
            if draw_type == 5:
                draw_line_objects(mouseX, mouseY, drawX, drawY, current_attributes, current_char,current_color)
                draw_all_map_objects(con)
            elif draw_type == 6:
                draw_char_object(mouseX, mouseY,current_attributes, current_char, current_color)
                draw_all_map_objects(con)
            elif draw_type == 7:
                draw_all_map_objects(con)
            elif draw_type == 8:
                erase_map_object(con, mouseX, mouseY)
                draw_all_map_objects(con)

    if mouse.rbutton:
        erase_map_object(con, mouseX, mouseY)

    if not hide_mouse:
        draw_mouse(con, mouseX, mouseY, mouse_char, mouse_color)
