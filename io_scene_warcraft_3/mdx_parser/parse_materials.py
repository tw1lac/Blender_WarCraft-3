from ..classes.WarCraft3Material import WarCraft3Material
from . import binary_reader
from .parse_layers import parse_layers
from .. import constants

def parse_materials(data, model):
    r = binary_reader.Reader(data)
    dataSize = len(data)

    while r.offset < dataSize:
        material = WarCraft3Material()
        inclusiveSize = r.getf('<I')[0]
        priorityPlane = r.getf('<I')[0]
        flags = r.getf('<I')[0]

        if constants.MDX_CURRENT_VERSION > 800:
            shader = r.gets(80)
            if shader == "Shader_HD_DefaultUnit":
                material.hd = True
            layerChunkDataSize = inclusiveSize - 92
        else:
            layerChunkDataSize = inclusiveSize - 12

        if layerChunkDataSize > 0:
            layerChunkData = data[r.offset : r.offset + layerChunkDataSize]
            r.skip(layerChunkDataSize)
            material.layers = parse_layers(layerChunkData)

        model.materials.append(material)
