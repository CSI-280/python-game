
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
    (86, 12): 201,
    (88, 12): 205,
    (90, 12): 187,
    (92, 12): 215,
    (94, 12): 182,
    (96, 12): 216,
    (98, 12): 207,
    (100, 12): 181,
    (102, 12): 189,
    (104, 12): 213,
    (106, 12): 218,
    (108, 12): 196,
    (110, 12): 191,
    # Row Two
    (86, 14): 186,
    (88, 14): 206,
    (90, 14): 186,
    (92, 14): 185,
    (94, 14): 199,
    (96, 14): 203,
    (98, 14): 209,
    (100, 14): 198,
    (102, 14): 214,
    (104, 14): 212,
    (106, 14): 179,
    (108, 14): 197,
    (110, 14): 179,
    # Row Three
    (86, 16): 200,
    (88, 16): 205,
    (90, 16): 188,
    (92, 16): 204,
    (94, 16): 202,
    (96, 16): 208,
    (98, 16): 210,
    (100, 16): 211,
    (102, 16): 183,
    (104, 16): 190,
    (106, 16): 192,
    (108, 16): 196,
    (110, 16): 217,
    # Row Four
    (86, 18): 219,
    (88, 18): 220,
    (90, 18): 221,
    (92, 18): 222,
    (94, 18): 223,
    (96, 18): 226,
    (98, 18): 227,
    (100, 18): 228,
    (102, 18): 229,
    (104, 18): 184,
    (106, 18): 230,
    (108, 18): 231,
    (110, 18): 232,
    # Symbols
    # Row One
    (86, 21): 1,
    (88, 21): 2,
    (90, 21): 3,
    (92, 21): 4,
    (94, 21): 5,
    (96, 21): 6,
    (98, 21): 7,
    (100, 21): 8,
    (102, 21): 9,
    (104, 21): 10,
    (106, 21): 11,
    (108, 21): 12,
    (110, 21): 13,
    # Row Two
    (86, 23): 14,
    (88, 23): 15,
    (90, 23): 16,
    (92, 23): 17,
    (94, 23): 18,
    (96, 23): 19,
    (98, 23): 20,
    (100, 23): 21,
    (102, 23): 22,
    (104, 23): 23,
    (106, 23): 24,
    (108, 23): 25,
    (110, 23): 26,
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