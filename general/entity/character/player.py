import math
import arcade
from general.const import player_map1_opt
from general.func import get_map_point
from general.gui import GUI
from general.entity.character.default_char import CharClass
from ..entity_function import load_textures, face_dir_change, check_state, damage


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
        self.target = None
        self.timer = 0

        textures_type = ["walk", "idle", "attack", "hurt"]
        load_textures(textures_type, self.variables)

        self.hit_box = ([-100, -200], [-100, -100], [100, -100], [100, -200])

    def click_event(self, click_x, click_y, enemy_list, wall_list):
        """
        Method for decide what to do after clicking on a some map point\n
        If clicked on the enemy and enemy is out of radius -> go to enemy and attack right after\n
        If clicked on the enemy and enemy is in attack radius -> attack\n
        If clicked on the obstacle -> go to obstacle but stop right before\n
        If clicked on the obstacle when already stand by it -> do nothing\n

        :param click_x: parameter where player clicked on the map (x)- unfortunately those coords are window coords
         not a map coords so we need to recalculate it with get_map_point function
        :param click_y: parameter where player clicked on the map (y) - as same as above
        :param enemy_list: passing enemy_list to compare with coordinates and get clicked-on Sprite of the enemy
        :param wall_list: passing wall_list to compare with coordinates and get clicked-on Sprite of the wall to avoid walk loop
        """
        _x, _y = get_map_point([click_x, click_y], [self.center_x, self.center_y])
        enemies = arcade.get_sprites_at_point([_x, _y], enemy_list)
        obstacles = arcade.get_sprites_at_point([_x, _y], wall_list)
        if obstacles:
            print("USTAWIENIE COORDYNATOW")
            #_x, _y = self.where_can_go(obstacles[0])
        elif enemies:
            distance_between_player_enemy = arcade.get_distance(enemies[0].center_x,
                                                                enemies[0].center_y,
                                                                self.center_x,
                                                                self.center_y)

            if distance_between_player_enemy < self.height/2 + enemies[0].height/2:
                self._attack(enemies[0])
                print("FUNKCJA ATAKU")
                return
        else:
            _y = _y + (self.height/2) - 10
        print("FUNKCJA CHODZENIA: ide do: ", _x, _y)
        self._start(_x, _y)

    def _start(self, dest_x, dest_y):
        print("start")
        self.variables["is_moving"] = True
        self.variables["moving_dest_x"] = dest_x
        self.variables["moving_dest_y"] = dest_y
        face_dir_change(self.variables, self.variables["moving_dest_x"] - self.center_x)

    def _stop(self):
        self.timer = 0
        self.variables["is_moving"] = False
        self.variables["moving_dest_x"] = None
        self.variables["moving_dest_y"] = None

    def func_keys(self, key, mod):
        if key == arcade.key.TAB:
            self.player_variables["is_show_stats"] = False if self.player_variables["is_show_stats"] else True
        elif mod == arcade.key.MOD_ALT:
            self.player_variables["is_attacking"] = True

    def _attack(self, enemy):
        self.variables["is_attacking"] = True
        self.target = enemy

    def attack(self, delta_time):
        self._stop()
        self.animation("attack", delta_time, self.target)

    def make_damage(self, enemy):
        if not enemy:
            return
        if enemy.center_x > self.center_x:
            self.variables["face_direction"] = 0
        else:
            self.variables["face_direction"] = 1
        if enemy.variables["actual_health_points"] - damage(self) > 0:
            enemy.variables["actual_health_points"] -= damage(self)
        else:
            enemy.variables["actual_health_points"] = 0
        enemy.variables["is_hit"] = True

    def moving(self, delta_time):
        print("ide")
        # self.timer += delta_time
        tmp_x = self.center_x
        tmp_y = self.center_y
        goto_x, goto_y = self.variables["moving_dest_x"], self.variables["moving_dest_y"]
        x_diff, y_diff = goto_x - self.center_x, goto_y - self.center_y

        angle = math.atan2(y_diff, x_diff)
        change_x = math.cos(angle) * self.player_variables["movement_speed"] * delta_time
        change_y = math.sin(angle) * self.player_variables["movement_speed"] * delta_time
        # print(change_x, change_y)
        self.center_x += change_x
        self.center_y += change_y
        self.animation("walk", delta_time)
        if math.fabs(round(x_diff)) <= 1 and math.fabs(round(y_diff)) <= 1:
            self._stop()

    def reset_animation_state(self):
        self.variables["is_hit"] = False

    def animation(self, animation_type, delta_time, enemy=None):
        animation_ = ["idle", "walk", "attack", "hurt", "dying"]
        what_type = animation_type if animation_type in animation_ else None
        if what_type:
            self.variables["animation_cur_state"] = animation_.index(what_type)
            check_state(self)
            self.cur_texture_index += 1
            if what_type == "attack":
                if self.cur_texture_index == self.variables["attack_frame"] * self.variables["animation_attack_speed"] and enemy is not None:
                    self.make_damage(enemy)
                    self.variables["is_hit"] = False
            if self.cur_texture_index >= self.variables[f"textures_{what_type}_nr"] \
                    * self.variables[f"animation_{what_type}_speed"]:
                self.cur_texture_index = 0
                if what_type == "attack":
                    self.variables["is_attacking"] = False
                elif what_type == "hurt":
                    self.variables["is_hit"] = False
            self.texture = self.variables[f"textures_{what_type}"][self.cur_texture_index // self.variables[f"animation_{what_type}_speed"]][self.variables["face_direction"]]
        self.variables["animation_last_state"] = self.variables["animation_cur_state"]

    def behavior(self, delta_time):

        if self.variables["is_attacking"]:
            self.attack(delta_time)
        elif self.variables["is_moving"]:
            self.moving(delta_time)
        elif self.variables["is_hit"]:
            self.animation("hurt", delta_time)
        else:
            self.animation("idle", delta_time)

    def on_update(self, delta_time: float = 1 / 60):
        self.behavior(delta_time)
