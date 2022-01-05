import arcade
from .const import player_map1_opt
from .func import load_texture_pair_mod


class CharacterStats:
    """
    Class for characters stats keeping

    :var char_astats: keeps standard values for character
    :var char_misc: miscellaneous values
    :var char_resistances: character resistances
    """

    # General stats
    char_astats = {
        "str": 20,
        "dex": 15,
        "vit": 20,
        "ene": 40
        }


class PlayerCharacter(arcade.Sprite, CharacterStats):
    def __init__(self):
        super().__init__()
        self.center_x = player_map1_opt["center_x"]
        self.center_y = player_map1_opt["center_y"]
        self.scale = player_map1_opt["scale"]
        self.cur_texture_index = 0
        self.player_variables = player_map1_opt

        self.player_variables["textures_walk"],\
        self.player_variables["textures_walk_nr"] = load_texture_pair_mod(self.player_variables["graphic_location"]
                                                                          + self.player_variables["textures_walk_file"],
                                                                          720, 0, 490)
        self.player_variables["textures_idle"],\
        self.player_variables["textures_idle_nr"] = load_texture_pair_mod(self.player_variables["graphic_location"]
                                                                       + self.player_variables["textures_idle_file"],
                                                                       720, 0, 490)
        # self.player_variables["textures_attack"] = load_texture_pair_mod(self.player_variables["graphic_location"]
        #                                                                  + self.player_variables["textures_attack_file"], # noqa
        #                                                                  720, 0, 490)

        self.hit_box = ([-100, -200], [-100, 0], [100, 0], [100, -200])

    def start_moving(self, key):
        if key == arcade.key.UP:
            self.player_variables["move_up"] = True
        elif key == arcade.key.DOWN:
            self.player_variables["move_down"] = True
        elif key == arcade.key.RIGHT:
            self.player_variables["move_right"] = True
        elif key == arcade.key.LEFT:
            self.player_variables["move_left"] = True

    def stop_moving(self, key):
        if key == arcade.key.UP:
            self.player_variables["move_up"] = False
        elif key == arcade.key.DOWN:
            self.player_variables["move_down"] = False
        elif key == arcade.key.RIGHT:
            self.player_variables["move_right"] = False
        elif key == arcade.key.LEFT:
            self.player_variables["move_left"] = False

    def move(self, delta_time):
        if self.player_variables["move_up"]:
            self.center_y = self.center_y + self.player_variables["movement_speed"] * delta_time

        if self.player_variables["move_down"]:
            self.center_y = self.center_y - self.player_variables["movement_speed"] * delta_time

        if self.player_variables["move_right"]:
            self.center_x = self.center_x + self.player_variables["movement_speed"] * delta_time
            self.player_variables["face_direction"] = 0

        if self.player_variables["move_left"]:
            self.center_x = self.center_x - self.player_variables["movement_speed"] * delta_time
            self.player_variables["face_direction"] = 1

        if not self.player_variables["move_up"] and not self.player_variables["move_down"]:
            self.change_y = 0
        if not self.player_variables["move_right"] and not self.player_variables["move_left"]:
            self.change_x = 0

        if self.player_variables["move_up"] or self.player_variables["move_down"] or \
                self.player_variables["move_right"] or self.player_variables["move_left"]:
            self.player_variables["is_moving"] = True
            self.move_animation()
        else:
            self.player_variables["is_moving"] = False
            self.idle_animation()

    def move_animation(self):
        self.cur_texture_index += 1
        if self.cur_texture_index >= \
                self.player_variables["textures_walk_nr"] * self.player_variables["animation_walk_speed"]:
            self.cur_texture_index = 0
        self.texture = self.player_variables["textures_walk"][self.cur_texture_index // self.player_variables["animation_walk_speed"]][self.player_variables["face_direction"]]

    def idle_animation(self):
        self.cur_texture_index += 1
        if self.cur_texture_index >= \
                self.player_variables["textures_idle_nr"] * self.player_variables["animation_idle_speed"]:
            self.cur_texture_index = 0
        self.texture = self.player_variables["textures_idle"][self.cur_texture_index // self.player_variables["animation_idle_speed"]][self.player_variables["face_direction"]]

    def on_update(self, delta_time: float = 1 / 60):
        self.move(delta_time)


