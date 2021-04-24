from . import binary_reader
from .. import constants
from io_scene_warcraft_3.classes.WarCraft3Layer import WarCraft3Layer
from .parse_material_alpha import parse_material_alpha
from .parse_material_texture_id import parse_material_texture_id


def parse_layers(data):
    r = binary_reader.Reader(data)
    chunk_id = r.getid(constants.CHUNK_LAYER)
    layers_count = r.getf('<I')[0]
    layers = []
    for _ in range(layers_count):
        layer = WarCraft3Layer()
        inclusive_size = r.offset + r.getf('<I')[0]
        filter_mode = r.getf('<I')[0]
        shading_flags = r.getf('<I')[0]
        layer.texture_id = r.getf('<I')[0]
        texture_animation_id = r.getf('<I')[0]
        coord_id = r.getf('<I')[0]
        alpha = r.getf('<f')[0]
        while r.offset < inclusive_size:
            chunk_id = r.getid(constants.SUB_CHUNKS_LAYER)
            if chunk_id == constants.CHUNK_MATERIAL_ALPHA:
                layer.material_alpha = parse_material_alpha(r)
            elif chunk_id == constants.CHUNK_MATERIAL_TEXTURE_ID:
                layer.material_texture_id = parse_material_texture_id(r)
        layers.append(layer)
    return layers
