import math
import arcade
from .const import player_map1_opt, warrior_stats
from .func import load_texture_pair_mod, get_map_point
from .gui import GUI


class CharacterStats:
    """
    Class for characters stats keeping

    :var self.char_astats: keeps standard values for character
    :var self.char_misc: miscellaneous values
    :var self.char_resistances: character resistances
    """

    def __init__(self):

        # General stats
        self.char_astats = warrior_stats["char_astats"]

        # Miscellaneous stat
        self.char_misc = warrior_stats["char_misc"]

        # Char resistances
        self.char_resistances = warrior_stats["char_resistances"]

        # Char texture, animation settings
        self.player_texture = warrior_stats["char_texture"]


class PlayerCharacter(arcade.Sprite, GUI, CharacterStats):
    def __init__(self):
        super().__init__()
        CharacterStats.__init__(self)
        GUI.__init__(self)

        self.center_x = player_map1_opt["center_x"]
        self.center_y = player_map1_opt["center_y"]
        self.scale = player_map1_opt["scale"]
        self.cur_texture_index = 0
        self.player_variables = player_map1_opt

        self.player_texture["textures_walk"], self.player_texture["textures_walk_nr"] = \
            load_texture_pair_mod(self.player_texture["graphic_location"] + self.player_texture["textures_walk_file"],
                                  720, 0, 490)

        self.player_texture["textures_idle"], self.player_texture["textures_idle_nr"] = \
            load_texture_pair_mod(self.player_texture["graphic_location"] + self.player_texture["textures_idle_file"],
                                  720, 0, 490)

        self.player_texture["textures_attack"], self.player_texture["textures_attack_nr"] = \
            load_texture_pair_mod(self.player_texture["graphic_location"] + self.player_texture["textures_attack_file"],
                                  720, 0, 490)

        self.hit_box = ([-100, -200], [-100, 0], [100, 0], [100, -200])

    def func_keys(self, key, mod):
        if key == arcade.key.TAB:
            self.player_variables["is_show_stats"] = False if self.player_variables["is_show_stats"] else True
        elif mod == arcade.key.MOD_ALT:
            self.player_variables["is_attacking"] = True

    def set_move(self, dest_x, dest_y):
        _x, _y = get_map_point([dest_x, dest_y], [self.center_x, self.center_y])
        self.player_variables["moving_dest_x"] = _x
        self.player_variables["moving_dest_y"] = _y
        self.player_variables["is_moving"] = True
        self.face_dir_change(self.player_variables["moving_dest_x"] - self.center_x)

    def _stop(self):
        self.player_variables["is_moving"] = False
        self.player_variables["moving_dest_x"] = None
        self.player_variables["moving_dest_y"] = None
        return True

    def moving(self, _x, _y, delta_time):

        if self.player_variables["is_moving"] and _x and _y:
            goto_x, goto_y = _x, _y
            x_diff, y_diff = goto_x - self.center_x, goto_y - self.center_y

            if math.fabs(round(x_diff)) <= 1 and math.fabs(round(y_diff)) <= 1:
                self._stop()

            angle = math.atan2(y_diff, x_diff)
            self.center_x += math.cos(angle) * self.player_variables["movement_speed"] * delta_time
            self.center_y += math.sin(angle) * self.player_variables["movement_speed"] * delta_time
            self.move_animation(delta_time)
        elif self.player_variables["is_attacking"]:
            self.attack_animation(delta_time)
        else:
            self.idle_animation(delta_time)
        self.player_texture["animation_last_state"] = self.player_texture["animation_cur_state"]

    def _check_a_state(self):
        if self.player_texture["animation_cur_state"] != self.player_texture["animation_last_state"]:
            self.cur_texture_index = 0

    def set_movement_speed(self, value):
        self.player_variables["movement_speed"] = value

    def change_movement_speed(self, value):
        self.player_variables["movement_speed"] += value

    def face_dir_change(self, x):
        if x > 0:
            self.player_variables["face_direction"] = 0
        elif x < 0:
            self.player_variables["face_direction"] = 1

    def move_animation(self, delta_time):
        self.player_texture["animation_cur_state"] = 1
        self._check_a_state()
        self.cur_texture_index += 1
        if self.cur_texture_index >= \
                self.player_texture["textures_walk_nr"] * self.player_texture["animation_walk_speed"]:
            self.cur_texture_index = 0
        self.texture = self.player_texture["textures_walk"][self.cur_texture_index // self.player_texture["animation_walk_speed"]][self.player_variables["face_direction"]]

    def idle_animation(self, delta_time):
        self.player_texture["animation_cur_state"] = 0
        self._check_a_state()
        self.cur_texture_index += 1
        if self.cur_texture_index >= \
                self.player_texture["textures_idle_nr"] * self.player_texture["animation_idle_speed"]:
            self.cur_texture_index = 0
        self.texture = self.player_texture["textures_idle"][self.cur_texture_index // self.player_texture["animation_idle_speed"]][self.player_variables["face_direction"]]

    def attack_animation(self, delta_time):
        self.player_texture["animation_cur_state"] = 2
        self._check_a_state()
        self.set_movement_speed(50)
        self.cur_texture_index += 1
        if self.cur_texture_index >= \
                self.player_texture["textures_attack_nr"] * self.player_texture["animation_attack_speed"]:
            self.cur_texture_index = 0
            self.player_variables["is_attacking"] = False
            self.set_movement_speed(100)
        self.texture = self.player_texture["textures_attack"][self.cur_texture_index
                                                              // self.player_texture["animation_attack_speed"]][self.player_variables["face_direction"]]

    def on_update(self, delta_time: float = 1 / 60):
        self.moving(self.player_variables["moving_dest_x"],
                    self.player_variables["moving_dest_y"],
                    delta_time)
