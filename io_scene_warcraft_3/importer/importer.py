from .create_armature_actions import create_armature_actions
from .create_armature_object import create_armature_object
from .create_material import create_material
from .create_mesh_objects import create_mesh_objects
from .create_object_actions import create_object_actions


def load_warcraft_3_model(model, import_properties):
    bpy_materials = create_material(model, import_properties.team_color)
    bpy_objects = create_mesh_objects(model, bpy_materials)
    armature_object = create_armature_object(model, bpy_objects, import_properties.bone_size)
    create_armature_actions(armature_object, model, import_properties.frame_time)
    create_object_actions(model, bpy_objects, import_properties.frame_time)
