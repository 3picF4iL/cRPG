import arcade
import math
import random
from general.func import add_exp
from general.const import ENEMY_STATS
from ..entity_function import load_textures, face_dir_change, check_state, damage


def load_enemy_stats(enemy_class):
    enemy_stats = ENEMY_STATS[enemy_class].copy()
    return enemy_stats


class Enemy(arcade.Sprite):
    def __init__(self, enemy_class, player):
        super().__init__()
        self.personal_id = None
        self.variables = load_enemy_stats(enemy_class)
        self.player = player
        self.scale = self.variables["scale"]
        self.cur_texture_index = self.variables["animation_cur_state"]

        textures_type = ["walk", "idle", "attack", "hurt", "dying"]
        load_textures(textures_type, self.variables)

        self.walking_timer = 0
        self.randomized_number = random.randrange(3, 8)

        self.hit_box = ([-100, -200], [-100, -100], [100, -100], [100, -200])

    def is_player_in_radius(self):
        if self.player.center_x <= self.center_x + self.variables["radius"] or \
                self.player.center_y <= self.center_y + self.variables["radius"]:
            self.variables["player_in_radius"] = True
        else:
            self.variables["player_in_radius"] = False

    def _stop(self):
        self.variables["is_moving"] = False
        self.variables["dest_x"] = None
        self.variables["dest_y"] = None

    def moving(self, _x, _y, delta_time):
        _x, _y = self.variables["dest_x"], self.variables["dest_y"]
        x_diff, y_diff = _x - self.center_x, _y - self.center_y

        angle = math.atan2(y_diff, x_diff)
        self.center_x += math.cos(angle) * self.variables["mvm"] * delta_time
        self.center_y += math.sin(angle) * self.variables["mvm"] * delta_time

        face_dir_change(self.variables, x_diff)
        if math.fabs(round(x_diff)) <= 1 and math.fabs(round(y_diff)) <= 1:
            self._stop()

        self.walk_animation(delta_time)
        self.variables["animation_last_state"] = self.variables["animation_cur_state"]

    def go_to_point(self, _x=None, _y=None):
        self.variables["dest_x"] = _x
        self.variables["dest_y"] = _y

    def go_to_player(self, _x, _y):
        if arcade.get_distance_between_sprites(self.player, self) < 80:
            self.attack()
        else:
            self.variables["is_moving"] = True
            self.go_to_point(_x, _y)

    def make_damage(self):
        if self.player.center_x > self.center_x:
            self.variables["face_direction"] = 0
        else:
            self.variables["face_direction"] = 1
        if self.player.variables["actual_health_points"] - damage(self) > 0:
            self.player.variables["actual_health_points"] -= damage(self)
        else:
            self.player.variables["actual_health_points"] = 0
        self.player.variables["is_hit"] = True

    def attack(self):
        self._stop()
        self.variables["is_attacking"] = True

    def go_around(self, delta_time):
        if self.walking_timer > self.randomized_number * 60 * delta_time:
            center_x_int = int(self.variables["initial_x"])
            center_y_int = int(self.variables["initial_y"])
            random_x = random.randint(center_x_int - self.variables["radius"], center_x_int + self.variables["radius"])
            random_y = random.randint(center_y_int - self.variables["radius"], center_y_int + self.variables["radius"])
            self.go_to_point(random_x, random_y)
            self.walking_timer = 0
            self.randomized_number = random.randrange(3, 8)

    def idle_animation(self, delta_time):
        if not self.variables["is_attacking"]:
            self.variables["animation_cur_state"] = 0
            check_state(self)
            self.cur_texture_index += 1
            if self.cur_texture_index >= \
                    self.variables["textures_idle_nr"] * self.variables["animation_idle_speed"]:
                self.cur_texture_index = 0
            self.texture = self.variables["textures_idle"][self.cur_texture_index // self.variables["animation_idle_speed"]][self.variables["face_direction"]]
            self.variables["animation_last_state"] = self.variables["animation_cur_state"]

    def walk_animation(self, delta_time):
        if self.variables["is_moving"]:
            self.variables["animation_cur_state"] = 1
            check_state(self)
            self.cur_texture_index += 1
            if self.cur_texture_index >= \
                    self.variables["textures_walk_nr"] * self.variables["animation_walk_speed"]:
                self.cur_texture_index = 0
            self.texture = self.variables["textures_walk"] \
            [self.cur_texture_index // self.variables["animation_walk_speed"]][self.variables["face_direction"]]
            self.variables["animation_last_state"] = self.variables["animation_cur_state"]

    def attack_animation(self):
        if self.variables["is_attacking"]:
            self.variables["animation_cur_state"] = 2
            check_state(self)
            self.cur_texture_index += 1
            if self.cur_texture_index == self.variables["attack_frame"] * self.variables["animation_attack_speed"]:
                self.make_damage()
            if self.cur_texture_index >= self.variables["textures_attack_nr"] * self.variables["animation_attack_speed"]:
                self.cur_texture_index = 1
            self.texture = self.variables["textures_attack"][self.cur_texture_index // self.variables["animation_attack_speed"]][self.variables["face_direction"]]
            self.variables["is_attacking"] = False
            self.variables["animation_last_state"] = self.variables["animation_cur_state"]

    def get_hurt(self, delta_time):
        if self.variables["is_hit"]:
            self.variables["animation_cur_state"] = 3
            check_state(self)
            self.cur_texture_index += 1
            if self.cur_texture_index >= \
                    self.variables["textures_hurt_nr"] * self.variables["animation_hurt_speed"]:
                self.cur_texture_index = 0
                self.variables["is_hit"] = False
            self.texture = self.variables["textures_hurt"][self.cur_texture_index // self.variables["animation_hurt_speed"]][self.variables["face_direction"]]
        self.variables["animation_last_state"] = self.variables["animation_cur_state"]

    def die(self, delta_time):
        self.hit_box = [[1,1], [1,0], [0, 1]]
        self.variables["animation_cur_state"] = 4
        check_state(self)
        self.cur_texture_index += 1
        if self.cur_texture_index >= \
                self.variables["textures_dying_nr"] * self.variables["animation_dying_speed"]:
            self.cur_texture_index = 0
            add_exp(self.player, self)
            self.kill()
        self.texture = self.variables["textures_dying"][self.cur_texture_index // self.variables["animation_dying_speed"]][self.variables["face_direction"]]
        self.variables["animation_last_state"] = self.variables["animation_cur_state"]

    def behavior(self, delta_time):
        if self.variables["actual_health_points"] <= 0:
            self.die(delta_time)
            return
        elif self.variables["is_attacking"]:
            self.attack_animation()
        elif self.variables["is_hit"]:
            self.get_hurt(delta_time)
            return
        if self.variables["dest_x"] is not None and self.variables["dest_y"] is not None:
            self.variables["is_moving"] = True
            self.moving(_x=self.variables["dest_x"], _y=self.variables["dest_y"], delta_time=delta_time)
        elif self.variables["player_in_radius"]:
            self.go_to_player(self.player.center_x, self.player.center_y)
        elif not self.variables["player_in_radius"]:
            self.go_around(delta_time)

        if not self.variables["is_moving"] and not self.variables["is_attacking"] and not self.variables["is_hit"]:
            self.idle_animation(delta_time)

    def on_update(self, delta_time: float = 1 / 60):
        self.behavior(delta_time)
        self.walking_timer += delta_time

