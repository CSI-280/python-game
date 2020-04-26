import tcod as libtcod


def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message':'You are already at full health'})
        entity.fighter.heal(amount)
        results.append({'consumed': True, 'message': 'Your wounds start to feel better!'})

    return results
