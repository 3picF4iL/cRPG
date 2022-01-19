import math
import arcade
from general.const import player_map1_opt
from general.func import load_texture_pair_mod, get_map_point
from general.gui import GUI
from general.char_class.default_char import CharClass


class PlayerCharacter(arcade.Sprite, GUI, CharClass):
    def __init__(self, char_class):
        CharClass.__init__(self, char_class)
        super().__init__()
        GUI.__init__(self)

        self.personal_id = 1000
        self.center_x = player_map1_opt["center_x"]
        self.center_y = player_map1_opt["center_y"]
        self.scale = player_map1_opt["scale"]
        self.cur_texture_index = 0
        self.player_variables = player_map1_opt
        self.timer = 0
        self.char_stats["textures_walk"], self.char_stats["textures_walk_nr"] = \
            load_texture_pair_mod(self.char_stats["graphic_location"] + self.char_stats["textures_walk_file"],
                                  720, 0, 490)

        self.char_stats["textures_idle"], self.char_stats["textures_idle_nr"] = \
            load_texture_pair_mod(self.char_stats["graphic_location"] + self.char_stats["textures_idle_file"],
                                  720, 0, 490)

        self.char_stats["textures_attack"], self.char_stats["textures_attack_nr"] = \
            load_texture_pair_mod(self.char_stats["graphic_location"] + self.char_stats["textures_attack_file"],
                                  720, 0, 490)

        self.char_stats["textures_hurt"], self.char_stats["textures_hurt_nr"] = \
            load_texture_pair_mod(self.char_stats["graphic_location"] + self.char_stats["textures_hurt_file"],
                                  720, 0, 490)

        self.hit_box = ([-100, -200], [-100, -100], [100, -100], [100, -200])

    def func_keys(self, key, mod):
        if key == arcade.key.TAB:
            self.player_variables["is_show_stats"] = False if self.player_variables["is_show_stats"] else True
        elif mod == arcade.key.MOD_ALT:
            self.player_variables["is_attacking"] = True

    def set_move(self, dest_x, dest_y):
        _x, _y = get_map_point([dest_x, dest_y+self.height/2-10], [self.center_x, self.center_y])
        self.player_variables["moving_dest_x"] = _x
        self.player_variables["moving_dest_y"] = _y
        self.player_variables["is_moving"] = True
        self.face_dir_change(self.player_variables["moving_dest_x"] - self.center_x)

    def _stop(self):
        self.player_variables["is_moving"] = False
        self.player_variables["moving_dest_x"] = None
        self.player_variables["moving_dest_y"] = None
        return True

    def is_moving(self, delta_time):
        pass

    def moving(self, _x, _y, delta_time):
        if self.player_variables["is_moving"] and _x and _y:
            goto_x, goto_y = _x, _y
            x_diff, y_diff = goto_x - self.center_x, goto_y - self.center_y

            if math.fabs(round(x_diff)) <= 1 and math.fabs(round(y_diff)) <= 1:
                self._stop()
            else:
                self.timer += delta_time

            angle = math.atan2(y_diff, x_diff)
            self.center_x += math.cos(angle) * self.player_variables["movement_speed"] * delta_time
            self.center_y += math.sin(angle) * self.player_variables["movement_speed"] * delta_time
            self.move_animation(delta_time)
        elif self.player_variables["is_attacking"]:
            self.attack_animation(delta_time)

        self.char_stats["animation_last_state"] = self.char_stats["animation_cur_state"]
        self.debug = self.timer

    def _check_a_state(self):
        if self.char_stats["animation_cur_state"] != self.char_stats["animation_last_state"]:
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

    def reset_animation_state(self):
        self.char_stats["is_hit"] = False

    def move_animation(self, delta_time):
        self.reset_animation_state()
        self.char_stats["animation_cur_state"] = 1
        self._check_a_state()
        self.cur_texture_index += 1
        if self.cur_texture_index >= \
                self.char_stats["textures_walk_nr"] * self.char_stats["animation_walk_speed"]:
            self.cur_texture_index = 0
        self.texture = self.char_stats["textures_walk"][self.cur_texture_index // self.char_stats["animation_walk_speed"]][self.player_variables["face_direction"]]

    def idle_animation(self, delta_time):
        self.char_stats["animation_cur_state"] = 0
        self._check_a_state()
        self.cur_texture_index += 1
        if self.cur_texture_index >= \
                self.char_stats["textures_idle_nr"] * self.char_stats["animation_idle_speed"]:
            self.cur_texture_index = 0
        self.texture = self.char_stats["textures_idle"][self.cur_texture_index // self.char_stats["animation_idle_speed"]][self.player_variables["face_direction"]]
        self.char_stats["animation_last_state"] = self.char_stats["animation_cur_state"]

    def attack_animation(self, delta_time):
        self.char_stats["animation_cur_state"] = 2
        self._check_a_state()
        self.set_movement_speed(50)
        self.cur_texture_index += 1
        if self.cur_texture_index >= \
                self.char_stats["textures_attack_nr"] * self.char_stats["animation_attack_speed"]:
            self.cur_texture_index = 0
            self.player_variables["is_attacking"] = False
            self.set_movement_speed(100)
        self.texture = self.char_stats["textures_attack"][self.cur_texture_index
                                                              // self.char_stats["animation_attack_speed"]][self.player_variables["face_direction"]]

        self.char_stats["animation_last_state"] = self.char_stats["animation_cur_state"]

    def get_hurt(self, delta_time):
        if self.char_stats["is_hit"]:
            self.char_stats["animation_cur_state"] = 3
            self._check_a_state()
            self.cur_texture_index += 1
            if self.cur_texture_index >= \
                    self.char_stats["textures_hurt_nr"] * self.char_stats["animation_hurt_speed"]:
                self.cur_texture_index = 0
                self.char_stats["is_hit"] = False
            self.texture = self.char_stats["textures_hurt"][self.cur_texture_index // self.char_stats["animation_hurt_speed"]][self.player_variables["face_direction"]]
        self.char_stats["animation_last_state"] = self.char_stats["animation_cur_state"]

    def behavior(self, delta_time):
        if self.player_variables["is_moving"]:
            self.moving(self.player_variables["moving_dest_x"],
                        self.player_variables["moving_dest_y"],
                        delta_time)
        elif self.char_stats["is_hit"]:
            self.get_hurt(delta_time)
        else:
            self.idle_animation(delta_time)

    def on_update(self, delta_time: float = 1 / 60):
        self.behavior(delta_time)
