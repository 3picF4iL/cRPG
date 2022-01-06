import arcade
import arcade.gui
from .func import set_bg_color, set_window_with_size


class Settings(arcade.View):
    """ Class to manage the game over view """

    def __init__(self, main_menu):
        super(Settings, self).__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.main_menu = main_menu
        self.stage_name = "Settings"

        set_bg_color(color=arcade.color.AMETHYST)

        # Layout element for keeping buttons in vertical order
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        video_button = arcade.gui.UIFlatButton(text="Video", width=200)
        self.v_box.add(video_button.with_space_around(bottom=20))

        sound_button = arcade.gui.UIFlatButton(text="Sound", width=200)
        self.v_box.add(sound_button.with_space_around(bottom=20))

        back_button = arcade.gui.UIFlatButton(text="Back", width=200)
        self.v_box.add(back_button.with_space_around(bottom=20))

        @video_button.event("on_click")
        def on_click_video(event):
            video_view = SettingsVideo(self)
            self.manager.disable()
            self.window.show_view(video_view)

        # use a decorator to handle on_click events
        @sound_button.event("on_click")
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

        @back_button.event("on_click")
        def on_click_back(event):
            self.manager.disable()
            main_menu.manager.enable()
            self.window.show_view(main_menu)

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_draw(self):
        arcade.start_render()
        self.manager.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        self.manager.disable()
        self.main_menu.manager.enable()
        self.window.show_view(self.main_menu)


class SettingsVideo(arcade.View):
    """ Class to manage the game over view """

    def __init__(self, settings):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.settings_view = settings

        set_bg_color(color=arcade.color.AMETHYST)

        # Layout element for keeping buttons in vertical order
        self.v_box = arcade.gui.UIBoxLayout()

        # Setting title
        label = arcade.gui.UILabel(text="Video Settings", font_size=30)
        self.v_box.add(label.with_space_around(bottom=20))

        # Create the buttons
        small_size_button = arcade.gui.UIFlatButton(text="800x600", width=200)
        self.v_box.add(small_size_button.with_space_around(bottom=20))

        # For later :)
        #
        # style = dict(
        #     bg_color_pressed=arcade.color.YELLOW
        #     )

        normal_size_button = arcade.gui.UIFlatButton(text="1024x786", width=200)

        self.v_box.add(normal_size_button.with_space_around(bottom=20))

        large_size_button = arcade.gui.UIFlatButton(text="1920x1080", width=200)
        self.v_box.add(large_size_button.with_space_around(bottom=20))

        back_button = arcade.gui.UIFlatButton(text="Back to Settings", width=200)
        self.v_box.add(back_button.with_space_around(bottom=20))

        @small_size_button.event("on_click")
        def on_click_start(event):
            set_window_with_size(0, self.window)

        # use a decorator to handle on_click events
        @normal_size_button.event("on_click")
        def on_click_settings(event):
            set_window_with_size(1, self.window)

        @large_size_button.event("on_click")
        def on_click_exit(event):
            set_window_with_size(2, self.window)

        @back_button.event("on_click")
        def on_click_exit(event):
            self.manager.disable()
            settings.manager.enable()
            self.window.show_view(settings)

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_draw(self):
        arcade.start_render()
        self.manager.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        self.manager.disable()
        self.settings_view.manager.enable()
        self.window.show_view(self.settings_view)
