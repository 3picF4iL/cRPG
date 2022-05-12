import arcade.arcade as arcade
from random import randint

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
LAYER_NAME_ENTITIES = "Entities"

map1_opt = {
    "map1_location": "general/maps/map1/map1.json",
    "scale": 0.8,
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
    "is_moving": False,
    "is_show_stats": False,
    "is_attacking": False,
    "face_direction": 0,  # Left = 1, right = 0


}

stage_map1_opt = {
    # Elements lists appearing on the maps
    "player_list": arcade.SpriteList(visible=False),  # List of the players on the maps
    "enemy_list": arcade.SpriteList(visible=False),  # List of the enemies on the maps
    "item_on_floor_list": arcade.SpriteList(),  # List of the items on the maps
    "entities_list": arcade.SpriteList(),

    # Elements that need to be placed in the code
    "debugger": None,  # For the debug console
    "tile_map": None,  # Loading maps from file
    "scene": None,  # Creating first scene
    "physics_engine": None,  # Physic engine
    "physics_engine_enemies": None,  # Physic engine - FOR TEST (ENEMIES COLLISION BETWEEN EACH OTHER)
    "camera": None,  # Camera instance
    "gui": None,  # GUI instance
    "gui_camera": None,  # Camera GUI instance
    "map_opt": map1_opt,

    # Flag Information appearing on the maps
    "show_char_stat": False,  # Show character stats on the right side of the screen
    "show_floor_item_stats": False,  # Show items name that lies on the floor

    # Other flags
    "on_path": True,  # changed from self.'path_walking', flag checking if the player is on the 'path'
    # Should be moved to char_class player?
    "debug_console": False,  # Check if the debug console is enabled
    # "enemy_file_conf": "general/enemy/enemy_settings"
    "enemies_on_map": lambda filename="general/enemy/enemy_settings": [(f.read(), f.close()) for f in [open(filename)]][0][0]

}

