import arcade
import arcade.gui
from general.settings_menu import Settings
from .func import set_bg_color, rescale


class PauseMenu(arcade.View):
    """ Class to manage the game over view """

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.stage_name = "Pause Menu"
        self.entered_settings = False

        set_bg_color(color=arcade.make_transparent_color(arcade.color.AMETHYST, 100))

        # Layout element for keeping buttons in vertical order
        self.v_box = arcade.gui.UIBoxLayout()

        back_button = arcade.gui.UIFlatButton(text="Back", width=200)
        self.v_box.add(back_button.with_space_around(bottom=20))

        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)
        self.v_box.add(quit_button.with_space_around(bottom=20))

        # use a decorator to handle on_click events

        @back_button.event("on_click")
        def on_click_settings(event):
            self.manager.disable()
            arcade.set_background_color(arcade.color.AMAZON)
            if self.entered_settings:
                rescale(self.main_window)
            self.window.show_view(self.main_window)

        @settings_button.event("on_click")
        def on_click_settings(event):
            settings_view = Settings(self)
            self.manager.disable()
            settings_view.manager.enable()
            self.window.show_view(settings_view)
            self.entered_settings = True

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

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # resume game
            self.manager.disable()
            arcade.set_background_color(arcade.color.AMAZON)
            if self.entered_settings:
                rescale(self.main_window)
            self.window.show_view(self.main_window)
