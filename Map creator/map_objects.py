
import tcod as libtcod

class Object():
    def __init__(self, name, char_number, color=libtcod.light_grey, x = 0, y = 0):
        self.name = name
        self.char = char_number
        self.color = color
        self.coords = [x, y]
    @property
    def x(self):
        return self.coords[0]
    @x.setter
    def x(self, newX):
        self.coords[0] = newX
    @property
    def y(self):
        return self.coords[1]
    @y.setter
    def y(self, newY):
        self.coords[1] = newY
    def get_char(self):
        return self.char
    def get_color(self):
        return self.color
    def __repr__(self):
        return str({self.name: [self.coords, self.char]})
    def __str__(self):
        return str(self.__repr__())

objects = []

# TODO
def remove_duplicate_objects():
    global objects
    pass


