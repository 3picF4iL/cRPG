import os
import re
import arcade
import arcade.gui
import random
from arcade.arcade_types import Point
from win32api import GetKeyState, keybd_event
from win32con import VK_CAPITAL, VK_NUMLOCK, VK_SCROLL, KEYEVENTF_KEYUP
from typing import Tuple, Dict, Any, NoReturn, List
from .const import SCREEN_SIZE, TITLE, LAYER_NAME_PLAYER, LAYER_NAME_ENTITIES, \
    LAYER_NAME_ENEMIES, BG_COLOR, NEXT_LEVEL_EXP

_NEXT_LEVEL_EXP = NEXT_LEVEL_EXP


def get_key_from_value(dictionary: Dict, value) -> Any:  # Return key or keys from value
    """
    Function for getting key from provided value

    :param dictionary: Dictionary inside where we looking for a key
    :param value: Dictionary value for key finding
    :return: Key from dictionary if found, none if not found
    """
    for k, v in dictionary.items():
        if v == value:
            return k
    return None


def checking_lockkey_states() -> NoReturn:  # Checking states of keyboard buttons
    """
    Check and disable all lock keys like Num, Scroll and Caps lock
    Necessary for properly handle debug console (no modifier can be used)

    :return: No return
    """

    def disable_lockkey(
            key: int) -> NoReturn:  # Disable states of Caps Lock, Num Lock and Scroll Lock buttons on keyboard
        """
        Internal function for key state checking

        :param key: Key for keybd_event
        :return: No return
        """
        keybd_event(key, 0)
        keybd_event(key, 0, KEYEVENTF_KEYUP)
        pass

    keys = [VK_NUMLOCK,  # Num Lock
            VK_SCROLL,  # Scroll Lock
            VK_CAPITAL]  # Caps Lock

    for _key in keys:
        if GetKeyState(_key):
            disable_lockkey(_key)


def set_window_with_size(size: int = 1, *args) -> Any:
    """
    Sets window size from game settings or creates a new window object with desired size

    | 0 - small: 800x600
    | 1 - normal: 1024x786
    | 2 - large: 1920x1080
    | Default is 1 = normal

    :param size: type int: 0, 1, 2
    :param args: type waiting for window from arcade.Window
    :return: arcade window
    """
    if len(args) == 1:
        window = args[0]
    else:
        window = None

    screen_w = SCREEN_SIZE[size][0]
    screen_h = SCREEN_SIZE[size][1]

    if window is None:
        return arcade.Window(width=screen_w, height=screen_h, title=TITLE)
    window.set_size(screen_w, screen_h)


def set_sprites_in_spritelist(sprite_list):
    sprite_list.sort(key=lambda x: x.position[1], reverse=True)


def set_player(char_class: int, player, scene: Any) -> NoReturn:
    """
    Creating and inserting player object into player list (for future drawing)

    :param char_class: string with Char class name e.g. 0, mage, hunter etc.
    :param player: Player character
    :param scene: Actual scene
    :param p_list: Player list
    """

    player_ = player(char_class)
    scene.add_sprite(LAYER_NAME_PLAYER, player_, visible=False)
    scene.add_sprite(LAYER_NAME_ENTITIES, player_)


def set_enemies(filename: Any, enemy, scene: Any, player: Any) -> NoReturn:
    """
    Load file with enemy type, coords and stats. Set each enemy in requested place

    :param filename: string with path to filename contains placement of every enemy, stat and behavior on each map
    :param enemy: put every created enemy on that list
    :param scene: add enemy to scene to keep it for distance counting, collision etc.
    TODO: Function should be refactored for more enemy settings in future (like face direction, patrol, aggressiveness)
    """
    enemies = filename()
    """
    ID(0) AMOUNT(1)   RADIUS(2)     X(3)    Y(4)  Dest_X(5)   Dest_Y(6)  
    0       3           100         500     100     280         350
    """
    for _, line in enumerate(enemies.splitlines()):
        line = line.split()
        for i in range(1, int(line[1]) + 1):
            enemy_ = enemy(int(line[0]), player)
            enemy_.personal_id = _
            enemy_.center_x = random.randint(int(line[3]), int(line[3]) + int(line[2]))
            enemy_.center_y = random.randint(int(line[4]), int(line[4]) + int(line[2]))
            enemy_.variables["initial_x"] = enemy_.center_x
            enemy_.variables["initial_y"] = enemy_.center_y
            # enemy_.variables["dest_x"] = int(line[5])
            # enemy_.variables["dest_y"] = int(line[6])

            # Adding enemy to entity group and enemy group
            scene.add_sprite(LAYER_NAME_ENEMIES, enemy_, visible=False)
            scene.add_sprite(LAYER_NAME_ENTITIES, enemy_)


