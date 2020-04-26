# Start for the item class. So far holds name, description,
class Item(object):
    def __init__(self, use_function=None, healing=False, ammo=False, damage=None, **kwargs):
        self.use_function = use_function
        self.function_kwargs = kwargs
        self.healing = healing
        self.ammo = ammo
        self.damage = damage

