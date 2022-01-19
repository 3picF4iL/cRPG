import arcade
import math
import random
from general.func import load_texture_pair_mod
from general.const import ENEMY_STATS


def load_enemy_stats(enemy_class):
    enemy_stats = ENEMY_STATS[enemy_class].copy()
    return enemy_stats


class Enemy(arcade.Sprite):
    def __init__(self, enemy_class, player):
        super().__init__()
        #self.additional_settings = {}
        self.personal_id = None
        self.enemy_stats = load_enemy_stats(enemy_class)
        self.player = player
        self.scale = self.enemy_stats["scale"]
        self.cur_texture_index = self.enemy_stats["animation_cur_state"]

        self.enemy_stats["textures_walk"], self.enemy_stats["textures_walk_nr"] = \
            load_texture_pair_mod(self.enemy_stats["graphic_location"] + self.enemy_stats["textures_walk_file"],
                                  720, 0, 490)

        self.enemy_stats["textures_idle"], self.enemy_stats["textures_idle_nr"] = \
            load_texture_pair_mod(self.enemy_stats["graphic_location"] + self.enemy_stats["textures_idle_file"],
                                  720, 0, 490)

        self.enemy_stats["textures_attack"], self.enemy_stats["textures_attack_nr"] = \
            load_texture_pair_mod(self.enemy_stats["graphic_location"] + self.enemy_stats["textures_attack_file"],
                                  720, 0, 490)

        self.walking_timer = 0
        self.randomized_number = random.randrange(3, 8)
        self.hit_box = ([-100, -200], [-100, -100], [100, -100], [100, -200])

    def face_dir_change(self, x):
        if x > 0:
            self.enemy_stats["face_direction"] = 0
        elif x < 0:
            self.enemy_stats["face_direction"] = 1

    def _check_a_state(self):
        if self.enemy_stats["animation_cur_state"] != self.enemy_stats["animation_last_state"]:
            self.cur_texture_index = 0

    def is_player_in_radius(self):
        if self.player.center_x <= self.center_x + self.enemy_stats["radius"] or \
                self.player.center_y <= self.center_y + self.enemy_stats["radius"]:
            self.enemy_stats["player_in_radius"] = True
        else:
            self.enemy_stats["player_in_radius"] = False

    def _stop(self):
        self.enemy_stats["is_moving"] = False
        self.enemy_stats["dest_x"] = None
        self.enemy_stats["dest_y"] = None

    def moving(self, _x, _y, delta_time):
        _x, _y = self.enemy_stats["dest_x"], self.enemy_stats["dest_y"]
        x_diff, y_diff = _x - self.center_x, _y - self.center_y

        angle = math.atan2(y_diff, x_diff)
        self.center_x += math.cos(angle) * self.enemy_stats["mvm"] * delta_time
        self.center_y += math.sin(angle) * self.enemy_stats["mvm"] * delta_time

        self.face_dir_change(x_diff)
        if math.fabs(round(x_diff)) <= 1 and math.fabs(round(y_diff)) <= 1:
            self._stop()

        self.walk_animation(delta_time)
        self.enemy_stats["animation_last_state"] = self.enemy_stats["animation_cur_state"]

    def go_to_point(self, _x=None, _y=None):
        self.enemy_stats["dest_x"] = _x
        self.enemy_stats["dest_y"] = _y

    def go_to_player(self, _x, _y):
        if arcade.get_distance_between_sprites(self.player, self) < 60:
            self.attack()
        else:
            self.enemy_stats["is_moving"] = True
            self.go_to_point(_x, _y)

    @property
    def damage(self):
        damage = random.randint(self.enemy_stats["dmg_min"], self.enemy_stats["dmg_max"])
        return damage

    def make_damage(self):
        self.player.char_stats["actual_health_points"] -= self.damage
        self.player.char_stats["is_hit"] = True

    def attack(self):
        self._stop()
        self.enemy_stats["is_attacking"] = True

    def go_around(self, delta_time):
        if self.walking_timer > self.randomized_number * 60 * delta_time:
            center_x_int = int(self.enemy_stats["initial_x"])
            center_y_int = int(self.enemy_stats["initial_y"])
            random_x = random.randint(center_x_int+100, center_x_int + self.enemy_stats["radius"])
            random_y = random.randint(center_y_int+100, center_y_int + self.enemy_stats["radius"])
            self.go_to_point(random_x, random_y)
            self.walking_timer = 0
            self.randomized_number = random.randrange(3, 8)

    def idle_animation(self, delta_time):
        if not self.enemy_stats["is_attacking"]:
            self.enemy_stats["animation_cur_state"] = 0
            self._check_a_state()
            self.cur_texture_index += 1
            if self.cur_texture_index >= \
                    self.enemy_stats["textures_idle_nr"] * self.enemy_stats["animation_idle_speed"]:
                self.cur_texture_index = 0
            self.texture = self.enemy_stats["textures_idle"][self.cur_texture_index // self.enemy_stats["animation_idle_speed"]][self.enemy_stats["face_direction"]]
            self.enemy_stats["animation_last_state"] = self.enemy_stats["animation_cur_state"]

    def walk_animation(self, delta_time):
        if self.enemy_stats["is_moving"]:
            self.enemy_stats["animation_cur_state"] = 1
            self._check_a_state()
            self.cur_texture_index += 1
            if self.cur_texture_index >= \
                    self.enemy_stats["textures_walk_nr"] * self.enemy_stats["animation_walk_speed"]:
                self.cur_texture_index = 0
            self.texture = self.enemy_stats["textures_walk"] \
            [self.cur_texture_index // self.enemy_stats["animation_walk_speed"]][self.enemy_stats["face_direction"]]
            self.enemy_stats["animation_last_state"] = self.enemy_stats["animation_cur_state"]

    def attack_animation(self):
        if self.enemy_stats["is_attacking"]:
            self.enemy_stats["animation_cur_state"] = 2
            self._check_a_state()
            self.cur_texture_index += 1
            if self.cur_texture_index == self.enemy_stats["attack_frame"] * self.enemy_stats["animation_attack_speed"]:
                self.make_damage()
            if self.cur_texture_index >= self.enemy_stats["textures_attack_nr"] * self.enemy_stats["animation_attack_speed"]:
                self.cur_texture_index = 1
            self.texture = self.enemy_stats["textures_attack"][self.cur_texture_index // self.enemy_stats["animation_attack_speed"]][self.enemy_stats["face_direction"]]
            self.enemy_stats["is_attacking"] = False
            self.enemy_stats["animation_last_state"] = self.enemy_stats["animation_cur_state"]

    def behavior(self, delta_time):

        if self.enemy_stats["is_attacking"]:
            self.attack_animation()

        if not self.enemy_stats["player_in_radius"]:
            self.go_around(delta_time)
        else:
            self.go_to_player(self.player.center_x, self.player.center_y)

        if self.enemy_stats["dest_x"] is not None and self.enemy_stats["dest_y"] is not None:
            self.enemy_stats["is_moving"] = True
            self.moving(_x=self.enemy_stats["dest_x"], _y=self.enemy_stats["dest_y"], delta_time=delta_time)
        else:
            self.enemy_stats["is_moving"] = False
            self.idle_animation(delta_time)

    def on_update(self, delta_time: float = 1 / 60):
        self.behavior(delta_time)

        self.walking_timer += delta_time
        pass
