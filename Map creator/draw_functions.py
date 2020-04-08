
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


def draw_line_objects(x1, y1, x2, y2, name, char_number, color):
    point_list = list(bresenham(x1, y1, x2, y2))

    for point in point_list:
        new_object = map_objects.Object(name, char_number, color)
        new_object.x = point[0] - OUTLINE_SIZE
        new_object.y = point[1] - OUTLINE_SIZE
        map_objects.objects.append(new_object)


def draw_box(con, x1, y1, x2, y2, char, color):
    # top
    draw_line(con, x1, y1, x2, y1, char, color)
    # right
    draw_line(con, x2, y1, x2, y2, char, color)
    # bottom
    draw_line(con, x2, y2, x1, y2, char, color)
    # left
    draw_line(con, x1, y2, x1, y1, char, color)


def draw_box_objects(x1, y1, x2, y2, name, color):
    # top
    draw_line_objects(x1, y1, x2, y1, name, 205, color)
    # right
    draw_line_objects(x2, y1, x2, y2, name, 186, color)
    # bottom
    draw_line_objects(x2, y2, x1, y2, name, 205, color)
    # left
    draw_line_objects(x1, y2, x1, y1, name, 186, color)

    # botton right to top left
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
    draw_char_object(x1, y1, 15, color)
    draw_char_object(x1, y1, corner_chars[0], color)
    # top right
    draw_char_object(x2, y1, 15, color)
    draw_char_object(x2, y1, corner_chars[1], color)
    # bottom left
    draw_char_object(x1, y2, 15, color)
    draw_char_object(x1, y2, corner_chars[2], color)
    # bottom right
    draw_char_object(x2, y2, 15, color)
    draw_char_object(x2, y2, corner_chars[3], color)


def draw_char(con, x, y, char, color):
    # Color of printed char
    libtcod.console_set_default_foreground(con, color)
    libtcod.console_put_char(con, x, y, char, libtcod.BKGND_NONE)
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)


def draw_char_object(x, y, char, color):
    new_object = map_objects.Object("point", char, color)
    new_object.x = x - OUTLINE_SIZE
    new_object.y = y - OUTLINE_SIZE
    map_objects.objects.append(new_object)


def draw_word(con, x, y, word, color):
    # Color of letter
    libtcod.console_set_default_foreground(con, color)
    for letter in word:
        libtcod.console_put_char(con, x, y, letter, libtcod.BKGND_NONE)
        x += 1

    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)


def draw_borders(con):
    draw_box(con, MAP_BOX_SIZE[0][0], MAP_BOX_SIZE[0][1],
                   MAP_BOX_SIZE[1][0], MAP_BOX_SIZE[1][1], 219, libtcod.dark_amber)
    draw_box(con, PICKER_BOX_SIZE[0][0], PICKER_BOX_SIZE[0][1],
                  PICKER_BOX_SIZE[1][0], PICKER_BOX_SIZE[1][1], 219, libtcod.dark_amber)
    draw_ui(con)


def draw_ui(con):
    draw_char(con, 111, 2, 88, libtcod.red)

    draw_word(con, 95, 3, "TOOLS", libtcod.white)
    draw_line(con, 86, 4, 110, 4, 205, libtcod.white)

    # Loop through and print contents of constant ui dictionary
    for x, y in ui_elements:
        char = ui_elements[(x, y)]
        draw_char(con, x, y, char, libtcod.white)

    draw_word(con, 95, 9, "CHARS", libtcod.white)
    draw_line(con, 86, 10, 110, 10, 205, libtcod.white)


def draw_all_map_objects(con):
    clear_canvas(con)
    for obj in map_objects.objects:
        libtcod.console_set_default_foreground(con, obj.get_color())
        libtcod.console_put_char(con,
                                 obj.x + OUTLINE_SIZE,
                                 obj.y + OUTLINE_SIZE,
                                 obj.get_char(),
                                 libtcod.BKGND_NONE)
    map_objects.remove_duplicate_objects()
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

old_mouse_pos = [None, None]
old_mouse_char = None
old_mouse_char_color = None


def draw_mouse(con, x, y, mouse_char):
    global old_mouse_pos, old_mouse_char, old_mouse_char_color
    # TODO, make this a global variable, fix instances of this global variable
    # in input_handlers

    # re draw the char that the mouse was at previously
    if old_mouse_pos[0] != None:
        libtcod.console_set_default_foreground(con, old_mouse_char_color)
        libtcod.console_put_char(con, old_mouse_pos[0], old_mouse_pos[1], old_mouse_char, libtcod.BKGND_NONE)

    # get old variables for next time this function is called
    old_mouse_pos[0] = x
    old_mouse_pos[1] = y

    if libtcod.console_get_char(con, x, y) != mouse_char:
        old_mouse_char = libtcod.console_get_char(con, x, y)
        old_mouse_char_color = libtcod.console_get_char_foreground(con, x, y)

    # draw where the mouse is now
    libtcod.console_set_default_foreground(con, libtcod.white)
    libtcod.console_put_char(con, x, y, mouse_char, libtcod.BKGND_NONE)

    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)


def clear_screen(con):
    for y in range(SCREEN_HEIGHT):
        for x in range(SCREEN_WIDTH):
            libtcod.console_put_char(con, x, y, ' ', libtcod.BKGND_NONE)


def clear_canvas(con):
    for y in range(OUTLINE_SIZE, MAP_HEIGHT + OUTLINE_SIZE):
        for x in range(OUTLINE_SIZE, MAP_WIDTH+ OUTLINE_SIZE):
            libtcod.console_put_char(con, x, y, ' ', libtcod.BKGND_NONE)
