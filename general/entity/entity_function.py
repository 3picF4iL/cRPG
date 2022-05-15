from typing import List, Dict
from ..const import ENTITY_TEXTURE_SET
from ..func import load_texture_pair_mod


def load_textures(texture_list: List, entity_variables: Dict):
    if not texture_list:
        raise Exception("Texture list is empty!")
    if not entity_variables:
        raise Exception("Entity variable dict is empty!")
    # frame settings
    texture_width, texture_shift, texture_height = ENTITY_TEXTURE_SET

    for texture_type in texture_list:
        entity_variables[f"textures_{texture_type}"], entity_variables[f"textures_{texture_type}_nr"] = \
            load_texture_pair_mod(entity_variables["graphic_location"] +
                                  entity_variables[f"textures_{texture_type}_file"],
                                  texture_width, texture_shift, texture_height)


def face_dir_change(entity_variables, x):
    if x > 0:
        entity_variables["face_direction"] = 0
    elif x < 0:
        entity_variables["face_direction"] = 1