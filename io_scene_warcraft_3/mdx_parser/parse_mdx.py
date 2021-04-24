from ..classes.MDXImportProperties import MDXImportProperties
from ..classes.WarCraft3Model import WarCraft3Model
from .. import constants
from ..importer import importer
from . import binary_reader
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


def parse_mdx(data, import_properties):
    data_size = len(data)
    r = binary_reader.Reader(data)
    r.getid(constants.CHUNK_MDX_MODEL)
    model = WarCraft3Model()
    model.file = import_properties.mdx_file_path

    while r.offset < data_size:
        chunk_id = r.getid(constants.SUB_CHUNKS_MDX_MODEL, debug=True)
        chunk_size = r.getf('<I')[0]
        chunk_data = data[r.offset: r.offset + chunk_size]
        r.skip(chunk_size)

        if chunk_id == constants.CHUNK_VERSION:
            parse_version(chunk_data, model)
        elif chunk_id == constants.CHUNK_GEOSET:
            parse_geosets(chunk_data, model)
        elif chunk_id == constants.CHUNK_TEXTURE:
            parse_textures(chunk_data, model)
        elif chunk_id == constants.CHUNK_MATERIAL:
            parse_materials(chunk_data, model)
        elif chunk_id == constants.CHUNK_MODEL:
            parse_model(chunk_data, model)
        elif chunk_id == constants.CHUNK_BONE:
            parse_bones(chunk_data, model)
        elif chunk_id == constants.CHUNK_PIVOT_POINT:
            parse_pivot_points(chunk_data, model)
        elif chunk_id == constants.CHUNK_HELPER:
            parse_helpers(chunk_data, model)
        elif chunk_id == constants.CHUNK_ATTACHMENT:
            parse_attachments(chunk_data, model)
        elif chunk_id == constants.CHUNK_EVENT_OBJECT:
            parse_events(chunk_data, model)
        elif chunk_id == constants.CHUNK_COLLISION_SHAPE:
            parse_collision_shapes(chunk_data, model)
        elif chunk_id == constants.CHUNK_SEQUENCE:
            parse_sequences(chunk_data, model)
        elif chunk_id == constants.CHUNK_GEOSET_ANIMATION:
            parse_geoset_animations(chunk_data, model)

    importer.load_warcraft_3_model(model, import_properties)
