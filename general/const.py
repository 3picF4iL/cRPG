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

map1_opt = {
    "map1_location": "general/map/map1/map1.json",
    "scale": 0.6
}

player_map1_opt = {
    "scale": 0.2,
    "center_x": 200,
    "center_y": 200,
    "graphic_location": "graphic/player/movement/",
    "movement_speed": 200,
    "move_up": False,
    "move_down": False,
    "move_right": False,
    "move_left": False,
    "is_moving": False,
    "face_direction": 0,  # Left = 1, right = 0
    "textures_walk_file": "walking_18.png",
    "textures_walk_nr": 0,
    "textures_walk": [],
    "animation_walk_speed": 4,
    "textures_attack_file": "attacking_15.png",
    "textures_attack_nr": 0,
    "textures_attack": [],
    "animation_attack_speed": 4,
    "textures_idle_file": "idle_12.png",
    "textures_idle_nr": 0,
    "textures_idle": [],
    "animation_idle_speed": 4
}

##################
# Other settings and variables
##################

LAYER_NAME_WALLS = "Walls"
LAYER_NAME_ITEMS = "Items"
LAYER_NAME_PATH = "Path"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_ENEMIES = "Enemies"
LAYER_NAME_MEADOW = "Meadow"

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

