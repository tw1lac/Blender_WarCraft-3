if "create_armature_actions" not in locals():
    print("load importer")
    from io_scene_warcraft_3.importer.create_armature_actions import create_armature_actions
    from io_scene_warcraft_3.importer.create_armature_object import create_armature_object
    from io_scene_warcraft_3.importer.create_mesh_objects import create_mesh_objects
    from io_scene_warcraft_3.importer.create_object_actions import create_object_actions
else:
    print("reload importer")
    import importlib
    from . import create_armature_actions, create_armature_object, create_mesh_objects, create_object_actions
    importlib.reload(create_armature_actions)
    importlib.reload(create_armature_object)
    importlib.reload(create_mesh_objects)
    importlib.reload(create_object_actions)


def load_warcraft_3_model(model, importProperties):
    bpyObjects = create_mesh_objects(model, importProperties.set_team_color)
    armatureObject = create_armature_object(model, bpyObjects, importProperties.bone_size)
    create_armature_actions(armatureObject, model, importProperties.frame_time)
    create_object_actions(model, bpyObjects, importProperties.frame_time)
