"""
##########################
# Character initial settings
##########################
"""


class CharClass:
    def __init__(self, char_class):
        """
        Class for characters stats keeping

        :var self.char_stats: keeps standard values for character
        :var self.char_stats: miscellaneous values
        :var self.char_resistances: character resistances
        """
        self._class = char_class
        # General stats

        self.stats = {
            "char_stats": {
                "str": 0,   # Strength
                "dex": 0,   # Dexterity
                "vit": 0,   # Vitality
                "ene": 0,   # Energy
                "max_hp": 0,
                "max_mana": 0,
                "stamina": 0,
                "actual_health_points": 0,
                "actual_mana_points": 0,
                "actual_stamina_points": 0,
                "dmg_min": 0,
                "dmg_max": 0,
                "lvl": 1,
                "mf": 0,  # Magic Find - 20%
                "gf": 0,  # Gold Find - 20% - increase max and min value of gold drop for value
                "gb": 0,   # Add X gold to min and max value
                "exp": 0,   # Experience
                "diff": 0,  # 0, 1, 2 - 0 the lowest, 2 - the highest
                "place": None,  # Where char is actually
                "dc": 0,    # Drop Chance - if enemy killed = % chance to drop anything
                "mvm": 0,   # Movement speed
                "as": 0,     # Attack speed %
                "lvl_hp": 0,    # HP increasing when lvl up
                "lvl_mana": 0,    # Mana increasing when lvl up
                "lvl_stam": 0,    # Stamina increasing when lvl up
                "add_str": 0,    # Strength value when changing
                "add_dex": 0,    # Dexterity value when changing
                "add_vit": 0,    # HP increasing when changing
                "add_ene": 0,     # Mana increasing when lvl up
                # Char resistances
                "cr": 0,  # Cold res
                "fr": 0,  # Fire res
                "lr": 0,  # Lighting res
                "pr": 0,  # Poison res

                # Char textures variables that will be set from file
                "textures_walk_file": "walking_18.png",
                "animation_walk_speed": 1,
                "textures_attack_file": "attack_12.png",
                "animation_attack_speed": 1,
                "textures_idle_file": "idle_17.png",
                "animation_idle_speed": 1,

                # Char textures variables that will be set during initialization
                "graphic_location": f"graphic/player/{self._class}/movement/",
                "animation_last_state": 0,  # 0 - idle, 1 - moving, 2 - attacking
                "animation_cur_state": 0,
                "textures_walk_nr": 0,
                "textures_attack_nr": 0,
                "textures_idle_nr": 0,
                "textures_walk": [],
                "textures_attack": [],
                "textures_idle": [],
                }
        }

        self.char_stats = self.stats["char_stats"]
        self.load_char_stats()

        """
        Set attribute - set specified value for the attribute
        Get attribute - get value of the attribute (e.g. str = 10)
        Change attribute - change attribute value by value (e.g. str = str + 1)
        stat = {"char_stats", "char_resistances", "char_texure"}
        attr = e.g "str", "dex" etc.
        value = integer/string etc.
        """

    def animation_speed_recalc(self):
        self.char_stats["animation_walk_speed"] = self.char_stats["mvm"] // 100 * 2
        self.char_stats["animation_attack_speed"] = self.char_stats["as"] // 10 * 2

    def level_up(self):
        values_for_change = [self.char_stats["lvl_hp"], self.char_stats["lvl_mana"], self.char_stats["lvl_stamina"]]
        for i, attr, actual in enumerate(zip(["max_hp", "max_mana", "stamina"],
                                             ["actual_health_points", "actual_mana_points", "actual_stamina_points"])):
            self.set_attribute(attr, values_for_change[i])
            self.set_attribute(actual, values_for_change[i])

    def set_attribute(self, attr, value):
        self.char_stats[attr] = value
        return self.char_stats[attr]

    def get_attribute(self, attr):
        return self.char_stats[attr]

    def change_attribute(self, attr, value):
        try:
            self.char_stats[attr] += value
        except TypeError:
            raise TypeError(f"Attribute {attr} cannot be changed by {value} because attr {attr} "
                            f"with attr {attr} is type {type(attr)} and value is type {type(value)}")
        return self.char_stats[attr]

    def change_resistance(self, res, value):
        self.char_stats[res] += value
        return self.char_stats[res]

    def get_resistance(self, res):
        return self.char_stats[res]

    def set_resistance(self, res, value):
        self.char_stats[res] = value
        return self.char_stats[res]

    def load_char_stats(self):
        values = [line for line in open("general/char_class/class_settings", "r").readlines()
                  if line.startswith(str(self._class)) and not line.startswith("#")][0]
        # if len(values) != 3:
        #     raise ValueError(f"More char_class character values({len(values)} than expected (3)!")
        values = values.split()
        values.pop(0)

        _stats = list(self.char_stats.keys())
        print(_stats)
        print(values)
        for j, (value, stat) in enumerate(zip(values, _stats)):
            if value is None or stat is None:
                break
            import re
            if value.isdigit():
                value = int(value)
            elif re.match(r'^[0-9]\.[0-9]$', value):
                value = float(value)
            self.verify_value(pos=j+1, value=value)
            self.set_attribute(attr=stat, value=value)

        print(self.char_stats)

    @staticmethod
    def verify_value(pos, value):
        type_value = type(value)
        print(type_value)
        if pos in range(1, 18) or pos == 19 or pos in range(21, 23) or pos in range(30, 34) or pos in [35, 37, 39]:
            if not isinstance(value, int):
                raise ValueError(f"Expected int on position {pos} got {type_value}, {value}")
        elif pos in range(23, 28) or pos == 29:
            if not isinstance(value, float):
                raise ValueError(f"Expected float on position {pos} got {type_value}, {value}")
        elif pos in [34, 36, 38]:
            if not isinstance(value, str):
                raise ValueError(f"Expected string on position {pos} got {type_value}, {value}")
        elif pos == 28:
            if value < 11:
                raise ValueError(f"Expected value on position {pos} to be >11 got {value}, {value}")
        elif pos == 0:
            if value not in range(0, 10):
                raise ValueError(f"Expected value in range 0-9 on {pos} got {value}, {value}")
        elif pos == 18:
            if value not in range(0, 3):
                raise ValueError(f"Expected value in range 0-2 on {pos} got {value}, {value}")
        elif pos == 20:
            if value not in range(0, 100):
                raise ValueError(f"Expected value in range 0-100 on {pos} got {value}, {value}")
        else:
            raise ValueError(f"Position ({pos}) not match in any, {value}")

        return pos, value
