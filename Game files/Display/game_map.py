
import tcod as libtcod
from random import randint
from Display.tile import Tile
from Objects.entity import Entity
from Objects.item import Item
from Display.render_functions import RenderOrder
import json
import os, random

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def load_random_map(self, player):
        player_spawn_x = 0
        player_spawn_y = 0

        file = random.choice(os.listdir("../Map Files/"))
        print('Loading {}'.format(file))
        with open('../Map Files/' + file) as fin:
            data = fin.read()
        data = json.loads(data)

        for element in data:
            for coords, attr in element.items():
                x, y = coords.split(' ')
                x, y = int(x), int(y)
                color = attr[2]
                if len(attr[0]) > 0:
                    # collidable
                    if attr[0] == 'c':
                        self.tiles[x][y].set_blocked(True)
                        self.tiles[x][y].set_block_sight(True)
                    # player spawns next to the 'd'own stairs
                    if attr[0] == 'd':
                        player_spawn_x = x + 1
                        player_spawn_y = y

                char_code = attr[1]
                self.tiles[x][y].set_char_code(char_code)
                self.tiles[x][y].set_color(color)

        player.x = player_spawn_x
        player.y = player_spawn_y


    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities,
                 max_items_per_room):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            # random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # random position without going out of the boundaries of the map
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            # "Rect" class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with
            # this one
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                self.create_room(new_room)

                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    # this is the first room, where the player starts at
                    player.x = new_x
                    player.y = new_y
                else:
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip a coin (random number that is either 0 or 1)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room, entities, max_items_per_room)

                # finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities, max_items_per_room):
        num_items_per_room = randint(0, max_items_per_room)

        for i in range(num_items_per_room):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                # this if statement makes it an 50% chance to be "I" or "i"
                if randint(0, 100) < 50:
                    item_component = Item()
                    item = Entity(x, y, 'I', libtcod.pink, 'Potion of good vibes',
                                  render_order=RenderOrder.ITEM, item=item_component)

                    entities.append(item)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
