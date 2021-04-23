from typing import List

from bpy.types import Material, Object

from io_scene_warcraft_3.classes.MDXImportProperties import MDXImportProperties
from io_scene_warcraft_3.classes.WarCraft3Model import WarCraft3Model
from io_scene_warcraft_3.importer.create_armature_actions import create_armature_actions
from io_scene_warcraft_3.importer.create_armature_object import create_armature_object
from io_scene_warcraft_3.importer.create_mesh_objects import create_mesh_objects
from io_scene_warcraft_3.importer.create_material import create_material
from io_scene_warcraft_3.importer.create_object_actions import create_object_actions


def load_warcraft_3_model(model: WarCraft3Model, import_properties: MDXImportProperties):

    bpy_materials: List[Material] = create_material(model, import_properties.team_color)
    bpy_objects: List[Object] = create_mesh_objects(model, bpy_materials)
    armature_object: Object = create_armature_object(model, bpy_objects, import_properties.bone_size)
    create_armature_actions(armature_object, model, import_properties.frame_time)
    create_object_actions(model, bpy_objects, import_properties.frame_time)
