
import tcod as libtcod
import map_objects

from constants import *


# bresenham taken from https://github.com/encukou/bresenham/blob/master/bresenham.py
# not my work
def bresenham(x0, y0, x1, y1):
    """Yield integer coordinates on the line from (x0, y0) to (x1, y1).
    Input coordinates should be integers.
    The result will contain both the start and the end point.
    """
    dx = x1 - x0
    dy = y1 - y0

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2*dy - dx
    y = 0

    for x in range(dx + 1):
        yield x0 + x*xx + y*yx, y0 + x*xy + y*yy
        if D >= 0:
            y += 1
            D -= 2*dx
        D += 2*dy


def draw_line(con, x1, y1, x2, y2, char, color):
    # char color
    libtcod.console_set_default_foreground(con, color)

    # list of points that make up a line
    point_list = list(bresenham(x1, y1, x2, y2))

    # draw for every point in the line
    for point in point_list:
        # draw single character
        libtcod.console_put_char(con, point[0], point[1], char, libtcod.BKGND_NONE)

    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)


def draw_line_objects(x1, y1, x2, y2, attr, char_number, color):
    point_list = list(bresenham(x1, y1, x2, y2))

    for point in point_list:
        new_object = map_objects.Object(attr, char_number, color)
        new_object.x = point[0] - OUTLINE_SIZE
        new_object.y = point[1] - OUTLINE_SIZE
        map_objects.objects.append(new_object)


def draw_box(con, x1, y1, x2, y2, char, color):

    # Drag down
    if y2 > y1:
        for y in range(y1, y2):
            draw_line(con, x1, y, x2, y, char, color)
    # Drag up
    elif y1 > y2:
        for y in range(y2, y1):
            draw_line(con, x1, y, x2, y, char, color)


def draw_box_objects(x1, y1, x2, y2, attr, char, color):

    # Drag down
    if y2 > y1:
        for y in range(y1, y2):
            draw_line_objects(x1, y, x2, y, attr, char, color)
    # Drag up
    elif y1 > y2:
        for y in range(y2, y1):
            draw_line_objects(x1, y, x2, y, attr, char, color)


def draw_hollow_box(con, x1, y1, x2, y2, char, color):

    # top
    draw_line(con, x1, y1, x2, y1, char, color)
    # right
    draw_line(con, x2, y1, x2, y2, char, color)
    # bottom
    draw_line(con, x2, y2, x1, y2, char, color)
    # left
    draw_line(con, x1, y2, x1, y1, char, color)


def draw_hollow_box_objects(x1, y1, x2, y2, attr, char, color):

    # top
    draw_line_objects(x1, y1, x2, y1, attr, char, color)
    # right
    draw_line_objects(x2, y1, x2, y2, attr, char, color)
    # bottom
    draw_line_objects(x2, y2, x1, y2, attr, char, color)
    # left
    draw_line_objects(x1, y2, x1, y1, attr, char, color)


def draw_wall(con, x1, y1, x2, y2, color, char_type):
    if char_type == "single":
        wall_type = (196, 179)
    elif char_type == "double":
        wall_type = (205, 186)

    # top
    draw_line(con, x1, y1, x2, y1, wall_type[0], color)
    # right
    draw_line(con, x2, y1, x2, y2, wall_type[1], color)
    # bottom
    draw_line(con, x2, y2, x1, y2, wall_type[0], color)
    # left
    draw_line(con, x1, y2, x1, y1, wall_type[1], color)

    if char_type == "single":
        corner_chars = [217, 192, 191, 218]
        # bottom right to top left
        if x1 < x2 and y1 < y2:
            corner_chars = [218, 191, 192, 217]
        # bottom left to top right
        if x1 > x2 and y1 < y2:
            corner_chars = [191, 218, 217, 192]
        # top right to bottom left
        if x1 < x2 and y1 > y2:
            corner_chars = [192, 217, 218, 191]
        # top left to bottom right
        if x1 >= x2 and y1 >= y2:
            corner_chars = [217, 192, 191, 218]

    if char_type == "double":
        corner_chars = [188, 200, 187, 201]
        # bottom right to top left
        if x1 < x2 and y1 < y2:
            corner_chars = [201, 187, 200, 188]
        # bottom left to top right
        if x1 > x2 and y1 < y2:
            corner_chars = [187, 201, 188, 200]
        # top right to bottom left
        if x1 < x2 and y1 > y2:
            corner_chars = [200, 188, 201, 187]
        # top left to bottom right
        if x1 >= x2 and y1 >= y2:
            corner_chars = [188, 200, 187, 201]

    # top left
    draw_char(con, x1, y1, corner_chars[0], color)
    # top right
    draw_char(con, x2, y1, corner_chars[1], color)
    # bottom left
    draw_char(con, x1, y2, corner_chars[2], color)
    # bottom right
    draw_char(con, x2, y2, corner_chars[3], color)


