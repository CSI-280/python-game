import tcod as libtcod
from constants import *
import draw_functions

import datetime
import json
from json import JSONEncoder

from tkinter import Tk
from tkinter.filedialog import askopenfilename


class Object:
    def __init__(self, attr, char_number, color=libtcod.white, x=0, y=0):
        self.coords = [x, y]
        self.attr = attr
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
                    self.attr,
                    self.char,
                    self.color
                ]
        }


class ObjectEncoder(JSONEncoder):
    def default(self, o):
        return o.encode()


objects = []


def display_map_object_properties(con, x, y):
    remove_duplicate_objects()
    for element in objects:
        temp_x = element.x + CANVAS_OFFSET_X
        temp_y = element.y + CANVAS_OFFSET_Y
        if temp_x == x and temp_y == y:
            message = "Char #: {} Attr: {}".format(element.char, element.attr)
            draw_functions.display_message(con, message, libtcod.white)
            break


def erase_map_object(con, x, y):
    for i in range(0, 1):
        for element in objects:
            temp_x = element.x + CANVAS_OFFSET_X
            temp_y = element.y + CANVAS_OFFSET_Y
            if temp_x == x and temp_y == y:
                objects.remove(element)

    draw_functions.draw_all_map_objects(con)


def erase_all_map_objects():
    objects.clear()
    print("Canvas cleared")


def edit_element_attributes(con, x, y):
    new_attr = input("Enter new attribute string below or '!' to esc:\n")
    if new_attr is not "!":
        for element in objects:
            temp_x = element.x + CANVAS_OFFSET_X
            temp_y = element.y + CANVAS_OFFSET_Y
            if temp_x == x and temp_y == y:
                element.attr = new_attr
                print("Character attributes changed successfully")
                break
    else:
        print("Character unchanged")


def remove_duplicate_objects():
    for element in objects:
        to_remove = []
        num_duplicates = 0
        removed = 0
        temp_x = element.x
        temp_y = element.y
        # Get number of duplicates for given element
        for other in objects:
            if (other.x, other.y) == (temp_x, temp_y):
                num_duplicates += 1
        # If duplicates exist then loop through list and delete until most recent
        if num_duplicates >= 1:
            for duplicate in objects:
                if (duplicate.x, duplicate.y) == (temp_x, temp_y) and removed < num_duplicates - 1:
                    removed += 1
                    to_remove.append(duplicate)
        for r in to_remove:
            objects.remove(r)
    print("Duplicates removed")


def update_map():
    for element in objects:
        for x, y in chars_menu:
            char, attr = chars_menu[(x, y)]
            if element.char == char:
                element.attr = attr
    print("Map attributes updated")


def import_map():
    global able_to_click

    try:
        # file picker
        Tk().withdraw()
        filename = askopenfilename(initialdir='../Map Files',
                                   title='Import map')
        print('Loading', filename)

        # test if the file can be opened, if not, FileNotFoundError will
        # be raised and loop will quit before erase_all_map_objects() is called
        with open(filename, 'r'):
            pass

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
            attr, char_number, color_list = list(element.values())[0]
            color = libtcod.Color(color_list[0], color_list[1], color_list[2])
            objects.append(Object(attr, char_number, color, x, y))

        print('Loaded', filename)
    except FileNotFoundError:
        print('Canceled load file')


def export_map():
    # TODO, make this a constant
    location = '../Map Files/'
    # current time
    file_name = '-'.join(str(datetime.datetime.now()).split('.'))
    # filename can't contain colons
    file_name = file_name.replace(':', '-') + '.json'
    # remove all duplicate objects in list
    remove_duplicate_objects()
    # open file for exporting
    with open(location + file_name, 'w') as file_out:
        file_out.write(json.dumps(objects, indent=4, cls=ObjectEncoder))
    print('Saved file as "{}"'.format(file_name))
