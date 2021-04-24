from . import binary_reader
from .. import constants
from io_scene_warcraft_3.classes.WarCraft3Model import WarCraft3Model
from io_scene_warcraft_3.importer.importer import load_warcraft_3_model
from .parse_attachments import parse_attachments
from .parse_bones import parse_bones
from .parse_collision_shapes import parse_collision_shapes
from .parse_events import parse_events
from .parse_geoset_animations import parse_geoset_animations
from .parse_geosets import parse_geosets
from .parse_helpers import parse_helpers
from .parse_materials import parse_materials
from .parse_model import parse_model
from .parse_pivot_points import parse_pivot_points
from .parse_sequences import parse_sequences
from .parse_textures import parse_textures
from .parse_version import parse_version


def parse_mdx(data, importProperties):
    dataSize = len(data)
    r = binary_reader.Reader(data)
    r.getid(constants.CHUNK_MDX_MODEL)
    model = WarCraft3Model()
    while r.offset < dataSize:
        chunkId = r.getid(constants.SUB_CHUNKS_MDX_MODEL, debug=True)
        chunkSize = r.getf('<I')[0]
        chunkData = data[r.offset : r.offset + chunkSize]
        r.skip(chunkSize)
        if chunkId == constants.CHUNK_VERSION:
            parse_version(chunkData)
        elif chunkId == constants.CHUNK_GEOSET:
            parse_geosets(chunkData, model)
        elif chunkId == constants.CHUNK_TEXTURE:
            parse_textures(chunkData, model)
        elif chunkId == constants.CHUNK_MATERIAL:
            parse_materials(chunkData, model)
        elif chunkId == constants.CHUNK_MODEL:
            parse_model(chunkData, model)
        elif chunkId == constants.CHUNK_BONE:
            parse_bones(chunkData, model)
        elif chunkId == constants.CHUNK_PIVOT_POINT:
            parse_pivot_points(chunkData, model)
        elif chunkId == constants.CHUNK_HELPER:
            parse_helpers(chunkData, model)
        elif chunkId == constants.CHUNK_ATTACHMENT:
            parse_attachments(chunkData, model)
        elif chunkId == constants.CHUNK_EVENT_OBJECT:
            parse_events(chunkData, model)
        elif chunkId == constants.CHUNK_COLLISION_SHAPE:
            parse_collision_shapes(chunkData, model)
        elif chunkId == constants.CHUNK_SEQUENCE:
            parse_sequences(chunkData, model)
        elif chunkId == constants.CHUNK_GEOSET_ANIMATION:
            parse_geoset_animations(chunkData, model)
    load_warcraft_3_model(model, importProperties)