def get_window_size() -> Tuple:
    """
    Get current windows size

    :return: Tuple: [width, height]
    """
    current_window = arcade.get_window()
    return current_window.get_size()


def game_dir() -> str:
    _game_dir = os.path.dirname(os.path.abspath(__file__))
    return str(_game_dir)


def set_bg_color(color: Tuple = BG_COLOR) -> None:
    """
    Set window's background color

    :param color: Desired color
    :return: None
    """
    return arcade.set_background_color(color)


def check_the_battle(enemy_list, player):
    for enemy in enemy_list:
        dist = arcade.get_distance_between_sprites(player, enemy)
        if dist < 150:
            enemy.variables["player_in_radius"] = True
            # if arcade.get_distance_between_sprites(player, enemy) <= 50 and player.is_attacking:
            #     if enemy.get_hit(player.damage):
            #         add_exp(player, enemy)
            #
            # if arcade.get_distance_between_sprites(player, enemy) <= 50 and enemy.is_attacking:
            #     player.get_hit(enemy.damage)
            #
            # if not player.is_attacking:
            #     enemy.is_hit = False
            #
            # if not enemy.is_attacking:
            #     player.is_hit = False
        else:
            enemy.variables["player_in_radius"] = False


def add_exp(player, enemy):
    player.variables["exp"] += enemy.variables["exp"]
    enemy.variables["exp"] = 0
    p_level = player.variables["lvl"]
    p_exp = player.variables["exp"]
    if p_exp < NEXT_LEVEL_EXP[p_level + 1]:
        return
    lvl_to_delete = []
    for lvl, exp in _NEXT_LEVEL_EXP.items():
        diff = p_exp - exp
        if diff >= 0:
            player.variables["lvl"] += 1
            player.level_up()
            lvl_to_delete.append(lvl)
            p_exp -= exp
        else:
            player.variables["exp"] = p_exp
            break

    for lvl in lvl_to_delete:
        print(lvl)
        del _NEXT_LEVEL_EXP[lvl]


def load_texture_pair_mod(filename, width, y, height, hit_box_algorithm: str = "Simple"):
    """
    Load a texture pair, with the second being a mirror image of the first.
    Useful when doing animations and the character can face left/right.

    amount is taken from texture name - place number of frames in the name
    """
    textures_list = []  # I know it is tuple but the name is more understandable
    amount = [int(s) for s in re.findall(r'\d+', filename.split('/')[-1:][0])][0]

    for multiplying in range(amount):
        textures_list.append([
            arcade.texture.load_texture(filename,
                                               hit_box_algorithm=hit_box_algorithm,
                                               x=multiplying * width,
                                               y=y,
                                               width=width,
                                               height=height),
            arcade.texture.load_texture(filename,
                                               flipped_horizontally=True,
                                               hit_box_algorithm=hit_box_algorithm,
                                               x=multiplying * width,
                                               y=y,
                                               width=width,
                                               height=height)
        ])
    return textures_list, amount


def draw_highlighted_enemies(enemy_list, sw, sh):
    """
    Draw enemy health on the top of the screen

    :param enemy_list: List of the enemies
    :param sw: Screen width
    :param sh: Screen height
    """
    red = arcade.color.RED_DEVIL
    bar_width = 150
    bar_height = 10

    for enemy in enemy_list:
        if enemy.variables["is_highlighted"]:
            health_width = bar_width * (enemy.variables["actual_health_points"] / enemy.variables["max_hp"])
            arcade.draw_rectangle_outline(sw / 2, sh - 15, bar_width + 1, bar_height + 1, [0, 0, 0])
            arcade.draw_rectangle_filled(center_x=sw / 2 - 0.5 * (bar_width - health_width),
                                         center_y=sh - 15,
                                         width=health_width,
                                         height=bar_height,
                                         color=red)
            arcade.draw_text(f"{enemy.variables['enemy_name']} {enemy.variables['actual_health_points']} HP",
                             sw / 2 - 50,
                             sh - 20,
                             [255, 255, 255],
                             7,
                             100, bold=True,
                             font_name="Tahoma")


