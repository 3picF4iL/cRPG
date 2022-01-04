import arcade
from general.func import set_window_with_size
from general.map.map1.stages.stages import GameViewStart


def main():
    window = set_window_with_size()
    # main_menu = MainMenu()
    # window.show_view(main_menu)
    game = GameViewStart()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()
