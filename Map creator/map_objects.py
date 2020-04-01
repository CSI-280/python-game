
class Object():
    def __init__(self, name, char_number, x = 0, y = 0):
        self.coords = [x, y]
        self.name = name
        self.char = char_number
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
    def __repr__(self):
        return str({self.name: [self.coords, self.char]})
    def __str__(self):
        return str(self.__repr__())

objects = []

# TODO
def remove_duplicate_objects():
    global objects
    pass


