from ..classes.WarCraft3Material import WarCraft3Material
from . import binary_reader
from .parse_layers import parse_layers
from .. import constants
from ..classes.WarCraft3Model import WarCraft3Model


def parse_materials(data, model):
    r = binary_reader.Reader(data)
    data_size = len(data)

    while r.offset < data_size:
        material = WarCraft3Material()
        inclusive_size = r.getf('<I')[0]
        priority_plane = r.getf('<I')[0]
        flags = r.getf('<I')[0]

        # if constants.MDX_CURRENT_VERSION > 800:
        if model.version > 800:
            shader = r.gets(80)
            if shader == "Shader_HD_DefaultUnit":
                material.hd = True
            layer_chunk_data_size = inclusive_size - 92
        else:
            layer_chunk_data_size = inclusive_size - 12

        if layer_chunk_data_size > 0:
            layer_chunk_data = data[r.offset: r.offset + layer_chunk_data_size]
            r.skip(layer_chunk_data_size)
            material.layers = parse_layers(layer_chunk_data, model.version)

        model.materials.append(material)
