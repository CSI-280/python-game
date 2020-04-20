
import tcod as libtcod


def handle_keys(key):
    # Movement keys
    if key.vk == libtcod.KEY_UP or key.c == ord('w'):
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key.c == ord('s'):
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key.c == ord('a'):
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key.c == ord('d'):
        return {'move': (1, 0)}

    # Pickup item
    if key.c == ord('g'):
        return {'pickup': True}

    # Open inventory
    if key.c == ord('i'):
        return {'inventory': True}

    if key.vk == libtcod.KEY_ENTER and (key.lalt or key.ralt):
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}