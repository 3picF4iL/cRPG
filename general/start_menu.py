import arcade
import arcade.gui
from .func import set_bg_color
from map.map1.stages.stages import GameViewStart

class MainMenu(arcade.View):
    """ Class to manage the game over view """

    def __init__(self):
        super(MainMenu, self).__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.gui_manager = arcade.gui.UIManager()

        self.gui_manager.enable()
        set_bg_color(color=arcade.color.AMETHYST)

        # Layout element for keeping buttons in vertical order
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)
        self.v_box.add(quit_button.with_space_around(bottom=20))

        @start_button.event("on_click")
        def on_click_start(event):
            start_view = GameViewStart()
            self.manager.disable()
            self.window.show_view(start_view)

        # use a decorator to handle on_click events
        @settings_button.event("on_click")
        def on_click_settings(event):
            settings_view = Settings()
            self.manager.disable()
            self.window.show_view(settings_view)

        @quit_button.event("on_click")
        def on_click_exit(event):
            arcade.exit()

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



class Settings(arcade.View):
    """ Class to manage the game over view """

    def __init__(self):
        super(Settings, self).__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.gui_manager = arcade.gui.UIManager()

        self.gui_manager.enable()
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
            video_view = SettingsVideo()
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
            self.window.show_view(MainMenu())

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


class SettingsVideo(arcade.View):
    """ Class to manage the game over view """

    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.gui_manager = arcade.gui.UIManager()

        self.gui_manager.enable()
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
            settings = Settings()
            self.manager.disable()
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
