import arcade
from .const import player_map1_opt, MOVEMENT_KEYS


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
        # Load textures for idle standing
        self.idle_texture_pair = arcade.load_texture_pair(player_map1_opt["graphic_location"])
        self.texture = self.idle_texture_pair[0]
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

        if self.player_variables["move_left"]:
            self.center_x = self.center_x - self.player_variables["movement_speed"] * delta_time

        if not self.player_variables["move_up"] and not self.player_variables["move_down"]:
            self.change_y = 0
        if not self.player_variables["move_right"] and not self.player_variables["move_left"]:
            self.change_x = 0

        if self.player_variables["move_up"] or self.player_variables["move_down"] or \
                self.player_variables["move_right"] or self.player_variables["move_left"]:
            self.player_variables["is_moving"] = True
        else:
            self.player_variables["is_moving"] = False

    def on_update(self, delta_time: float = 1 / 60):
        self.move(delta_time)


