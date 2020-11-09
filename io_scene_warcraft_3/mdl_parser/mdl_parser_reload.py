if "load_mdl" in locals():
    print("reload mdl_parser")
    import importlib
    from . import get_vertex_groups, load_mdl
    from . import (
        parse_attachments,
        parse_bones,
        parse_collision_shapes,
        parse_events,
        parse_geometry,
        parse_geoset_animations,
        parse_geoset_color,
        parse_geoset_transformation,
        parse_geosets,
        parse_helpers,
        parse_materials,
        parse_mdl,
        parse_model,
        parse_node,
        parse_pivot_points,
        parse_sequences,
        parse_textures,
        parse_version
     )
    importlib.reload(get_vertex_groups)
    importlib.reload(load_mdl)
    importlib.reload(parse_attachments)
    importlib.reload(parse_bones)
    importlib.reload(parse_collision_shapes)
    importlib.reload(parse_events)
    importlib.reload(parse_geometry)
    importlib.reload(parse_geoset_animations)
    importlib.reload(parse_geoset_color)
    importlib.reload(parse_geoset_transformation)
    importlib.reload(parse_geosets)
    importlib.reload(parse_helpers)
    importlib.reload(parse_materials)
    importlib.reload(parse_mdl)
    importlib.reload(parse_model)
    importlib.reload(parse_node)
    importlib.reload(parse_pivot_points)
    importlib.reload(parse_sequences)
    importlib.reload(parse_textures)
    importlib.reload(parse_version)