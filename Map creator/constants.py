
MAP_WIDTH = 80
MAP_HEIGHT = 50

OUTLINE_SIZE = 2

# 30 px for char picker
SCREEN_WIDTH = 80 + OUTLINE_SIZE*2 + 30
# 2 px for black outline and colored outline
SCREEN_HEIGHT = 50 + OUTLINE_SIZE*2

CELL_SIZE = 10

# Defines coords for map and picker boxes
MAP_BOX_SIZE = ((1, 1), (MAP_WIDTH + 2, MAP_HEIGHT + 2))
PICKER_BOX_SIZE = ((MAP_WIDTH + 2 + 2, 1), (SCREEN_WIDTH - 2, SCREEN_HEIGHT - 2))

# Defines UI elements as a dictionary
# Format: (x, y): char
ui_elements = {
    # TOOLS
    (93, 6): 218,   # pointer tool
    (95, 6): 8,     # wall tool
    (97, 6): 219,   # box tool
    (99, 6): 47,    # line tool
    (101, 6): 7,     # single char tool
    (103, 6): 88,   # erase tool
    # CHARS
    # Building pieces
    (87, 12): 201,
    (89, 12): 205,
    (91, 12): 187,
    (93, 12): 182,
    (95, 12): 183,
    (97, 12): 184,
    (99, 12): 185,
    (101, 12): 186,
    (103, 12): 187,
    (105, 12): 188,
    (107, 12): 189,
    (109, 12): 190,
    (87, 14): 186,
    (89, 14): 206,
    (91, 14): 186,
    (93, 14): 194,
    (95, 14): 195,
    (97, 14): 196,
    (99, 14): 197,
    (101, 14): 198,
    (103, 14): 199,
    (105, 14): 200,
    (107, 14): 201,
    (109, 14): 202,
    (87, 16): 200,
    (89, 16): 205,
    (91, 16): 188,
    (93, 16): 206,
    (95, 16): 207,
    (97, 16): 208,
    (99, 16): 209,
    (101, 16): 210,
    (103, 16): 211,
    (105, 16): 212,
    (107, 16): 213,
    (109, 16): 214,
    # Symbols
    (87, 19): 1,
    (89, 19): 2,
    (91, 19): 3,
    (93, 19): 4,
    (95, 19): 5,
    (97, 19): 6,
    (99, 19): 7,
    (101, 19): 8,
    (103, 19): 9,
    (105, 19): 10,
    (107, 19): 11,
    (109, 19): 12,
    (87, 21): 13,
    (89, 21): 14,
    (91, 21): 15,
    (93, 21): 16,
    (95, 21): 17,
    (97, 21): 18,
    (99, 21): 19,
    (101, 21): 20,
    (103, 21): 21,
    (105, 21): 22,
    (107, 21): 23,
    (109, 21): 24,
    # Floor pieces
<<<<<<< HEAD
    (87, 32): 176,
    (89, 32): 177,
    (91, 32): 178,
    (93, 32): 159
=======
    (87, 24): 176,
    (89, 24): 177,
    (91, 24): 178,
>>>>>>> 37897f27fd248786e90496c285dfd470565f895c
}

# Colors dict
# Format: (x, y): (char, color)
color_menu = {
    # Row One
    (87, 30): (219, (255, 255, 255)),   # White
    (89, 30): (219, (200, 50, 150)),    # Light Red
    (91, 30): (219, (200, 0, 0)),       # Red
    (93, 30): (219, (100, 0, 0)),       # Dark Red
    (95, 30): (219, (50, 150, 200)),    # Light Blue
    (97, 30): (219, (0, 0, 200)),       # Blue
    (99, 30): (219, (0, 0, 100)),       # Dark Blue
    (101, 30): (219, (50, 200, 150)),   # Light Green
    (103, 30): (219, (0, 200, 0)),      # Green
    (105, 30): (219, (0, 100, 0)),      # Dark Green
    (107, 30): (219, (255, 255, 0)),    # Yellow
    (109, 30): (219, (255, 150, 0)),    # Dark Yellow
    # Row Two
}

# Buttons
# Button size
# Format: (width, height)
button_size = (9, 2)

# Buttons dict
# Format: (x, y): (word)
button_menu = {
    (87, 36): 'EXPORT',
    (100, 36): 'CLEAR',
    (87, 40): 'IMPORT',
}