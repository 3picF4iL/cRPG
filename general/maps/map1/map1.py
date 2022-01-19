import arcade
import arcade.gui
from abc import ABC, abstractmethod
from general.char_class.player import PlayerCharacter
from general.enemy.enemy import Enemy
from general.func import set_bg_color, set_player, checking_lockkey_states,\
    get_window_size, center_camera_to_player, set_enemies, \
    set_sprites_in_spritelist, check_the_battle, highlight_object
from general.menu.pause_menu import PauseMenu
from general.const import map1_opt, FUNC_KEYS, stage_map1_opt
from general.const import (LAYER_NAME_WALLS,
                           LAYER_NAME_ENEMIES,
                           LAYER_NAME_PLAYER,
                           LAYER_NAME_ENTITIES)


class GameViewStart(arcade.View):
    def __init__(self):
        checking_lockkey_states()  # Turn off LOCK's keys
        super().__init__()
        super(GameViewStart, self).__init__()
        self.stage_name = "Map_1"
        set_bg_color()

        self.screen_w, self.screen_h = get_window_size()
        self.stage = stage_map1_opt

    def setup(self):
        # Map settings
        map_name = map1_opt["map1_location"]
        layer_options = map1_opt["layer_options"]

        self.stage["tile_map"] = arcade.load_tilemap(map_name, self.stage["map_opt"]["scale"],
                                                     layer_options)
        self.stage["scene"] = arcade.Scene.from_tilemap(self.stage["tile_map"])

        # Player and entities settings
        set_player(0,
                   PlayerCharacter,
                   self.stage["scene"])

        self.player = self.stage["scene"].get_sprite_list(LAYER_NAME_PLAYER)[0]

        set_enemies(
            self.stage["enemies_on_map"],
            Enemy,
            self.stage["scene"],
            self.player)

        # Camera and physic engine
        self.stage["camera"] = arcade.Camera(self.screen_w, self.screen_h)
        self.stage["gui_camera"] = arcade.Camera(self.screen_w, self.screen_h)
        self.stage["physic_engine"] = arcade.PhysicsEngineSimple(self.player,
                                                                 [
                                                                     self.stage["scene"].get_sprite_list(LAYER_NAME_WALLS),
                                                                     self.stage["scene"].get_sprite_list(LAYER_NAME_ENTITIES)
                                                                  ]
                                                                 )

    def on_draw(self):
        # Start rendering
        arcade.start_render()

        # Camera use
        self.stage["camera"].use()
        # Scene with the layers drawing
        self.stage["scene"].draw()
        # Some debug
        self.player.print_char_info_over_head()

        # GUI for player at the end on the top view level
        self.stage["gui_camera"].use()
        self.player.print_hud()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.player.set_move(x, y)

    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, _buttons: int, _modifiers: int):
        self.player.set_move(x, y)
        #self.player.debug = (x, y)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.on_mouse_hover(x, y)

    def on_mouse_hover(self, x, y):
        highlight_object(
                         x, y,
                         self.player,
                         None,
                         self.stage["scene"].get_sprite_list('Enemies')
                         )

    #def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        #self.player.debug = (x, y)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            pause_menu = PauseMenu(previous_menu=self, menu_name="Pause Menu")
            self.window.show_view(pause_menu)

        elif symbol in FUNC_KEYS:
            self.player.func_keys(symbol, modifiers)

    def on_key_release(self, _symbol: int, _modifiers: int):
        if _symbol in FUNC_KEYS:
            self.player.func_keys(_symbol+1000, _modifiers)

    def on_update(self, delta_time: float):
        center_camera_to_player(self.stage["camera"],
                                self.player.center_x,
                                self.player.center_y)
        set_sprites_in_spritelist(self.stage["scene"].get_sprite_list('Entities'))
        for entity in self.stage["scene"].get_sprite_list('Entities'):
            entity.on_update(delta_time)
        check_the_battle(self.stage["scene"].get_sprite_list('Enemies'), self.player)

        self.stage["physic_engine"].update()

