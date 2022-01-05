import arcade

##################
# SCREEN SETTINGS
##################

SCREEN_SIZE = \
    {
        0: [800, 600],  # Small - 800x600
        1: [1024, 786],  # Normal - 1024x786
        2: [1920, 1080]  # Large - 1920x1080
    }

TITLE = "Monsters and Dungeons"
BG_COLOR = arcade.color.AMAZON

##################
# MAP SETTINGS
##################

# Map1

LAYER_NAME_WALLS = "Walls"
LAYER_NAME_ITEMS = "Items"
LAYER_NAME_PATH = "Path"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_ENEMIES = "Enemies"
LAYER_NAME_MEADOW = "Meadow"

map1_opt = {
    "map1_location": "general/map/map1/map1.json",
    "scale": 0.6,
    "layer_options": {
            LAYER_NAME_WALLS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_PATH: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_MEADOW: {
                "use_spatial_hash": True,
            },
    }
}

player_map1_opt = {
    "scale": 0.2,
    "center_x": 200,
    "center_y": 200,
    "movement_speed": 100,
    "move_up": False,
    "move_down": False,
    "move_right": False,
    "move_left": False,
    "is_moving": False,
    "is_show_stats": False,
    "face_direction": 0,  # Left = 1, right = 0

}

stage_map1_opt = {
            # Elements lists appearing on the map
            "player_list": arcade.SpriteList(),        # List of the players on the map
            "enemy_list": arcade.SpriteList(),         # List of the enemies on the map
            "item_on_floor_list": arcade.SpriteList(),     # List of the items on the map

            # Elements that need to be placed in the code
            "debugger": None,           # For the debug console
            "tile_map": None,           # Loading map from file
            "scene": None,              # Creating first scene
            "physics_engine": None,     # Physic engine
            "camera": None,             # Camera instance
            "gui": None,                # GUI instance
            "gui_camera": None,         # Camera GUI instance
            "map_opt": map1_opt,

            # Flag Information appearing on the map
            "show_char_stat": False,            # Show character stats on the right side of the screen
            "show_floor_item_stats": False,     # Show items name that lies on the floor

            # Other flags
            "on_path": True,        # changed from self.'path_walking', flag checking if the player is on the 'path'
                                    # Should be moved to class player?
            "debug_console": False  # Check if the debug console is enabled

        }

##########################
# Character initial settings
##########################

warrior_stats = {
    "char_astats": {
        "str": 20,
        "dex": 15,
        "vit": 20,
        "ene": 40,
        "max_hp": 100,
        "max_mana": 20,
        "actual_health_points": 100,
        "actual_mana_points": 20,
        "dmg_min": 1,
        "dmg_max": 3
        },
    # Miscellaneous stat
    "char_misc": {
        "lvl": 1,
        "mf": 20,  # Magic Find - 20%
        "gf": 5,  # Gold Find - 20% - increase max and min value of gold drop for value
        "gb": 0,   # Add X gold to min and max value
        "exp": 0,
        "diff": 1,  # 0, 1, 2 - 0 the lowest, 2 - the highest
        "place": "None",
        "dc": 100
        },

    # Char resistances
    "char_resistances": {
        "cr": 10,
        "fr": 10,
        "lr": 10,
        "pr": 10
        },

    "char_texture": {
        "graphic_location": "graphic/player/movement/",
        "textures_walk_file": "walking_18.png",
        "textures_walk_nr": 0,
        "textures_walk": [],
        "animation_walk_speed": 2,
        "textures_attack_file": "attacking_15.png",
        "textures_attack_nr": 0,
        "textures_attack": [],
        "animation_attack_speed": 4,
        "textures_idle_file": "idle_17.png",
        "textures_idle_nr": 0,
        "textures_idle": [],
        "animation_idle_speed": 5
    }
}

##################
# Other settings and variables
##################

MOVEMENT_KEYS = [
    [
        arcade.key.UP,
        arcade.key.DOWN,
    ],
    [
        arcade.key.RIGHT,
        arcade.key.LEFT
    ]
]

NEXT_LEVEL_EXP = {
    2: 1000,
    3: 1159,
    4: 1339,
    5: 1543,
    6: 1773,
    7: 2033,
    8: 2326,
    9: 2655,
    10: 3024,
    11: 3438,
    12: 3901,
    13: 4419,
    14: 4997,
    15: 5641,
    16: 6358,
    17: 7155,
    18: 8040,
    19: 9022,
    20: 10110,
    21: 11314,
    22: 12645,
    23: 14115,
    24: 15737,
    25: 17526,
    26: 19496,
    27: 21664,
    28: 24047,
    29: 26665,
    30: 29539,
    31: 32691,
    32: 36146,
    33: 39929,
    34: 44069,
    35: 48596,
    36: 53543,
    37: 58945,
    38: 64840,
    39: 71269,
    40: 78275,
    41: 85906,
    42: 94213,
    43: 103249,
    44: 113074,
    45: 123750,
    46: 135344,
    47: 147928,
    48: 161579,
    49: 176380,
    50: 192420,
    51: 209793,
    52: 228601,
    53: 248953,
    54: 270965,
    55: 294761,
    56: 320474,
    57: 348245,
    58: 378226,
    59: 410579,
    60: 445476,
    61: 483102,
    62: 523653,
    63: 567339,
    64: 614383,
    65: 665024,
    66: 719515,
    67: 778127,
    68: 841148,
    69: 908884,
    70: 981661,
    71: 1059827,
    72: 1143751,
    73: 1233826,
    74: 1330470,
    75: 1434126,
    76: 1545267,
    77: 1664394,
    78: 1792039,
    79: 1928768,
    80: 2075182,
    81: 2231918,
    82: 2399652,
    83: 2579103,
    84: 2771031,
    85: 2976244,
    86: 3195598,
    87: 3430001,
    88: 3680414,
    89: 3947857,
    90: 4233409,
    91: 4538214,
    92: 4863483,
    93: 5210498,
    94: 5580616,
    95: 5975273,
    96: 6395990,
    97: 6844374,
    98: 7322126,
    99: 7831044
}

SHORTCUTS = {
    "cr": "Cold resistance",
    "fr": "Fire resistance",
    "lr": "Light resistance",
    "pr": "Poison resistance",
    "str": "Strength",
    "vit": "Vitality",
    "ene": "Energy",
    "dex": "Dexterity",
    "exp": "Experience",
    "mf": "Magic Find",
    "diff": "Difficulty",
    "lvl": "Level",
    "place": "Actual place",  # actual place where char is
    "gf": "Gold Find",
    "dc": "Drop Chance",
    "gb": "Gold Bonus",
    "dmg_min": "Min Damage",
    "dmg_max": "Max Damage"
}

DND = ["max_hp", "max_mana", "actual_health_points", "actual_mana_points"]


