import arcade
from win32api import GetKeyState, keybd_event
from win32con import VK_CAPITAL, VK_NUMLOCK, VK_SCROLL, KEYEVENTF_KEYUP
from typing import Tuple
from .const import SCREEN_SIZE, TITLE
from .const import BG_COLOR


def get_key_from_value(dictionary, value):  # Return key or keys from value
    for k, v in dictionary.items():
        if v == value:
            return k
    return None


def checking_lockkey_states():  # Checking states of keyboard buttons
    def disable_lockkey(key):  # Disable states of Caps Lock, Num Lock and Scroll Lock buttons on keyboard
        keybd_event(key, 0)
        keybd_event(key, 0, KEYEVENTF_KEYUP)
        pass

    keys = [VK_NUMLOCK,  # Num Lock
            VK_SCROLL,   # Scroll Lock
            VK_CAPITAL]  # Caps Lock

    for _key in keys:
        if GetKeyState(_key):
            disable_lockkey(_key)


def set_window_with_size(size: int = 1, *args):
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


@property
def get_window_size() -> Tuple:
    """
    Get current windows size

    :return: Tuple: [width, height]
    """
    current_window = arcade.get_window()
    return current_window.get_size()


def set_bg_color(color: Tuple = BG_COLOR):
    return arcade.set_background_color(color)