def draw_wall_objects(x1, y1, x2, y2, attr, color, char_type):
    if char_type == "single":
        wall_type = (196, 179)
    elif char_type == "double":
        wall_type = (205, 186)

    # top
    draw_line_objects(x1, y1, x2, y1, attr, wall_type[0], color)
    # right
    draw_line_objects(x2, y1, x2, y2, attr, wall_type[1], color)
    # bottom
    draw_line_objects(x2, y2, x1, y2, attr, wall_type[0], color)
    # left
    draw_line_objects(x1, y2, x1, y1, attr, wall_type[1], color)

    if char_type == "single":
        corner_chars = [217, 192, 191, 218]
        # bottom right to top left
        if x1 < x2 and y1 < y2:
            corner_chars = [218, 191, 192, 217]
        # bottom left to top right
        if x1 > x2 and y1 < y2:
            corner_chars = [191, 218, 217, 192]
        # top right to bottom left
        if x1 < x2 and y1 > y2:
            corner_chars = [192, 217, 218, 191]
        # top left to bottom right
        if x1 >= x2 and y1 >= y2:
            corner_chars = [217, 192, 191, 218]

    if char_type == "double":
        corner_chars = [188, 200, 187, 201]
        if x1 < x2 and y1 < y2:
            corner_chars = [201, 187, 200, 188]
        # bottom left to top right
        if x1 > x2 and y1 < y2:
            corner_chars = [187, 201, 188, 200]
        # top right to bottom left
        if x1 < x2 and y1 > y2:
            corner_chars = [200, 188, 201, 187]
        # top left to bottom right
        if x1 >= x2 and y1 >= y2:
            corner_chars = [188, 200, 187, 201]

    # top left
    draw_char_object(x1, y1, "c", corner_chars[0], color)
    # top right
    draw_char_object(x2, y1, "c", corner_chars[1], color)
    # bottom left
    draw_char_object(x1, y2, "c", corner_chars[2], color)
    # bottom right
    draw_char_object(x2, y2, "c", corner_chars[3], color)


def draw_char(con, x, y, char, color):
    # Color of printed char
    libtcod.console_set_default_foreground(con, color)
    libtcod.console_put_char(con, x, y, char, libtcod.BKGND_NONE)
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)


def draw_char_object(x, y, attr, char, color):
    new_object = map_objects.Object(attr, char, color)
    new_object.x = x - OUTLINE_SIZE
    new_object.y = y - OUTLINE_SIZE
    map_objects.objects.append(new_object)


def draw_word(con, x, y, word, color, max_len):
    # Color of letter
    libtcod.console_set_default_foreground(con, color)
    overflow = 0
    for letter in word:
        libtcod.console_put_char(con, x, y, letter, libtcod.BKGND_NONE)
        x += 1
        overflow += 1
        if overflow >= max_len:
            break

    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)


def draw_borders(con):
    draw_hollow_box(con, MAP_BOX_SIZE[0][0], MAP_BOX_SIZE[0][1],
              MAP_BOX_SIZE[1][0], MAP_BOX_SIZE[1][1], 219, libtcod.dark_amber)
    draw_hollow_box(con, PICKER_BOX_SIZE[0][0], PICKER_BOX_SIZE[0][1],
              PICKER_BOX_SIZE[1][0], PICKER_BOX_SIZE[1][1], 219, libtcod.dark_amber)
    draw_ui(con, None, None, None)


def draw_button(con, x, y, word):
    draw_wall(con, x, y, x+button_size[0], y+button_size[1], libtcod.white, "double")
    draw_word(con, x+2, y+1, word, libtcod.white, len(word))


