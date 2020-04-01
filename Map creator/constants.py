
MAP_WIDTH = 80
MAP_HEIGHT = 50

OUTLINE_SIZE = 2

# 30 px for char picker
SCREEN_WIDTH = 80 + OUTLINE_SIZE*2 + 30
# 2 px for black outline and colored outline
SCREEN_HEIGHT = 50 + OUTLINE_SIZE*2

CELL_SIZE = 10

# define coords for map and picker boxes
MAP_BOX_SIZE = ((1, 1), (MAP_WIDTH + 2, MAP_HEIGHT + 2))
PICKER_BOX_SIZE = ((MAP_WIDTH + 2 + 2, 1), (SCREEN_WIDTH - 2, SCREEN_HEIGHT - 2))
