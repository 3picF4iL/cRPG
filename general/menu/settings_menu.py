import arcade.arcade as arcade
import arcade.arcade.gui
from general.func import set_window_with_size, DefaultMenu


class Settings(DefaultMenu):
    """ Class to manage the game over view """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__buttons = ["Back", "Video", "Sound"]
        self.create_buttons(self.__buttons)

        @self.get_value(self.button_list[1].event("on_click"))
        def on_click_video(event):
            video_view = SettingsVideo(previous_menu=self, menu_name="Video Setting")
            self.change_view(video_view)

        # use a decorator to handle on_click events
        @self.get_value(self.button_list[2].event("on_click"))
        def on_click_sound(event):
            message_box = arcade.gui.UIMessageBox(
                width=300,
                height=200,
                message_text=(
                    "Option not implemented yet!"
                ),
                buttons=["Ok"]
            )
            self.manager.add(message_box)

        @self.get_value(self.button_list[0
                        ].event("on_click"))
        def on_click_back(event):
            self.back_button()


class SettingsVideo(DefaultMenu):
    """ Class to manage the game over view """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__buttons = ["Back to Settings", "800x600", "1024x786", "1920x1080", "Quit"]
        self.create_buttons(self.__buttons)

        label = arcade.gui.UILabel(text="Video Settings", font_size=30)
        self.v_box.children.insert(0, label.with_space_around(bottom=20))

        @self.get_value(self.button_list[1].event("on_click"))
        def on_click_1(event):
            set_window_with_size(0, self.window)

        # use a decorator to handle on_click events
        @self.get_value(self.button_list[2].event("on_click"))
        def on_click_2(event):
            set_window_with_size(1, self.window)

        @self.get_value(self.button_list[3].event("on_click"))
        def on_click_3(event):
            set_window_with_size(2, self.window)

        @self.get_value(self.button_list[0].event("on_click"))
        def on_click_back(event):
            self.back_button()

        @self.get_value(self.button_list[4].event("on_click"))
        def on_click_quit(event):
            self.quit_button()
