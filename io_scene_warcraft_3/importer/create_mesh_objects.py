import bpy

from io_scene_warcraft_3 import constants


def create_mesh_objects(model, team_color):
    preferences = bpy.context.user_preferences.addons['Blender_WarCraft-3_2-79'].preferences
    resource_folder = ''
    alternative_resource_folder = ''
    try:
        resource_folder = preferences.resourceFolder
        alternative_resource_folder = preferences.alternativeResourceFolder
    except:
        print("No resource folder set in addon preferences")

    texture_exc = 'png'
    try:
        texture_exc = preferences.textureExtension
    except:
        print("No file extention set in addon preferences")

    if texture_exc[0] != '.':
        texture_exc = '.' + texture_exc
    model.normalize_meshes_names()
    bpy_images = []
    for texture in model.textures:
        if texture.replaceable_id == 1:    # Team Color
            image_file = constants.TEAM_COLOR_IMAGES[team_color]
        elif texture.replaceable_id == 2:    # Team Glow
            image_file = constants.TEAM_GLOW_IMAGES[team_color]
        else:
            image_file = texture.image_file_name
        bpy_image = bpy.data.images.new(image_file.split('\\')[-1].split('.')[0], 0, 0)
        bpy_image.source = 'FILE'
        image_file_ext = image_file.split('\\')[-1].split('.')[-1]
        if image_file_ext == 'blp':
            bpy_image.filepath = alternative_resource_folder + image_file.split('.')[0] + texture_exc
        else:
            bpy_image.filepath = resource_folder + image_file
        bpy_images.append(bpy_image)
    bpy_materials = []
    for material in model.materials:
        bpy_images_of_layer = []
        for layer in material.layers:
            bpy_images_of_layer.append(bpy_images[layer.texture_id])
        material_name = bpy_images_of_layer[-1].filepath.split('\\')[-1].split('.')[0]
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
    bpy_objects = []
    for warCraft3Mesh in model.meshes:
        bpy_mesh = bpy.data.meshes.new(warCraft3Mesh.name)
        bpy_object = bpy.data.objects.new(warCraft3Mesh.name, bpy_mesh)
        bpy.context.scene.objects.link(bpy_object)
        bpy_mesh.from_pydata(warCraft3Mesh.vertices, (), warCraft3Mesh.triangles)
        bpy_mesh.uv_textures.new()
        uv_layer = bpy_mesh.uv_layers.active.data
        for tris in bpy_mesh.polygons:
            for loopIndex in range(tris.loop_start, tris.loop_start + tris.loop_total):
                vertex_index = bpy_mesh.loops[loopIndex].vertex_index
                uv_layer[loopIndex].uv = (warCraft3Mesh.uvs[vertex_index])
        bpy_material = bpy_materials[warCraft3Mesh.material_id]
        bpy_mesh.materials.append(bpy_material)
        bpy_image = None
        for textureSlot in bpy_material.texture_slots:
            if textureSlot:
                bpy_image = textureSlot.texture.image
        if bpy_image:
            for triangleID in range(len(bpy_object.data.polygons)):
                bpy_object.data.uv_textures[0].data[triangleID].image = bpy_image
        for vertexGroupId in warCraft3Mesh.vertex_groups_ids:
            bpy_object.vertex_groups.new(str(vertexGroupId))
        for vertex_index, vertexGroupIds in enumerate(warCraft3Mesh.vertex_groups):
            for vertexGroupId in vertexGroupIds:
                bpy_object.vertex_groups[str(vertexGroupId)].add([vertex_index, ], 1.0, 'REPLACE')
        bpy_objects.append(bpy_object)
    return bpy_objects
