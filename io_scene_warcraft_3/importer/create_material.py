import os
from pathlib import Path

import bpy

from .. import constants


def create_material(model, team_color):
    print("creating materials")
    # preferences = bpy.context.preferences.addons.get('io_scene_warcraft_3') #['io_scene_warcraft_3'].preferences
    preferences = bpy.context.user_preferences.addons['Blender_WarCraft-3_2-79'].preferences

    resource_folder: str = preferences.resourceFolder
    alternative_resource_folder = preferences.alternativeResourceFolder
    if resource_folder == '':
        print("No resource folder set in addon preferences")
    elif not resource_folder.endswith(os.path.sep):
        resource_folder += os.path.sep

    if alternative_resource_folder == '':
        print("No alt resource folder set in addon preferences")
    elif not alternative_resource_folder.endswith(os.path.sep):
        alternative_resource_folder += os.path.sep
    # try:
    #     resource_folder = preferences.resourceFolder
    #     alternative_resource_folder = preferences.alternativeResourceFolder
    # except:
    #     print("No resource folder set in addon preferences")
    # texture_exc = 'png'
    # try:
    #     texture_exc = preferences.textureExtension
    # except:
    #     print("No file extention set in addon preferences")

    texture_exc = preferences.textureExtension
    if texture_exc == '':
        print("No resource folder set in addon preferences")
        texture_exc = 'png'

    if texture_exc[0] != '.':
        texture_exc = '.' + texture_exc
    model.normalize_meshes_names()

    folders = get_folders(alternative_resource_folder, resource_folder, model)

    bpy_images = []
    for texture in model.textures:
        bpy_image = get_image(folders, team_color, texture, texture_exc)
        bpy_images.append(bpy_image)

    bpy_materials = []
    for material in model.materials:
        bpy_images_of_layer = []
        for layer in material.layers:
            bpy_images_of_layer.append(bpy_images[layer.texture_id])

        material_name = bpy_images_of_layer[-1].filepath.split(os.path.sep)[-1].split('.')[0]
        # material_name = bpy_images_of_layer[-1].filepath.split('\\')[-1].split('.')[0]
        bpy_material = bpy.data.materials.new(name=material_name)
        bpy_material.use_shadeless = True
        bpy_material.use_object_color = True
        bpy_material.diffuse_color = (1.0, 1.0, 1.0)
        texture_slot_index = 0
        for bpy_image in bpy_images_of_layer:
            bpy_material.texture_slots.add()
            bpy_texture = bpy.data.textures.new(name=material_name, type='IMAGE')
            bpy_material.texture_slots[texture_slot_index].texture = bpy_texture
            texture_slot_index += 1
            bpy_texture.image = bpy_image
        bpy_materials.append(bpy_material)


        # bpy_image = None
        # for textureSlot in bpy_material.texture_slots:
        #     if textureSlot:
        #         bpy_image = textureSlot.texture.image
        # if bpy_image:
        #     for triangleID in range(len(bpy_object.data.polygons)):
        #         bpy_object.data.uv_textures[0].data[triangleID].image = bpy_image

    return bpy_materials


def get_image(folders, team_color, texture, texture_exc):
    if texture.replaceable_id == 1:  # Team Color
        image_file = constants.TEAM_COLOR_IMAGES[team_color]
    elif texture.replaceable_id == 2:  # Team Glow
        image_file = constants.TEAM_GLOW_IMAGES[team_color]
    else:
        image_file = texture.image_file_name

    if image_file.endswith(".blp"):
        image_file = image_file.split(".blp")[0] + texture_exc
    file_path_parts = image_file.split('\\')
    # file_path_parts = image_file.split(os.path.sep)
    file_name = file_path_parts[-1].split('.')[0]
    bpy_image = bpy.data.images.new(file_name, 0, 0)
    bpy_image.source = 'FILE'
    bpy_image.filepath = image_file
    print("loading:", image_file)
    image_file.replace("\\", os.path.sep)

    for i in range(len(file_path_parts)):
        # file_path = Path(resource_folder + image_file)
        # split = image_file.split("\\", i)
        split = image_file.split(os.path.sep, i)
        image_file = split[len(split)-1]

        for folder in folders:
            file_path = check_file_path(folder, image_file)
            if file_path != '':
                bpy_image.filepath = file_path
                return bpy_image
    return bpy_image


def get_folders(alternative_folder, resource_folder, model):
    model_folder = str(Path(model.file).parent)
    # print("model folder:", model_folder)
    textures1 = "Textures" + os.path.sep
    textures2 = "textures" + os.path.sep
    folders1 = [model_folder,
                model_folder + textures1, model_folder + textures2,
                resource_folder, alternative_folder,
                resource_folder + textures1, resource_folder + textures2,
                alternative_folder + textures1, alternative_folder + textures2]
    folders = []
    for folder in folders1:
        f = check_file_path(folder, "")
        if f != '' and f not in folders:
            folders.append(f)
    return folders


def check_file_path(folder, image_file):
    file_path = folder + image_file
    # print("checking", file_path)
    try:
        if Path(file_path).exists():
            # print("got valid", file_path)
            return file_path
    except OSError:
        print("bad path:", file_path)

    return ''
