from ..classes.WarCraft3Layer import WarCraft3Layer
from .. import constants
from . import binary_reader
from .parse_material_alpha import parse_material_alpha
from .parse_material_texture_id import parse_material_texture_id
from .parse_fresnel_colour import parse_fresnel_colour


def parse_layers(data):
    r = binary_reader.Reader(data)
    chunkId = r.getid(constants.CHUNK_LAYER)
    layersCount = r.getf('<I')[0]
    layers = []

    for _ in range(layersCount):
        layer = WarCraft3Layer()
        inclusiveSize = r.offset + r.getf('<I')[0]
        filterMode = r.getf('<I')[0]
        shadingFlags = r.getf('<I')[0]
        layer.texture_id = r.getf('<I')[0]
        textureAnimationId = r.getf('<I')[0]
        coordId = r.getf('<I')[0]
        alpha = r.getf('<f')[0]
        if constants.MDX_CURRENT_VERSION > 800:
            emissive_gain = r.getf('<f')[0]
            if constants.MDX_CURRENT_VERSION > 900:
                fresnel_color = [r.getf('<f')[0],r.getf('<f')[0],r.getf('<f')[0]]
                fresnel_opacity = r.getf('<f')[0]
                fresnel_team_color = r.getf('<f')[0]
        while r.offset < inclusiveSize:
            chunkId = r.getid(constants.SUB_CHUNKS_LAYER)
            if chunkId == constants.CHUNK_MATERIAL_TEXTURE_ID:
                layer.material_texture_id = parse_material_texture_id(r)
            elif chunkId == constants.CHUNK_MATERIAL_ALPHA:
                layer.material_alpha = parse_material_alpha(r)
            elif chunkId == constants.CHUNK_MATERIAL_FRESNEL_COLOUR:
                fresnel_colour = parse_fresnel_colour(r)
            elif chunkId == constants.CHUNK_MATERIAL_EMISSIONS:
                emissions = parse_material_alpha(r)
            elif chunkId == constants.CHUNK_MATERIAL_FRESNEL_ALPHA:
                fresnel_alpha = parse_material_alpha(r)
            elif chunkId == constants.CHUNK_MATERIAL_FRESNEL_TEAMCOLOUR:
                fresnel_teamcolour = parse_material_alpha(r)
        layers.append(layer)

    return layers
