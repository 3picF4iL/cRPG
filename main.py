import arcade
from general.func import set_window_with_size
from general.maps.map1.map1 import GameViewStart
# from general.menu.start_menu import MainMenu

#arcade.configure_logging()

def main():
    window = set_window_with_size()
    # main_menu = MainMenu()
    # window.show_view(main_menu)
    game = GameViewStart()
    game.setup()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()
