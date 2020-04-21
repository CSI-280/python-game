from Display.render_functions import RenderOrder

class Entity:

    def __init__(self, x, y, char, color, name, blocks=False, render_order=RenderOrder.CORPSE,
                 item=None, inventory=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.item = item
        self.inventory = inventory

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

entities = []

def get_blocking_entities_at_location(entities_list, destination_x, destination_y):
    for entity in entities_list:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None
