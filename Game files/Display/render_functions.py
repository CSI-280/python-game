import tcod as libtcod

from enum import Enum

from GamePlay.game_states import GameStates
from Display.menus import inventory_menu


class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             '{0}: {1}/{2}'.format(name, value, maximum))


def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, SCREEN_WIDTH,
               SCREEN_HEIGHT, bar_width, panel_height, panel_y, colors, game_state):

    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight
                char_color = libtcod.Color(
                    game_map.tiles[x][y].color[0],
                    game_map.tiles[x][y].color[1],
                    game_map.tiles[x][y].color[2]
                )
                dimmer_color = libtcod.Color(
                    int(game_map.tiles[x][y].color[0] * 0.3),
                    int(game_map.tiles[x][y].color[1] * 0.3),
                    int(game_map.tiles[x][y].color[2] * 0.3)
                )
                if visible:
                    libtcod.console_set_default_foreground(con, char_color)
                    libtcod.console_put_char(con,
                                             x,
                                             y,
                                             game_map.tiles[x][y].char_code,
                                             libtcod.BKGND_NONE)

                    game_map.tiles[x][y].explored = True

                elif game_map.tiles[x][y].explored:
                    libtcod.console_set_default_foreground(con, dimmer_color)
                    libtcod.console_put_char(con,
                                             x,
                                             y,
                                             game_map.tiles[x][y].char_code,
                                             libtcod.BKGND_NONE)

    # Draw all entities in the list
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map)

    libtcod.console_set_default_foreground(con, libtcod.white)
    libtcod.console_print_ex(con, 1, SCREEN_HEIGHT - 2, libtcod.BKGND_NONE,
                             libtcod.LEFT,
                             'HP: {0:02}/{1:02}'.format(player.fighter.hp,
                                                        player.fighter.max_hp))

    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               libtcod.light_red, libtcod.darker_red)

    libtcod.console_blit(panel, 0, 0, SCREEN_WIDTH, panel_height, 0, 0, panel_y)


    if game_state == GameStates.SHOW_INVENTORY:
        inventory_menu(con, 'Press key next to item to use it, ESC to exit.\n',
                       entity.inventory, 50, SCREEN_WIDTH, SCREEN_HEIGHT)

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char,
                                 libtcod.BKGND_NONE)


def clear_entity(con, entity):
    # erase the character that represents this object
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
