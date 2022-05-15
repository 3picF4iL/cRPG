from typing import List, Dict
from ..func import load_texture_pair_mod


def load_textures(texture_list: List, entity_variables: Dict):
    if not texture_list:
        raise Exception("Texture list is empty!")
    if not entity_variables:
        raise Exception("Entity variable dict is empty!")

    for texture_type in texture_list:
        entity_variables[f"textures_{texture_type}"], entity_variables[f"textures_{texture_type}_nr"] = \
            load_texture_pair_mod(entity_variables["graphic_location"] +
                                  entity_variables[f"textures_{texture_type}_file"], 720, 0, 490)
