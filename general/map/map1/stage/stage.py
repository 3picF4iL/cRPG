import arcade
import arcade.gui
from general.func import set_bg_color, set_player, checking_lockkey_states
from general.const import map1_opt, MOVEMENT_KEYS
from general.const import (LAYER_NAME_PATH,
                           LAYER_NAME_WALLS,
                           LAYER_NAME_MEADOW,
                           LAYER_NAME_ENEMIES)


class GameViewStart(arcade.View):
    def __init__(self):
        super().__init__()
        set_bg_color()
        checking_lockkey_states()  # Turn off LOCK's keys

        self.stage = {
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

    def on_show(self):
        self.setup()

    def setup(self):
        map_name = map1_opt["map1_location"]

        layer_options = {
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
        self.stage["tile_map"] = arcade.load_tilemap(map_name, self.stage["map_opt"]["scale"], layer_options)
        self.stage["scene"] = arcade.Scene.from_tilemap(self.stage["tile_map"])
        set_player(self.stage["player_list"], self.stage["scene"])
        self.stage["physic_engine"] = arcade.PhysicsEngineSimple(self.stage["player_list"][0],
                                                                 [
                                                                     self.stage["scene"].
                                                                 get_sprite_list(LAYER_NAME_WALLS),
                                                                 #    self.stage["scene"].
                                                                # get_sprite_list(LAYER_NAME_ENEMIES)
                                                                 ]
                                                                 )

    def on_draw(self):
        arcade.start_render()
        self.stage["scene"].draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol in MOVEMENT_KEYS[0] or MOVEMENT_KEYS[1]:
            self.stage["player_list"][0].start_moving(symbol)
        pass

    def on_key_release(self, _symbol: int, _modifiers: int):
        if _symbol in MOVEMENT_KEYS[0] or MOVEMENT_KEYS[1]:
            self.stage["player_list"][0].stop_moving(_symbol)
        pass

    def on_update(self, delta_time: float):
        self.stage["player_list"][0].on_update(delta_time)
        self.stage["physic_engine"].update()

