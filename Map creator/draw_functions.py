
import tcod as libtcod

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


def draw_line(con, x1, y1, x2, y2):
    # char color
    libtcod.console_set_default_foreground(con, libtcod.red)

    # list of points that make up a line
    point_list = list(bresenham(x1, y1, x2, y2))

    # draw for every point in the line
    for point in point_list:
        # draw single character
        libtcod.console_put_char(con, point[0], point[1], '\'', libtcod.BKGND_NONE)
        
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)


def draw_box(con, x1, y1, x2, y2):
    draw_line(con, x1, y1, x2, y1)
    draw_line(con, x2, y1, x2, y2)
    draw_line(con, x2, y2, x1, y2)
    draw_line(con, x1, y2, x1, y1)


def draw_borders(con, map_box_size, picker_box_size):
    #clear_screen(con)
    draw_box(con, map_box_size[0][0], map_box_size[0][1],
                  map_box_size[1][0], map_box_size[1][1])
    draw_box(con, picker_box_size[0][0], picker_box_size[0][1],
                  picker_box_size[1][0], picker_box_size[1][1])
    

def clear_screen(con):
    for y in range(SCREEN_HEIGHT):
        for x in range(SCREEN_WIDTH):
            libtcod.console_put_char(con, x, y, ' ', libtcod.BKGND_NONE)

    