def draw_ui(con, hl_tool, hl_char, hl_color):
    # X alignment for UI elements, Y is changed on element
    left_coord = 102
    right_coord = 126
    word_start = 112
    # Headers
    draw_word(con, word_start, 3, "TOOLS", libtcod.white, 5)
    draw_line(con, left_coord, 4, right_coord, 4, 205, libtcod.white)

    draw_word(con, word_start, 9, "CHARS", libtcod.white, 5)
    draw_line(con, left_coord, 10, right_coord, 10, 205, libtcod.white)

    draw_word(con, word_start - 1, 27, "COLORS", libtcod.white, 6)
    draw_line(con, left_coord, 28, right_coord, 28, 205, libtcod.white)

    draw_word(con, word_start - 1, 41, "ACTIONS", libtcod.white, 7)
    draw_line(con, left_coord, 42, right_coord, 42, 205, libtcod.white)

    # Tool menu
    for x, y in tools_menu:
        char = tools_menu[(x, y)]
        draw_char(con, x, y, char, libtcod.white)

    # Chars menu
    for x, y in chars_menu:
        char, attr = chars_menu[(x, y)]
        draw_char(con, x, y, char, libtcod.white)

    # Color menu
    for x, y in color_menu:
        char, color = color_menu[(x, y)]
        draw_char(con, x, y, char, color)

    if hl_tool:
        highlight_ui(con, hl_tool[0], hl_tool[1], 249, libtcod.white)
    if hl_char:
        highlight_ui(con, hl_char[0], hl_char[1], 249, libtcod.white)
    if hl_color:
        highlight_ui(con, hl_color[0], hl_color[1], 249, libtcod.white)

    draw_line(con, left_coord - 1, 52, right_coord + 1, 52, 219, libtcod.dark_amber)
    draw_char(con, 102, 54, '>', libtcod.white)

    # Action menu
    for x, y in button_menu:
        word = button_menu[x, y]
        draw_button(con, x, y, word)


def highlight_ui(con, x, y, char, color):

    # Draw a char in the 8 coords around a ui item
    draw_char(con, x + 1, y, char, color)
    draw_char(con, x - 1, y, char, color)
    draw_char(con, x, y + 1, char, color)
    draw_char(con, x, y - 1, char, color)
    draw_char(con, x, y + 1, char, color)

    draw_char(con, x + 1, y + 1, char, color)
    draw_char(con, x - 1, y - 1, char, color)
    draw_char(con, x + 1, y - 1, char, color)
    draw_char(con, x - 1, y + 1, char, color)


def change_background(con, x1, y1, x2, y2, color):
    # change background of square depending on coordinates
    for y in range(y1 + 1, y2):
        for x in range(x1 + 1, x2):
            libtcod.console_set_char_background(con, x, y, color)


def draw_all_map_objects(con):
    clear_canvas(con)
    for obj in map_objects.objects:
        libtcod.console_set_default_foreground(con, obj.get_color())
        libtcod.console_put_char(con,
                                 obj.x + OUTLINE_SIZE,
                                 obj.y + OUTLINE_SIZE,
                                 obj.get_char(),
                                 libtcod.BKGND_NONE)
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)


old_mouse_pos = [None, None]
old_mouse_char = None
old_mouse_char_color = None


def draw_mouse(con, x, y, mouse_char, color):
    global old_mouse_pos, old_mouse_char, old_mouse_char_color

    # re draw the char that the mouse was at previously
    if old_mouse_pos[0] is not None:
        libtcod.console_set_default_foreground(con, old_mouse_char_color)
        libtcod.console_put_char(con, old_mouse_pos[0], old_mouse_pos[1], old_mouse_char, libtcod.BKGND_NONE)

    # get old variables for next time this function is called
    old_mouse_pos[0] = x
    old_mouse_pos[1] = y

    if libtcod.console_get_char(con, x, y) != mouse_char:
        old_mouse_char = libtcod.console_get_char(con, x, y)
        old_mouse_char_color = libtcod.console_get_char_foreground(con, x, y)

    # draw where the mouse is now
    libtcod.console_set_default_foreground(con, color)
    libtcod.console_put_char(con, x, y, mouse_char, libtcod.BKGND_NONE)

    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)


def display_message(con, message, color):
    draw_word(con, 104, 54, " " * 24, libtcod.white, 24)
    draw_word(con, 104, 54, message, color, 24)


def clear_screen(con):
    for y in range(SCREEN_HEIGHT):
        for x in range(SCREEN_WIDTH):
            libtcod.console_put_char(con, x, y, ' ', libtcod.BKGND_NONE)


def clear_canvas(con):
    for y in range(OUTLINE_SIZE, MAP_HEIGHT + OUTLINE_SIZE):
        for x in range(OUTLINE_SIZE, MAP_WIDTH + OUTLINE_SIZE):
            libtcod.console_put_char(con, x, y, ' ', libtcod.BKGND_NONE)


def refresh_tools(con, hl_tool, hl_char, hl_color):
    for y in range(OUTLINE_SIZE, MAP_HEIGHT):
        for x in range(MAP_WIDTH + 6, SCREEN_WIDTH - 2):
            libtcod.console_put_char(con, x, y, ' ', libtcod.BKGND_NONE)
            libtcod.console_set_char_background(con, x, y, libtcod.black)
    draw_ui(con, hl_tool, hl_char, hl_color)
