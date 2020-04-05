from item import Item

class Inventory(object):
    def __init__(self):
        self.items = {}

    # Adds a new object of the item type to the dict
    def add_item(self, item):
        self.items[item.name] = item

    # Removes a key from the dict. Param is a string for the name of the item.
    def remove_item(self, item):
        if  not self.items[item].key:
            del self.items[item]
        else:
            print("Key item: cannot be dropped")

    # Rudimentary print function.
    def print_items(self):
        for item in self.items.values():
            print(item.name, item.desc, item.qty)
