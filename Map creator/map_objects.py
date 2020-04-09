import tcod as libtcod
from constants import *
import draw_functions

import datetime
import json
from json import JSONEncoder

from tkinter import Tk
from tkinter.filedialog import askopenfilename


class Object():
    def __init__(self, name, char_number, color=libtcod.light_grey, x=0, y=0):
        self.coords = [x, y]
        self.name = name
        self.char = char_number
        self.color = color

    @property
    def x(self):
        return self.coords[0]

    @x.setter
    def x(self, new_x):
        self.coords[0] = new_x

    @property
    def y(self):
        return self.coords[1]

    @y.setter
    def y(self, new_y):
        self.coords[1] = new_y

    def get_char(self):
        return self.char

    def get_color(self):
        return self.color

    def encode(self):
        """Format JSON uses in export_map()"""
        return {
            str(self.coords[0]) + ' ' + str(self.coords[1]):
                [
                    self.name,
                    self.char,
                    self.color
                ]
        }


class ObjectEncoder(JSONEncoder):
    def default(self, o):
        return o.encode()


objects = []


def erase_map_object(con, x, y):
    for element in objects:
        temp_x = element.x + OUTLINE_SIZE
        temp_y = element.y + OUTLINE_SIZE
        if temp_x == x and temp_y == y:
            print("Removed ", element)
            objects.remove(element)
            draw_functions.draw_all_map_objects(con)


def erase_all_map_objects():
    objects.clear()
    print("Canvas cleared")


# TODO
def remove_duplicate_objects():
    pass


def import_map():
    # file picker
    Tk().withdraw()
    filename = askopenfilename(initialdir='../Map Files',
                               title='Import map')
    print('Loading', filename)

    erase_all_map_objects()
    print(objects)

    # get json from file
    with open(filename, 'r') as fin:
        json_output = json.loads(fin.read())

    # convert each json element to an 'Object'
    for element in json_output:
        x, y = tuple(list(element.keys())[0].split(' '))
        x = int(x)
        y = int(y)
        name, char_number, color_list = list(element.values())[0]
        color = libtcod.Color(color_list[0], color_list[1], color_list[2])
        objects.append(Object(name, char_number, color, x, y))

    print('Loaded', filename)


def export_map():
    # TODO, make this a constant
    location = '../Map Files/'
    # current time
    file_name = '-'.join(str(datetime.datetime.now()).split('.'))
    # filename can't contain colons
    file_name = file_name.replace(':', '-') + '.json'
    # open file for exporting
    with open(location + file_name, 'w') as file_out:
        file_out.write(json.dumps(objects, indent=4, cls=ObjectEncoder))
    print('Saved file as "{}"'.format(file_name))
