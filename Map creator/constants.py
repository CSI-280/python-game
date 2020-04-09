
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
    # Building Pieces
    # Row One
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
    # Row Two
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
    # Row Three
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
    # Row One
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
    # Row Two
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
    (87, 24): 176,
    (89, 24): 177,
    (91, 24): 178,
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
    (107, 30): (219, (255, 200, 0)),    # Yellow
    (109, 30): (219, (255, 100, 0)),    # Orange
    # Row Two
    (87, 32): (219, (150, 150, 150)),   # Gray
    (89, 32): (219, (250, 128, 114)),   # Salmon
    (91, 32): (219, (220, 20, 60)),     # Crimson
    (93, 32): (219, (178, 34, 34)),     # Brick Red
    (95, 32): (219, (64, 224, 208)),    # Turquoise
    (97, 32): (219, (0, 128, 128)),     # Teal
    (99, 32): (219, (25, 25, 112)),     # Midnight Blue
    (101, 32): (219, (152, 251, 152)),  # Pale Green
    (103, 32): (219, (107, 142, 35)),   # Olive Green
    (105, 32): (219, (34, 139, 34)),    # Forest Green
    (107, 32): (219, (240, 230, 140)),  # Khaki
    (109, 32): (219, (210, 105, 30)),   # Dark Orange
    # Row Three
    (87, 34): (219, (212, 175, 55)),    # Metallic Gold
    (89, 34): (219, (153, 101, 21)),    # Golden Brown
    (91, 34): (219, (255, 182, 193)),   # Light Pink
    (93, 34): (219, (255, 20, 147)),    # Deep Red
    (95, 34): (219, (199, 21, 13)),     # Violet
    (97, 34): (219, (221, 160, 221)),   # Pale Purple
    (99, 34): (219, (255, 0, 255)),     # Fuchsia
    (101, 34): (219, (148, 0, 211)),    # Dark Violet
    (103, 34): (219, (75, 0, 130)),     # Indigo
    (105, 34): (219, (51, 17, 0)),      # Brown
    (107, 34): (219, (26, 4, 0)),       # Dark Brown
    (109, 34): (219, (26, 0, 0)),       # Darkest Brown
}

# Buttons
# Format: (width, height)
button_size = (9, 2)

# Buttons dict
# Format: (x, y): (word)
button_menu = {
    (87, 40): 'EXPORT',
    (100, 40): 'CLEAR',
    (87, 44): 'IMPORT',
}