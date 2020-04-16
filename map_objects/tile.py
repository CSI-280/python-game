class Tile:

    def __init__(self, blocked, block_sight=None, char_code=0, color=[255, 255, 255]):
        self.char_code = char_code

        self.blocked = blocked

        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight

        self.explored = False

        self.color = color

    def set_char_code(self, new_code):
        self.char_code = new_code

    def set_blocked(self, new_value):
        self.blocked = new_value

    def set_color(self, new_color):
        self.color = new_color

    def __str__(self):
        """This is a 'dunder' method.  This is what print() uses when it prints
        out things.  So if you print an object of this class, it will print this
        For example:
           x = Tile(True)
           print(x)

           'Char code 0, Blocked True, Block_sight: True'
        """
        return 'Char code {}, Blocked {}, Block_sight: {}'.format(
            self.char_code, self.blocked, self.block_sight
        )
