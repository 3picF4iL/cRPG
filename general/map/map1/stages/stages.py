import os
import random
import arcade
import arcade.gui
from general.func import set_bg_color, set_window_with_size, checking_lockkey_states
from general.const import map1_opt


class GameViewStart(arcade.View):
    def __init__(self):
        super().__init__()
        set_bg_color()
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        checking_lockkey_states()  # Turn off LOCK's keys

        self.stage = {
            # Elements lists appearing on the map
            "player_list": None,        # List of the players on the map
            "enemy_list": None,         # List of the enemies on the map
            "item_on_floor_list": None,     # List of the items on the map

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

    def on_show(self):
        self.setup()

    def setup(self):
        map_name = "../map1.json"

        layer_options = {
            "borders": {
                "use_spatial_hash": True,
            },
            "path": {
                "use_spatial_hash": True,
            },
            "meadow": {
                "use_spatial_hash": True,
            },
            "enemy": {
                "use_spatial_hash": True,
            }
        }

        self.stage["tile_map"] = arcade.load_tilemap(map_name, self.stage["map_opt"]["scale"], layer_options)
        self.stage["scene"] = arcade.Scene.from_tilemap(self.stage["tile_map"])

    def on_draw(self):
        arcade.start_render()
        self.stage["scene"].draw()
