from enum import Enum


class GameStates(Enum):
    PLAYERS_TURN = 1
    ENEMY_TURN = 2
    SHOW_INVENTORY = 3
    PLAYER_DEAD = 4
    DROP_INVENTORY = 5
