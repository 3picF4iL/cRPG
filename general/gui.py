"""
Temp desc
"""
import arcade
from .const import NEXT_LEVEL_EXP, SHORTCUTS, DND
from .func import get_window_size


class GUI:
    def __init__(self):
        self.s_w, self.s_h = get_window_size()
        self.debug = None

    def print_hud(self):
        self._print_bottom_bar(self.debug)
        self._print_side_bar()

    def _get_char_stats(self):
        stats = ""
        for stat in [self.char_astats, self.char_misc, self.char_resistances]:
            for attribute, value in stat.items():
                value_ = value
                if not attribute in DND:
                    stats += f"{SHORTCUTS[attribute]}: {value_}\n"
            stats += "\n"
        return stats

    def print_char_stats(self, show_stats):
        """
        Print character stats information

        :return: string of selected stats
        """
        if show_stats:
            stats = self._get_char_stats()

            arcade.draw_rectangle_filled(self.s_w - 75, self.s_h / 2, 150, self.s_h - 200, arcade.color.ANTIQUE_BRONZE)
            arcade.draw_text(f"{stats}", self.s_w - 148, self.s_h - 150, [0, 0, 0], 10, 200, 'left',
                             bold=True, multiline=True)

    def print_player_main_stats(self, transparent):
        green = arcade.color.GREEN
        red = arcade.color.RED
        black = arcade.color.WHITE_SMOKE
        blue = arcade.color.BLUE
        yellow = arcade.color.YELLOW
        if transparent:
            black = arcade.make_transparent_color(black, 350)
            green = arcade.make_transparent_color(green, 350)
            red = arcade.make_transparent_color(red, 350)
            blue = arcade.make_transparent_color(blue, 350)
            yellow = arcade.make_transparent_color(yellow, 350)

        # ==========
        # HEALTH
        # ==========
        arcade.draw_text(f"Health: {self.char_astats['actual_health_points']}/{self.char_astats['max_hp']}", 100, 50, black, 9, 5)

        health_bar_percent = self.char_astats['actual_health_points']/self.char_astats['max_hp']
        if health_bar_percent < 1:
            health_bar_posx = 200 - (200 - 200 * health_bar_percent) / 2
            health_bar_width = 200 - (200 - 200 * health_bar_percent)
            health_bar_red_width = 200 - health_bar_width
            health_bar_red_posx = 200 + health_bar_width/2
        else:
            health_bar_red_width = health_bar_red_posx = 0
            health_bar_posx = health_bar_width = 200

        arcade.draw_rectangle_filled(health_bar_posx, 40, health_bar_width, 9, green)
        arcade.draw_rectangle_filled(health_bar_red_posx, 40, health_bar_red_width, 9, red)

        # ==========
        # MANA
        # ==========
        arcade.draw_text(f"Mana: {self.char_astats['actual_mana_points']}/{self.char_astats['max_mana']}",
                         self.s_w - 300, 50, black, 9, 5)

        mana_bar_percent = self.char_astats['actual_mana_points']/self.char_astats['max_mana']
        if mana_bar_percent < 1:
            mana_bar_posx = self.s_w - (200 - 200 * mana_bar_percent) / 2
            mana_bar_width = 200 - (200 - 200 * mana_bar_percent)
            mana_bar_black_width = 200 - mana_bar_width
            mana_bar_black_posx = (self.s_w - 190) + mana_bar_width/2
        else:
            mana_bar_black_width = mana_bar_black_posx = 0
            mana_bar_posx = self.s_w - 200
            mana_bar_width = 200

        arcade.draw_rectangle_filled(mana_bar_posx, 40, mana_bar_width, 9, blue)
        arcade.draw_rectangle_filled(mana_bar_black_posx, 40, mana_bar_black_width, 9, black)

        # ==========
        # EXP
        # ==========
        exp_line = (self.s_w - 190) * self.char_misc['exp'] / NEXT_LEVEL_EXP[self.char_misc['lvl']+1]
        arcade.draw_text(f"Lvl: {self.char_misc['lvl']} | EXP: {self.char_misc['exp']}",
                         self.s_w/2-40, 30, black, 9, 100)
        arcade.draw_line(100, 20, 100 + exp_line, 20, yellow)

    def _print_bottom_bar(self, debug):
        transparent = False

        if 120 > self.center_y > 0:
            transparent = True

        transparent_value = 100
        main_color = arcade.color.ANTIQUE_BRONZE

        if transparent:
            main_color = arcade.make_transparent_color(main_color, transparent_value)

        arcade.draw_circle_filled(80, 20, 10, main_color)
        arcade.draw_circle_filled(80, 60, 10, main_color)
        arcade.draw_circle_filled(self.s_w-80, 20, 10, main_color)
        arcade.draw_circle_filled(self.s_w-80, 60, 10, main_color)
        arcade.draw_rectangle_filled(self.s_w/2, 40, self.s_w-140, 40, main_color)
        arcade.draw_rectangle_filled(self.s_w/2, 40, self.s_w-160, 60, main_color)
        self.print_player_main_stats(transparent)
        self._print_debug_info(debug)

    def _print_side_bar(self):
        self.print_char_stats(self.player_variables["is_show_stats"])

    def _print_debug_info(self, debug):
        """
        Print some info, instead of score there might be different info

        :param score: Some input
        :return: No return
        """
        arcade.draw_text(f"DEBUG: {debug}",
                         100, 20, [255, 255, 0], 8, 20, 'left', bold=True)
        arcade.draw_text(f"Att: {self.player_variables['is_attacking']}",
                         200, 20, [255, 255, 0], 8, 20, 'left', bold=True)
        arcade.draw_text(f"Mov: {self.player_variables['is_moving']}",
                         300, 20, [255, 255, 0], 8, 20, 'left', bold=True)

    def print_char_info_over_head(self):
        arcade.draw_text(f"[{round(self.center_x)}, {round(self.center_y)}]", self.center_x-20, self.center_y+40,
                         [0, 0, 0], 8, 100, 'left', bold=True, multiline=True)

    def print_items_info(self, item_list, show):
        if show:
            for item in item_list:
                if not arcade.get_distance_between_sprites(self, item) > 300:
                    arcade.draw_text(f"{item.print_created_item()}", item.center_x, item.center_y + item.height/2,
                                     [0, 0, 0], 10, 100, 'left', bold=True, multiline=True)

    def rescale(self):
        self.s_w, self.s_h = get_window_size()
