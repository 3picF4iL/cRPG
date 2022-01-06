import arcade
import arcade.gui
from .func import set_bg_color
from .settings_menu import Settings
from general.maps.map1.map1 import GameViewStart


class MainMenu(arcade.View):
    """ Class to manage the game over view """

    def __init__(self):
        super(MainMenu, self).__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.stage_name = "Main Menu"

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
            start_view.setup()
            self.window.show_view(start_view)

        # use a decorator to handle on_click events
        @settings_button.event("on_click")
        def on_click_settings(event):
            settings_view = Settings(self)
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
