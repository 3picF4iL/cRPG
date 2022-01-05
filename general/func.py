import os
import re
import arcade
from win32api import GetKeyState, keybd_event
from win32con import VK_CAPITAL, VK_NUMLOCK, VK_SCROLL, KEYEVENTF_KEYUP
from typing import Tuple, Dict, Any, NoReturn, List
from .const import SCREEN_SIZE, TITLE, LAYER_NAME_PLAYER, LAYER_NAME_ENEMIES, BG_COLOR


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

    :return: No return
    """

    def disable_lockkey(key: int) -> NoReturn:  # Disable states of Caps Lock, Num Lock and Scroll Lock buttons on keyboard
        """
        Internal function for key state checking

        :param key: Key for keybd_event
        :return: No return
        """
        keybd_event(key, 0)
        keybd_event(key, 0, KEYEVENTF_KEYUP)
        pass

    keys = [VK_NUMLOCK,  # Num Lock
            VK_SCROLL,   # Scroll Lock
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
        return arcade.Window(screen_w, screen_h, TITLE)
    window.set_size(screen_w, screen_h)


def set_player(player, p_list: list, scene: Any) -> NoReturn:
    """
    Creating and inserting player object into player list (for future drawing)

    :param player: Player class
    :param scene: Actual scene
    :param p_list: Player list
    """

    player_ = player()
    scene.add_sprite(LAYER_NAME_PLAYER, player_)
    p_list.append(player_)


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
                                        x=multiplying*width,
                                        y=y,
                                        width=width,
                                        height=height),
            arcade.texture.load_texture(filename,
                                        flipped_horizontally=True,
                                        hit_box_algorithm=hit_box_algorithm,
                                        x=multiplying*width,
                                        y=y,
                                        width=width,
                                        height=height)
        ])
    return textures_list, amount


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

