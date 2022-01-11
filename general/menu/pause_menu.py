import arcade
from general.func import DefaultMenu, rescale
from .settings_menu import Settings


class PauseMenu(DefaultMenu):
    """ Class to manage the game over view """

    def __init__(self, **kwargs):
        print(kwargs)
        super().__init__(**kwargs)

        self.__buttons = ["Resume Game", "Settings", "Quit"]
        self.create_buttons(self.__buttons)

        @self.get_value(self.button_list[0].event("on_click"))
        def on_click_back(event):
            self.back_button()

        @self.get_value(self.button_list[1].event("on_click"))
        def on_click_settings(event):
            settings_view = Settings(previous_menu=self, menu_name="Settings")
            self.entered_settings = True
            self.change_view(settings_view)

        @self.get_value(self.button_list[2].event("on_click"))
        def on_click_exit(event):
            self.quit_button()
