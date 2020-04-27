
import tcod as libtcod
from GamePlay.ai import BasicMonster
from GamePlay.fighter import Fighter
from Display.tile import Tile
from Objects.entity import *
from Objects.item import Item
from Display.render_functions import RenderOrder
from Objects.item_functions import heal
import constants
import json
import os
import random


class GameMap:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.entrance_stairs = (0, 0)
        self.exit_stairs = (0, 0)
        self.all_maps = []
        self.current_map = -1

    def initialize_tiles(self):
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]
        return tiles

    def get_map_data(self):
        # get correct file
        file = self.all_maps[self.current_map]
        # display message to console
        print('Loading {}'.format(file))
        # read json data from map file
        with open(file) as fin:
            data = fin.read()
        data = json.loads(data)
        # return json data from map file as a python list
        return data

    def generate_map_list(self, first_map, last_map):
        directory = "../Map files/"
        all_files = os.listdir(directory)
        # remove first and last map from directory list
        for map_string in all_files:
            if map_string == first_map or map_string == last_map:
                all_files.remove(map_string)
        # randomize all_files list
        random.shuffle(all_files)
        # prepend directory to each map
        all_files = [directory + map_string for map_string in all_files]
        # set first and last map accordingly
        all_files.insert(0, directory + first_map)
        all_files.append(directory + last_map)
        self.all_maps = all_files

    def load_next_map(self, player, entities):
        if self.current_map < len(self.all_maps):
            self.current_map += 1

            # get all map data from the file
            data = self.get_map_data()
            # generate next map
            self.generate_map(data, True, player, entities)

    def load_previous_map(self, player, entities):
        if self.current_map > 0:
            self.current_map -= 1

            # get all map data from the file
            data = self.get_map_data()
            # generate next map
            self.generate_map(data, False, player, entities)

    def generate_map(self, data, spawn_at_entrance, player, entities):
        self.tiles = self.initialize_tiles()

        player_spawn_x = 0
        player_spawn_y = 0

        # mark initial exit stairs (in case map creator didn't put any)
        self.exit_stairs = (0, 0)
        self.entrance_stairs = (0, 0)
        # loop through each element in our json
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
                        if spawn_at_entrance:
                            player_spawn_x = x + 1
                            player_spawn_y = y
                        self.entrance_stairs = (x, y)
                    # Mark (u)p stairs
                    if 'u' in attr[0]:
                        if not spawn_at_entrance:
                            player_spawn_x = x + 1
                            player_spawn_y = y
                        self.exit_stairs = (x, y)
                    # Add (i)tems
                    if 'w' in attr[0]:
                        item_component = Item(damage=constants.weapons_dict[char_code][1])
                        item_name = constants.weapons_dict[char_code][0]
                        item = Entity(x, y, char_code, color, item_name,
                                      render_order=RenderOrder.ITEM,
                                      item=item_component)
                        entities.append(item)
                    if 'h' in attr[0]:
                        item_component = Item(healing=True, use_function=heal, amount=10)
                        item_name = "Health"
                        item = Entity(x, y, char_code, color, item_name,
                                      render_order=RenderOrder.ITEM,
                                      item=item_component)
                        entities.append(item)
                    if 'a' in attr[0]:
                        item_component = Item(ammo=True)
                        item_name = "Ammo"
                        item = Entity(x, y, char_code, color, item_name,
                                      render_order=RenderOrder.ITEM,
                                      item=item_component)
                        entities.append(item)
                    # Add (e)nemies to list
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

    def get_stairs(self):
        """returns both positions of stairs in the map"""
        both_stairs = (self.entrance_stairs, self.exit_stairs)
        # for some reason pycharm likes it when I return a single variable
        # rather than a tuple
        return both_stairs

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