import arcade
import math
import random
from general.func import load_texture_pair_mod, add_exp
from general.const import ENEMY_STATS


def load_enemy_stats(enemy_class):
    enemy_stats = ENEMY_STATS[enemy_class].copy()
    return enemy_stats


class Enemy(arcade.Sprite):
    def __init__(self, enemy_class, player):
        super().__init__()
        self.personal_id = None
        self.enemy_stats = load_enemy_stats(enemy_class)
        self.player = player
        self.scale = self.enemy_stats["scale"]
        self.cur_texture_index = self.enemy_stats["animation_cur_state"]

        textures_type = ["walk", "idle", "attack", "hurt", "dying"]
        for texture_type in textures_type:
            self.enemy_stats[f"textures_{texture_type}"], self.enemy_stats[f"textures_{texture_type}_nr"] = \
                load_texture_pair_mod(self.enemy_stats["graphic_location"] + self.enemy_stats[f"textures_{texture_type}_file"],
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

        self.animation("walk", delta_time)
        self.enemy_stats["animation_last_state"] = self.enemy_stats["animation_cur_state"]

    def go_to_point(self, _x=None, _y=None):
        self.enemy_stats["dest_x"] = _x
        self.enemy_stats["dest_y"] = _y

    def go_to_player(self, _x, _y):
        if arcade.get_distance_between_sprites(self.player, self) < 80:
            self.attack()
            print("zaatakowalem", self.personal_id)
        else:
            self.enemy_stats["is_moving"] = True
            self.go_to_point(_x, _y)

    @property
    def damage(self):
        damage = random.randint(self.enemy_stats["dmg_min"], self.enemy_stats["dmg_max"])
        return damage

    def make_damage(self):
        if self.player.center_x > self.center_x:
            self.enemy_stats["face_direction"] = 0
        else:
            self.enemy_stats["face_direction"] = 1
        if self.player.char_stats["actual_health_points"] - self.damage > 0:
            self.player.char_stats["actual_health_points"] -= self.damage
        else:
            self.player.char_stats["actual_health_points"] = 0
        self.player.char_stats["is_hit"] = True

    def attack(self):
        self._stop()
        self.enemy_stats["is_attacking"] = True

    def go_around(self, delta_time):
        if self.walking_timer > self.randomized_number * 60 * delta_time:
            center_x_int = int(self.enemy_stats["initial_x"])
            center_y_int = int(self.enemy_stats["initial_y"])
            random_x = random.randint(center_x_int-self.enemy_stats["radius"], center_x_int + self.enemy_stats["radius"])
            random_y = random.randint(center_y_int-self.enemy_stats["radius"], center_y_int + self.enemy_stats["radius"])
            self.go_to_point(random_x, random_y)
            self.walking_timer = 0
            self.randomized_number = random.randrange(3, 8)

    # def idle_animation(self, delta_time):
    #     if not self.enemy_stats["is_attacking"]:
    #         self.enemy_stats["animation_cur_state"] = 0
    #         self._check_a_state()
    #         self.cur_texture_index += 1
    #         if self.cur_texture_index >= \
    #                 self.enemy_stats["textures_idle_nr"] * self.enemy_stats["animation_idle_speed"]:
    #             self.cur_texture_index = 0
    #         self.texture = self.enemy_stats["textures_idle"][self.cur_texture_index // self.enemy_stats["animation_idle_speed"]][self.enemy_stats["face_direction"]]
    #         self.enemy_stats["animation_last_state"] = self.enemy_stats["animation_cur_state"]
    #
    # def walk_animation(self, delta_time):
    #     if self.enemy_stats["is_moving"]:
    #         self.enemy_stats["animation_cur_state"] = 1
    #         self._check_a_state()
    #         self.cur_texture_index += 1
    #         if self.cur_texture_index >= \
    #                 self.enemy_stats["textures_walk_nr"] * self.enemy_stats["animation_walk_speed"]:
    #             self.cur_texture_index = 0
    #         self.texture = self.enemy_stats["textures_walk"] \
    #         [self.cur_texture_index // self.enemy_stats["animation_walk_speed"]][self.enemy_stats["face_direction"]]
    #         self.enemy_stats["animation_last_state"] = self.enemy_stats["animation_cur_state"]
    #
    # def attack_animation(self):
    #     if self.enemy_stats["is_attacking"]:
    #         self.enemy_stats["animation_cur_state"] = 2
    #         self._check_a_state()
    #         self.cur_texture_index += 1
    #         if self.cur_texture_index == self.enemy_stats["attack_frame"] * self.enemy_stats["animation_attack_speed"]:
    #             self.make_damage()
    #         if self.cur_texture_index >= self.enemy_stats["textures_attack_nr"] * self.enemy_stats["animation_attack_speed"]:
    #             self.cur_texture_index = 1
    #         self.texture = self.enemy_stats["textures_attack"][self.cur_texture_index // self.enemy_stats["animation_attack_speed"]][self.enemy_stats["face_direction"]]
    #         self.enemy_stats["is_attacking"] = False
    #         self.enemy_stats["animation_last_state"] = self.enemy_stats["animation_cur_state"]
    #
    # def get_hurt(self, delta_time):
    #     if self.enemy_stats["is_hit"]:
    #         self.enemy_stats["animation_cur_state"] = 3
    #         self._check_a_state()
    #         self.cur_texture_index += 1
    #         if self.cur_texture_index >= \
    #                 self.enemy_stats["textures_hurt_nr"] * self.enemy_stats["animation_hurt_speed"]:
    #             self.cur_texture_index = 0
    #             self.enemy_stats["is_hit"] = False
    #         self.texture = self.enemy_stats["textures_hurt"][self.cur_texture_index // self.enemy_stats["animation_hurt_speed"]][self.enemy_stats["face_direction"]]
    #     self.enemy_stats["animation_last_state"] = self.enemy_stats["animation_cur_state"]
    #
    # def die(self, delta_time):
    #     self.hit_box = [[1,1], [1,0], [0, 1]]
    #     self.enemy_stats["animation_cur_state"] = 4
    #     self._check_a_state()
    #     self.cur_texture_index += 1
    #     if self.cur_texture_index >= \
    #             self.enemy_stats["textures_dying_nr"] * self.enemy_stats["animation_dying_speed"]:
    #         self.cur_texture_index = 0
    #         add_exp(self.player, self)
    #         self.kill()
    #     self.texture = self.enemy_stats["textures_dying"][self.cur_texture_index // self.enemy_stats["animation_dying_speed"]][self.enemy_stats["face_direction"]]
    #     self.enemy_stats["animation_last_state"] = self.enemy_stats["animation_cur_state"]

    def animation(self, animation_type, delta_time):
        animation_ = ["idle", "walk", "attack", "hurt", "dying"]
        what_type = animation_type if animation_type in animation_ else None
        if what_type:
            self.enemy_stats["animation_cur_state"] = animation_.index(what_type)
            self._check_a_state()
            self.cur_texture_index += 1
            if what_type == "attack":
                if self.cur_texture_index == self.enemy_stats["attack_frame"] * self.enemy_stats["animation_attack_speed"]:
                    self.make_damage()
                    self.enemy_stats["is_hit"] = False
            elif what_type == "dying":
                self.hit_box = [[1, 1], [1, 0], [0, 1]]
            if self.cur_texture_index >= self.enemy_stats[f"textures_{what_type}_nr"] \
                    * self.enemy_stats[f"animation_{what_type}_speed"]:
                self.cur_texture_index = 0
                if what_type == "attack":
                    self.enemy_stats["is_attacking"] = False
                elif what_type == "hurt":
                    self.enemy_stats["is_hit"] = False
                elif what_type == "dying":
                    add_exp(self.player, self)
                    self.kill()
            self.texture = self.enemy_stats[f"textures_{what_type}"][self.cur_texture_index // self.enemy_stats[f"animation_{what_type}_speed"]][self.enemy_stats["face_direction"]]
        self.enemy_stats["animation_last_state"] = self.enemy_stats["animation_cur_state"]

    # def behavior(self, delta_time):
    #     if self.enemy_stats["actual_health_points"] <= 0:
    #         self.die(delta_time)
    #         return
    #     elif self.enemy_stats["is_attacking"]:
    #         self.attack_animation()
    #     elif self.enemy_stats["is_hit"]:
    #         self.get_hurt(delta_time)
    #         return
    #     if self.enemy_stats["dest_x"] is not None and self.enemy_stats["dest_y"] is not None:
    #         self.enemy_stats["is_moving"] = True
    #         self.moving(_x=self.enemy_stats["dest_x"], _y=self.enemy_stats["dest_y"], delta_time=delta_time)
    #     elif self.enemy_stats["player_in_radius"]:
    #         self.go_to_player(self.player.center_x, self.player.center_y)
    #     elif not self.enemy_stats["player_in_radius"]:
    #         self.go_around(delta_time)
    #
    #     if not self.enemy_stats["is_moving"] and not self.enemy_stats["is_attacking"] and not self.enemy_stats["is_hit"]:
    #         self.idle_animation(delta_time)

    def behavior(self, delta_time):
        if self.enemy_stats["actual_health_points"] <= 0:
            self.animation("dying", delta_time)
            return
        elif self.enemy_stats["is_attacking"]:
            self.animation("attack", delta_time)
        elif self.enemy_stats["is_hit"]:
            self.animation("hurt", delta_time)
            return
        if self.enemy_stats["dest_x"] is not None and self.enemy_stats["dest_y"] is not None:
            self.enemy_stats["is_moving"] = True
            self.moving(_x=self.enemy_stats["dest_x"], _y=self.enemy_stats["dest_y"], delta_time=delta_time)
        elif self.enemy_stats["player_in_radius"] and not self.enemy_stats["is_attacking"]:
            self.go_to_player(self.player.center_x, self.player.center_y)
        elif not self.enemy_stats["player_in_radius"]:
            self.go_around(delta_time)

        if not self.enemy_stats["is_moving"] and not self.enemy_stats["is_attacking"] and not self.enemy_stats["is_hit"]:
            self.animation("idle", delta_time)

    def on_update(self, delta_time: float = 1 / 60):
        self.behavior(delta_time)
        self.walking_timer += delta_time

