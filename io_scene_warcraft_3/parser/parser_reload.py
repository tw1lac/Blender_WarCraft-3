if "load_mdx" in locals():
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
        parse_mdx,
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
    importlib.reload(parse_mdx)
    importlib.reload(parse_model)
    importlib.reload(parse_node)
    importlib.reload(parse_pivot_points)
    importlib.reload(parse_sequences)
    importlib.reload(parse_textures)
    importlib.reload(parse_version)