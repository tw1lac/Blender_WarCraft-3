if "parse_attachments" not in locals():
    print("load parser")
    from io_scene_warcraft_3.classes.WarCraft3Model import WarCraft3Model
    from io_scene_warcraft_3 import constants
    from io_scene_warcraft_3.importer import importer
    from io_scene_warcraft_3 import binary
    from io_scene_warcraft_3.parser.parse_attachments import parse_attachments
    from io_scene_warcraft_3.parser.parse_bones import parse_bones
    from io_scene_warcraft_3.parser.parse_collision_shapes import parse_collision_shapes
    from io_scene_warcraft_3.parser.parse_events import parse_events
    from io_scene_warcraft_3.parser.parse_geoset_animations import parse_geoset_animations
    from io_scene_warcraft_3.parser.parse_geosets import parse_geosets
    from io_scene_warcraft_3.parser.parse_helpers import parse_helpers
    from io_scene_warcraft_3.parser.parse_materials import parse_materials
    from io_scene_warcraft_3.parser.parse_model import parse_model
    from io_scene_warcraft_3.parser.parse_pivot_points import parse_pivot_points
    from io_scene_warcraft_3.parser.parse_sequences import parse_sequences
    from io_scene_warcraft_3.parser.parse_textures import parse_textures
    from io_scene_warcraft_3.parser.parse_version import parse_version
else:
    print("reload parser")
    import importlib
    from . import get_vertex_groups, load_mdx
    from . import (
        parse_attachments,
        parse_attachment_visibility,
        parse_bones,
        parse_collision_shapes,
        parse_events,
        parse_geometry,
        parse_geoset_alpha,
        parse_geoset_animations,
        parse_geoset_color,
        parse_geoset_rotation,
        parse_geoset_scaling,
        parse_geoset_translation,
        parse_geosets,
        parse_helpers,
        parse_layers,
        parse_material_alpha,
        parse_material_texture_id,
        parse_materials,
        parse_model,
        parse_node,
        parse_pivot_points,
        parse_sequences,
        parse_textures,
        parse_version
     )
    importlib.reload(get_vertex_groups)
    importlib.reload(load_mdx)
    importlib.reload(parse_attachments)
    importlib.reload(parse_attachment_visibility)
    importlib.reload(parse_bones)
    importlib.reload(parse_collision_shapes)
    importlib.reload(parse_events)
    importlib.reload(parse_geometry)
    importlib.reload(parse_geoset_alpha)
    importlib.reload(parse_geoset_animations)
    importlib.reload(parse_geoset_color)
    importlib.reload(parse_geoset_rotation)
    importlib.reload(parse_geoset_scaling)
    importlib.reload(parse_geoset_translation)
    importlib.reload(parse_geosets)
    importlib.reload(parse_helpers)
    importlib.reload(parse_layers)
    importlib.reload(parse_material_alpha)
    importlib.reload(parse_material_texture_id)
    importlib.reload(parse_materials)
    importlib.reload(parse_model)
    importlib.reload(parse_node)
    importlib.reload(parse_pivot_points)
    importlib.reload(parse_sequences)
    importlib.reload(parse_textures)
    importlib.reload(parse_version)


def parse_mdx(data, importProperties):
    dataSize = len(data)
    r = binary.Reader(data)
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
    importer.load_warcraft_3_model(model, importProperties)