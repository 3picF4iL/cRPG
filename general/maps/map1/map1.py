import arcade
import arcade.gui
from general.player import PlayerCharacter
from general.func import set_bg_color, set_player, checking_lockkey_states, get_window_size, center_camera_to_player
from general.menu.pause_menu import PauseMenu
from general.const import map1_opt, FUNC_KEYS, stage_map1_opt
from general.const import (LAYER_NAME_WALLS)


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

        self.stage["tile_map"] = arcade.load_tilemap(map_name, self.stage["map_opt"]["scale"],
                                                     layer_options)
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
        self.stage["player_list"][0].print_char_info_over_head()
        self.stage["gui_camera"].use()
        self.stage["player_list"][0].print_hud()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.stage["player_list"][0].set_move(x, y)

    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, _buttons: int, _modifiers: int):
        self.stage["player_list"][0].set_move(x, y)
        self.stage["player_list"][0].debug = [x, y]

    def on_mouse_hover(self, x, y):
        if self.stage["player_list"][0].center_x >= self.screen_w/2:
            x = x - self.stage["player_list"][0].center_x

        if self.stage["player_list"][0].center_y >= self.screen_h/2:
            y = y - self.screen_h/2

        for item in arcade.get_sprites_at_point([x, y], self.items_list):
            item.is_selected = True
            break
        else:
            for item in self.items_list:
                item.is_selected = False

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.stage["player_list"][0].debug = [x, y]

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            pause_menu = PauseMenu(previous_menu=self, menu_name="Pause Menu")
            self.window.show_view(pause_menu)

        elif symbol in FUNC_KEYS:
            self.stage["player_list"][0].func_keys(symbol, modifiers)

    def on_key_release(self, _symbol: int, _modifiers: int):
        if _symbol in FUNC_KEYS:
            self.stage["player_list"][0].func_keys(_symbol+1000, _modifiers)

    def on_update(self, delta_time: float):
        center_camera_to_player(self.stage["camera"],
                                self.stage["player_list"][0].center_x,
                                self.stage["player_list"][0].center_y)
        self.stage["player_list"][0].on_update(delta_time)
        self.stage["physic_engine"].update()

