import os
import math
from random import randint
import arcade


class Enemy(arcade.Sprite):
    def __init__(self, player, items):
        super().__init__()

        self.stats = ENEMY_1
        self.print_damage = False
        enemy_texture_path = "./graphic/animations/enemies/monster_1"
        self.character_face_direction = randint(0, 1)
        self.center_x = ENEMY1_STAT["initial_coords"][0]
        self.center_y = ENEMY1_STAT["initial_coords"][1]
        self.scale = SPRITE_SCALING_PLAYER * 0.9
        self.animation_walk_speed = 4
        self.animation_attack_speed = 5
        self.cur_texture_index = 0
        self.player = player
        self.items = items

        self.walk_textures_amount = len(os.listdir(f"{enemy_texture_path}/walk/"))
        self.attack_textures_amount = len(os.listdir(f"{enemy_texture_path}/attack/"))
        self.die_textures_amount = len(os.listdir(f"{enemy_texture_path}/die/"))
        self.idle_textures_amount = len(os.listdir(f"{enemy_texture_path}/idle/"))

        # Idle texture
        self.idle_textures = []
        for i in range(1, self.idle_textures_amount+1):
            texture = arcade.load_texture_pair(f"{enemy_texture_path}/idle/idle{i}.png",
                                               hit_box_algorithm='Simple')
            self.idle_textures.append(texture)

        # Walk textures
        self.walk_textures = []
        for i in range(1, self.walk_textures_amount+1):
            texture = arcade.load_texture_pair(f"{enemy_texture_path}/walk/walk{i}.png",
                                               hit_box_algorithm='Simple')
            self.walk_textures.append(texture)

        # Attack textures
        self.attack_textures = []
        for i in range(1, self.attack_textures_amount+1):
            texture = arcade.load_texture_pair(f"{enemy_texture_path}/attack/attack{i}.png",
                                               hit_box_algorithm='Simple')
            self.attack_textures.append(texture)

        # Die textures
        self.die_textures = []
        for i in range(1, self.die_textures_amount+1):
            texture = arcade.load_texture_pair(f"{enemy_texture_path}/die/die{i}.png",
                                               hit_box_algorithm='Simple')
            self.die_textures.append(texture)

        self.hit_box = ([-100, -200], [-100, 0], [100, 0], [100, -200])

    @property
    def damage(self):
        damage = randint(self.enemy_general["dmg_min"], self.enemy_general["dmg_max"])
        return damage

    def get_hit(self, value):
        if not self.is_hit:
            if self.actual_health_points - value <= 0:
                self.actual_health_points = 0
                self.is_killed = True
                return True
            self.actual_health_points -= value
            self.is_hit = True
        return False

    def draw_info(self):
        # arcade.draw_text(f"X:{self.center_x} Y: {self.center_y}", self.center_x-20, self.center_y+40,
        #                  [0, 0, 0], 7, 100)
        green = arcade.color.GREEN
        red = arcade.color.RED
        black = arcade.color.BLACK
        bar_width = 40
        bar_offset = 40
        bar_height = 3
        # ==========
        # HEALTH
        # ==========
        arcade.draw_text(f"HP: {self.actual_health_points}/{self.max_hp}",
                         self.center_x-30, self.center_y+43, black, 7, 5)
        arcade.draw_text(f"Exp: {self.enemy_misc['exp']}", self.center_x-30,
                         self.center_y+50, black, 7, 5)

        # Draw the 'unhealthy' background
        if self.actual_health_points < self.max_hp:
            arcade.draw_rectangle_filled(center_x=self.center_x,
                                         center_y=self.center_y + bar_offset,
                                         width=bar_width,
                                         height=bar_height,
                                         color=red)
        # Calculate width based on health
        health_width = bar_width * (self.actual_health_points / self.max_hp)

        arcade.draw_rectangle_filled(center_x=self.center_x - 0.5 * (bar_width - health_width),
                                     center_y=self.center_y + bar_offset,
                                     width=health_width,
                                     height=bar_height,
                                     color=green)

    def patrol(self, _to_x, *args):

        _from_x = ENEMY1_STAT["initial_coords"][0]
        _from_y = ENEMY1_STAT["initial_coords"][1]
        if len(args) != 0:
            _to_y = args[0]
        else:
            _to_y = self.center_y

        # _to_x -- ONE POINT (y is the same)
        # _from_x -- ONE POINT (y is the same)
        if self.direction_change_x and self.go_to_point(_to_x, _to_y):
            self.direction_change_x = False
            return
        elif not self.direction_change_x and self.go_to_point(_from_x, _to_y):
            self.direction_change_x = True
            return

    def start(self):
        if not self.is_walking:
            self.is_walking = True
            if self.direction_change_x:
                if self.change_x == 0:
                    self.change_x = self.movement_speed
            else:
                if self.change_x == 0:
                    self.change_x = -self.movement_speed

            if self.direction_change_y:
                if self.change_y == 0:
                    self.change_y = self.movement_speed
            else:
                if self.change_y == 0:
                    self.change_y = -self.movement_speed

    def stop(self):
        super().stop()
        if self.is_walking:
            self.is_walking = False

    def follow_player(self):
        enemy_x = self.center_x
        enemy_y = self.center_y
        player_x = self.player.center_x
        player_y = self.player.center_y

        self.start()

        if arcade.get_distance_between_sprites(self, self.player) < 50:
            self.stop()
            self.attack_player()
            return

        x_diff = player_x - enemy_x
        y_diff = player_y - enemy_y
        angle = math.atan2(y_diff, x_diff)
        self.change_x = math.cos(angle) * self.movement_speed
        self.change_y = math.sin(angle) * self.movement_speed
        self.velocity = [self.change_x, self.change_y]

    def go_to_point(self, _x, _y):
        enemy_x = self.center_x
        enemy_y = self.center_y
        goto_x = _x
        goto_y = _y

        self.start()

        x_diff = goto_x - enemy_x
        y_diff = goto_y - enemy_y
        if math.fabs(round(x_diff)) <= 1 and math.fabs(round(y_diff)) <= 1:
            self.stop()
            return True
        angle = math.atan2(y_diff, x_diff)
        self.change_x = math.cos(angle) * self.movement_speed
        self.change_y = math.sin(angle) * self.movement_speed

    def attack_player(self):
        if not self.is_attacking:
            self.is_attacking = True

    def _attack(self):
        if self.is_attacking:
            self.cur_texture_index += 1
            if self.cur_texture_index >= self.attack_textures_amount * self.animation_attack_speed:
                self.is_attacking = False
                self.cur_texture_index = 1
                self.player.is_hit = False
            self.texture = self.attack_textures[self.cur_texture_index
                                                // self.animation_attack_speed][self.character_face_direction]

    def _walk(self):
        if self.is_walking:
            self.cur_texture_index += 1
            if self.cur_texture_index >= self.walk_textures_amount * self.animation_walk_speed:
                self.cur_texture_index = 1
            self.texture = self.walk_textures[self.cur_texture_index
                                              // self.animation_walk_speed][self.character_face_direction]

    def _face_change(self):
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

    def _idle(self):
        idle_speed = 4
        if self.change_x == 0 and \
                self.change_y == 0 and \
                not self.is_attacking and \
                not self.is_walking and \
                not self.is_killed:
            self.cur_texture_index += 1
            if self.cur_texture_index >= self.idle_textures_amount * idle_speed:
                self.cur_texture_index = 0
            self.texture = self.idle_textures[self.cur_texture_index
                                              // idle_speed][self.character_face_direction]
            return

    def _die(self):
        dying_speed = 4
        if self.is_killed:
            self.is_attacking = False
            self.is_hit = False
            self.stop()
            self.cur_texture_index += 1
            if self.cur_texture_index >= self.die_textures_amount * dying_speed:
                self.cur_texture_index = 0
                self.is_killed = False
                if self._spawn_item() is not None or "":
                    self.items.append(self._spawn_item())
                self.kill()
            self.texture = self.die_textures[self.cur_texture_index // dying_speed][self.character_face_direction]

    def _spawn_item(self):
        item = generate_item(self.player,
                             input_x=self.center_x,
                             input_y=self.center_y - 50)
        if item is not None:
            print(item.item_name)
            return item

    def _behavior(self):
        if not self.player_in_radius and not self.is_patrol:
            self.go_to_point(self.center_x, self.center_y)
        elif not self.player_in_radius and self.is_patrol:
            self.patrol(500)
        else:
            self.follow_player()

    def update_animation(self, delta_time: float = 1 / 60):
        # Figure out if we need to flip face left or right
        self._face_change()

        # Idle animation
        self._idle()

        # Walking
        self._walk()

        # Attacking animation
        self._attack()

        # Die
        self._die()

        self._behavior()
