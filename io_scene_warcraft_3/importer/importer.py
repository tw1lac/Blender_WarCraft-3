from .create_armature_actions import create_armature_actions
from .create_armature_object import create_armature_object
from .create_mesh_objects import create_mesh_objects
from .create_object_actions import create_object_actions


def load_warcraft_3_model(model, importProperties):
    bpyObjects = create_mesh_objects(model, importProperties.set_team_color)
    armatureObject = create_armature_object(model, bpyObjects, importProperties.bone_size)
    create_armature_actions(armatureObject, model, importProperties.frame_time)
    create_object_actions(model, bpyObjects, importProperties.frame_time)
