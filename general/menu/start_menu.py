import arcade
from .settings_menu import Settings
from general.maps.map1.map1 import GameViewStart
from general.func import DefaultMenu


class MainMenu(DefaultMenu):
    """ Class to manage the game over view """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__buttons = ["Start Game", "Settings", "Quit"]
        self.create_buttons(self.__buttons)

        @self.get_value(self.button_list[0].event("on_click"))
        def on_click_start(event):
            start_view = GameViewStart()
            start_view.setup()
            self.change_view(start_view)

        # use a decorator to handle on_click events
        @self.get_value(self.button_list[0].event("on_click"))
        def on_click_settings(event):
            settings_view = Settings(previous_menu=self, menu_name="Settings")
            self.change_view(settings_view)

        @self.get_value(self.button_list[0].event("on_click"))
        def on_click_exit(event):
            self.quit_button()
