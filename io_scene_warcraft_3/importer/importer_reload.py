import importlib
print("reload importer_")
from . import importer, create_armature_actions, create_armature_object, create_mesh_objects, create_object_actions
importlib.reload(importer)
importlib.reload(create_armature_actions)
importlib.reload(create_armature_object)
importlib.reload(create_mesh_objects)
importlib.reload(create_object_actions)

# if "importer" in locals():
#     import importlib
#
#     print("reload importer")
#     from . import importer, create_armature_actions, create_armature_object, create_mesh_objects, create_object_actions
#
#     importlib.reload(importer)
#     importlib.reload(create_armature_actions)
#     importlib.reload(create_armature_object)
#     importlib.reload(create_mesh_objects)
#     importlib.reload(create_object_actions)

# if "create_armature_actions" in locals():
#     print("create_armature_actions")
# if "create_armature_object" in locals():
#     print("create_armature_object")
# if "create_mesh_objects" in locals():
#     print("create_mesh_objects")
# if "create_object_actions" in locals():
#     print("create_object_actions")


# if "create_mesh_objects" in locals():
#     print("reload importer")
#     import importlib
#     from . import importer, create_armature_actions, create_armature_object, create_mesh_objects, create_object_actions
#     importlib.reload(importer)
#     importlib.reload(create_armature_actions)
#     importlib.reload(create_armature_object)
#     importlib.reload(create_mesh_objects)
#     importlib.reload(create_object_actions)
