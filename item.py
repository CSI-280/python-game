# Start for the item class. So far holds name, description,
class Item(object):
    def __init__(self, name, description, quantity = 1, key = False):
        self.name = name
        self.desc = description
        self.qty = quantity
        self.key = key
