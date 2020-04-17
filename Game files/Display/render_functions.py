import tcod as libtcod

from enum import Enum


class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3


def render_all(con, entities, game_map, fov_map, fov_recompute, SCREEN_WIDTH,
               SCREEN_HEIGHT, colors):
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

    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)


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