
import tcod as libtcod
from GamePlay.ai import BasicMonster
from GamePlay.fighter import Fighter
from Display.tile import Tile
from Objects.entity import *
from Objects.item import Item
from Display.render_functions import RenderOrder
import constants
import json
import os
import random


class GameMap:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]
        return tiles

    def load_random_map(self, player, entities):
        player_spawn_x = 0
        player_spawn_y = 0

        file = random.choice(os.listdir("./Map Files/"))
        print('Loading {}'.format(file))
        with open('./Map Files/' + file) as fin:
            data = fin.read()
        data = json.loads(data)

        for element in data:
            for coords, attr in element.items():
                x, y = coords.split(' ')
                x, y = int(x), int(y)
                char_code = attr[1]
                color = attr[2]
                self.tiles[x][y].set_char_code(char_code)
                self.tiles[x][y].set_color(color)
                if len(attr[0]) > 0:
                    # Check for (c)ollision
                    if 'c' in attr[0]:
                        self.tiles[x][y].set_blocked(True)
                        self.tiles[x][y].set_block_sight(True)
                    # Set (t)ransparency
                    # If transparent then tile does not block vision
                    if 't' in attr[0]:
                        self.tiles[x][y].set_block_sight(False)
                    # Spawn player next to (d)own stairs
                    if 'd' in attr[0]:
                        player_spawn_x = x + 1
                        player_spawn_y = y
                    # Add (i)tems
                    if 'i' in attr[0]:
                        item_component = Item()
                        item_name = constants.items_dict[char_code]
                        item = Entity(x, y, char_code, color, item_name,
                                      render_order=RenderOrder.ITEM,
                                      item=item_component)
                        entities.append(item)

                    # Add (e)nemies to List
                    if 'e' in attr[0]:
                        # reset that spot on map to be blank with no attributes
                        self.tiles[x][y].set_char_code(0)
                        self.tiles[x][y].set_color((0, 0, 0))
                        attr.clear()

                        # create zombie where specified
                        fighter_component = Fighter(hp=10, defense=0, power=3)
                        ai_component = BasicMonster()
                        zombie = Entity(x, y, char_code, color, 'zombie',
                                        blocks=True, render_order=RenderOrder.ACTOR,
                                        fighter=fighter_component, ai=ai_component)
                        entities.append(zombie)

        player.x = player_spawn_x
        player.y = player_spawn_y

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        else:
            return False

    def reset_tile(self, x, y):
        tile = self.tiles[x][y]
        tile.char_code = 0
        tile.color = libtcod.black
        tile.block_sight = False
        tile.blocked = False