def _highlight_enemy(mouse_x, mouse_y, enemy_list):
    for enemy in arcade.get_sprites_at_point([mouse_x, mouse_y], enemy_list):
        print("je")
        enemy.variables["is_highlighted"] = True
        break
    else:
        for enemy in enemy_list:
            enemy.variables["is_highlighted"] = False


def _highlight_item(mouse_x, mouse_y, item_list):
    for item in arcade.get_sprites_at_point([mouse_x, mouse_y], item_list):
        item.draw_hit_box()


def highlight_object(mouse_x, mouse_y, player, item_list, enemy_list):
    x, y = get_map_point([mouse_x, mouse_y],
                         [player.center_x, player.center_y]
                         )
    if item_list:
        _highlight_item(x, y, item_list)
    _highlight_enemy(x, y, enemy_list)


def center_camera_to_player(camera, player_x, player_y):
    """
    Move camera to player

    :return: no return
    """
    screen_center_x = player_x - (camera.viewport_width / 2)
    screen_center_y = player_y - (camera.viewport_height / 2)

    if screen_center_x < 0:
        screen_center_x = 0
    if screen_center_y < 0:
        screen_center_y = 0
    player_centered = screen_center_x, screen_center_y
    camera.move_to(player_centered, speed=1)


def stop_player_if_obstacle(player, sprite_list):
    closest_sprite, dist = arcade.get_closest_sprite(player, sprite_list)
    if dist < 10:
        print(dist)
        player._stop()


def rescale(view):
    screen_w, screen_h = get_window_size()
    if view.screen_w != screen_w and view.screen_h != screen_h:
        view.screen_w = screen_w
        view.screen_h = screen_h
        view.stage["camera"].resize(screen_w, screen_h)
        view.stage["gui_camera"].resize(screen_w, screen_h)


def get_map_point(map_point: Point, player_point: Point) -> Point:
    _x, _y = map_point
    _x_player, _y_player = player_point
    screen_w, screen_h = get_window_size()
    #   800         1024/2 = 512 ; example
    if _x_player >= screen_w / 2:
        x = _x - screen_w / 2
    # -172 = 340 - 1024/2 ; example
    else:
        #   400     1024/2 = 512 ; example
        # _x_player <= 512 ; example
        x = _x
        _x_player = 0
    # 300 = 300 ; example

    if _y_player >= screen_h / 2:
        y = _y - screen_h / 2
    else:
        y = _y
        _y_player = 0

    return x + _x_player, y + _y_player


class DefaultMenu(arcade.View):
    def __init__(self, **kwargs):
        super().__init__()
        print(kwargs)
        self.previous_window = kwargs["previous_menu"]
        self.menu_name = kwargs["menu_name"]
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.button_list = []
        self.entered_settings = False
        self.v_box = arcade.gui.UIBoxLayout()

        set_bg_color(color=arcade.make_transparent_color(arcade.color.AMETHYST, 100))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def create_button(self, text, width, padding):
        button = arcade.gui.UIFlatButton(text=text, width=width)
        self.button_list.append(button)
        self.v_box.add(button.with_space_around(bottom=padding))

    def create_buttons(self, buttons: List):
        for b in buttons:
            self.create_button(b, 200, 20)

    def change_view(self, window):
        self.manager.disable()
        window.manager.enable()
        self.window.show_view(window)

    def back_button(self):
        self.manager.disable()
        try:
            self.previous_window.manager.enable()
        except AttributeError:
            set_bg_color()
        if self.entered_settings:
            rescale(self.previous_window)
        self.window.show_view(self.previous_window)

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:  # resume game
            self.back_button()

    @staticmethod
    def get_value(button):
        return button

    @staticmethod
    def quit_button():
        arcade.exit()

    def on_draw(self):
        arcade.start_render()
        self.manager.draw()
