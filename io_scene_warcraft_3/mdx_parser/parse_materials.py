from . import binary_reader
from io_scene_warcraft_3.classes.WarCraft3Material import WarCraft3Material
from .parse_layers import parse_layers


def parse_materials(data, model):
    r = binary_reader.Reader(data)
    dataSize = len(data)
    while r.offset < dataSize:
        material = WarCraft3Material()
        inclusiveSize = r.getf('<I')[0]
        priorityPlane = r.getf('<I')[0]
        flags = r.getf('<I')[0]
        layerChunkDataSize = inclusiveSize - 12
        if layerChunkDataSize > 0:
            layerChunkData = data[r.offset: r.offset + layerChunkDataSize]
            r.skip(layerChunkDataSize)
            material.layers = parse_layers(layerChunkData)
        model.materials.append(material)