ENEMY_STATS = {
    0: {
        "enemy_id": 0,
        "enemy_name": "FAST ZOMBIE",
        "scale": 0.2,
        "initial_x": None,
        "initial_y": None,
        "max_hp": 100,
        "max_mana": 10,
        "actual_health_points": 100,
        "actual_mana_points": 10,
        "mvm": 80,
        "as": 10,
        "dmg_min": 1,
        "dmg_max": 3,
        "def": 2,
        "lvl": 1,
        "exp": 1000,
        "diff": 0,
        "cr": 10,
        "fr": 10,
        "lr": 10,
        "pr": 10,
        "radius": 50,
        "is_attacking": False,
        "is_walking": False,
        "is_moving": False,
        "player_in_radius": False,
        "direction_change_x": True,
        "direction_change_y": True,
        "is_highlighted": False,
        "is_patrol": False,
        "is_hit": False,
        "is_killed": False,
        "dest_x": None,
        "dest_y": None,
        "face_direction": randint(0, 1),
        "attack_frame": 8,
        "textures_walk": [],
        "textures_walk_nr": "",
        "textures_walk_file": "walking_18.png",
        "animation_walk_speed": 3,
        "textures_idle": [],
        "textures_idle_nr": "",
        "textures_idle_file": "idle_17.png",
        "textures_attack": [],
        "textures_attack_nr": "",
        "textures_attack_file": "attack_12.png",
        "animation_attack_speed": 4,
        "textures_hurt": [],
        "textures_hurt_nr": "",
        "textures_hurt_file": "hurt_12.png",
        "animation_hurt_speed": 4,
        "textures_dying": [],
        "textures_dying_nr": "",
        "textures_dying_file": "dying_15.png",
        "animation_dying_speed": 3,
        "animation_idle_speed": 5,
        "animation_last_state": 0,
        "animation_cur_state": 0,
        "graphic_location": f"graphic/enemy/0/movement/",
    },
    1: {
        "enemy_id": 1,
        "enemy_name": "SLOW ZOMBIE",
        "scale": 0.2,
        "initial_x": None,
        "initial_y": None,
        "max_hp": 100,
        "max_mana": 10,
        "actual_health_points": 100,
        "actual_mana_points": 10,
        "mvm": 40,
        "as": 10,
        "dmg_min": 1,
        "dmg_max": 3,
        "def": 2,
        "lvl": 1,
        "exp": 300,
        "diff": 0,
        "cr": 10,
        "fr": 10,
        "lr": 10,
        "pr": 10,
        "radius": 50,
        "is_attacking": False,
        "is_walking": False,
        "is_moving": False,
        "player_in_radius": False,
        "direction_change_x": True,
        "direction_change_y": True,
        "is_highlighted": False,
        "dest_x": None,
        "dest_y": None,
        "is_patrol": False,
        "is_hit": False,
        "is_killed": False,
        "face_direction": randint(0, 1),
        "attack_frame": 8,
        "textures_walk": [],
        "textures_walk_nr": "",
        "textures_walk_file": "walking_18.png",
        "animation_walk_speed": 3,
        "textures_idle": [],
        "textures_idle_nr": "",
        "textures_idle_file": "idle_17.png",
        "textures_attack": [],
        "textures_attack_nr": "",
        "textures_attack_file": "attack_12.png",
        "animation_attack_speed": 4,
        "animation_idle_speed": 5,
        "textures_hurt": [],
        "textures_hurt_nr": "",
        "textures_hurt_file": "hurt_12.png",
        "animation_hurt_speed": 4,
        "textures_dying": [],
        "textures_dying_nr": "",
        "textures_dying_file": "dying_15.png",
        "animation_dying_speed": 3,
        "animation_last_state": 0,
        "animation_cur_state": 0,
        "graphic_location": f"graphic/enemy/1/movement/",
    },
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

FUNC_KEYS = [
    arcade.key.Q,
    arcade.key.TAB,
    arcade.key.LALT
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
    "dmg_max": "Max Damage",
    "mvm": "Movement speed",
    "as": "Attack Speed",
    "stamina": "Stamina"
}

DND = ["max_hp",
       "max_mana",
       "actual_health_points",
       "actual_mana_points",
       "actual_stamina_points",
       "actual_health_points",
       "actual_mana_points",
       "actual_stamina_points",
       "dmg_min",
       "dmg_max",
       "mf",  # Magic Find - 20%
       "gf",  # Gold Find - 20% - increase max and min value of gold drop for value
       "gb",  # Add X gold to min and max value
       "exp",  # Experience
       "diff",  # 0, 1, 2 - 0 the lowest, 2 - the highest
       "place",  # Where char is actually
       "dc",  # Drop Chance - if enemy killed = % chance to drop anything
       "mvm",  # Movement speed
       "as",  # Attack speed %
       "lvl_hp",  # HP increasing when lvl up
       "lvl_mana",  # Mana increasing when lvl up
       "lvl_stamina",  # Stamina increasing when lvl up
       "add_str",  # Strength value when changing
       "add_dex",  # Dexterity value when changing
       "add_vit",  # HP increasing when changing
       "add_ene",  # Mana increasing when lvl up
       "stamina",
       "lvl",
       "textures_walk_file",
       "animation_walk_speed",
       "textures_attack_file",
       "animation_attack_speed",
       "textures_idle_file",
       "animation_idle_speed",
       # Char textures variables that will be set during initialization
       "graphic_location",
       "animation_last_state",
       "animation_cur_state",
       "textures_walk_nr",
       "textures_attack_nr",
       "textures_idle_nr",
       "textures_walk",
       "textures_attack",
       "textures_idle",
       "animation_last_state",
       "animation_cur_state",
       "face_direction",
       "textures_walk_nr",
       "textures_attack_nr",
       "textures_idle_nr",
       "textures_hurt_nr",
       "textures_walk",
       "textures_attack",
       "textures_idle",
       "textures_hurt",
       "textures_hurt_file",
       "textures_idle_file",
       "idle_17.png",
       "animation_idle_speed",
       "animation_hurt_speed",
]
