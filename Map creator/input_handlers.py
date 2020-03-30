import tcod as libtcod

def handle_keys(key):
    """
    returns a dictionary depending on key inputted
    """
    # press alt + enter to go into fullscreen
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    return {}
