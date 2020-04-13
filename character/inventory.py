import tcod as libtcod

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    # Adds a new object of the item type to the dict
    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': print('inventory full')
            })
        else:
            results.append({
                'item_added': item,
                'message': print('You picked up {0}!'.format(item.name))
            })

            self.items.append(item)

        return results

    # Rudimentary print function.
    def print_items(self):
        for item in self.items.values():
            print(item.name, item.desc, item.qty)
