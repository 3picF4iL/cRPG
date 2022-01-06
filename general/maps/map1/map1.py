import arcade
import arcade.gui
from general.player import PlayerCharacter
from general.func import set_bg_color, set_player, checking_lockkey_states, get_window_size, center_camera_to_player
from general.pause_menu import PauseMenu
from general.const import map1_opt, MOVEMENT_KEYS, stage_map1_opt
from general.const import (LAYER_NAME_PATH,
                           LAYER_NAME_WALLS,
                           LAYER_NAME_MEADOW,
                           LAYER_NAME_ENEMIES)


class GameViewStart(arcade.View):
    def __init__(self):
        super().__init__()
        super(GameViewStart, self).__init__()
        self.stage_name = "Map_1"
        set_bg_color()
        checking_lockkey_states()  # Turn off LOCK's keys
        self.screen_w, self.screen_h = get_window_size()
        self.stage = stage_map1_opt

    def setup(self):
        map_name = map1_opt["map1_location"]
        layer_options = map1_opt["layer_options"]

        self.stage["tile_map"] = arcade.load_tilemap(map_name, self.stage["map_opt"]["scale"], layer_options)
        self.stage["scene"] = arcade.Scene.from_tilemap(self.stage["tile_map"])
        set_player(PlayerCharacter, self.stage["player_list"], self.stage["scene"])
        self.stage["camera"] = arcade.Camera(self.screen_w, self.screen_h)
        self.stage["gui_camera"] = arcade.Camera(self.screen_w, self.screen_h)

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
        self.stage["camera"].use()
        self.stage["scene"].draw()
        self.stage["gui_camera"].use()
        self.stage["player_list"][0].print_hud()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            pausemenu = PauseMenu(self)
            self.window.show_view(pausemenu)

        if symbol in MOVEMENT_KEYS[0] or symbol in MOVEMENT_KEYS[1]:
            self.stage["player_list"][0].start_moving(symbol)
        else:
            self.stage["player_list"][0].func_keys(symbol)
        pass

    def on_key_release(self, _symbol: int, _modifiers: int):
        if _symbol in MOVEMENT_KEYS[0] or _symbol in MOVEMENT_KEYS[1]:
            self.stage["player_list"][0].stop_moving(_symbol)
        else:
            self.stage["player_list"][0].func_keys(_symbol+1000)
        pass

    def on_update(self, delta_time: float):
        center_camera_to_player(self.stage["camera"],
                                self.stage["player_list"][0].center_x,
                                self.stage["player_list"][0].center_y)
        self.stage["player_list"][0].on_update(delta_time)
        self.stage["physic_engine"].update()

