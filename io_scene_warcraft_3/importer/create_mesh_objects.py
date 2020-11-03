import bpy

from io_scene_warcraft_3 import constants


def create_mesh_objects(model, setTeamColor):
    # preferences = bpy.context.preferences.addons.get('io_scene_warcraft_3') #['io_scene_warcraft_3'].preferences
    preferences = bpy.context.preferences.addons.get('io_scene_warcraft_3').preferences
    resourceFolder = ''
    alternativeResourceFolder = ''
    try:
        resourceFolder = preferences.resourceFolder
        alternativeResourceFolder = preferences.alternativeResourceFolder
    except:
        print("No resource folder set in addon preferences")

    textureExc = 'png'
    try:
        textureExc = preferences.textureExtension
    except:
        print("No file extention set in addon preferences")

    if textureExc[0] != '.':
        textureExc = '.' + textureExc
    model.normalize_meshes_names()
    bpyImages = []
    for texture in model.textures:
        if texture.replaceable_id == 1:    # Team Color
            imageFile = constants.TEAM_COLOR_IMAGES[setTeamColor]
        elif texture.replaceable_id == 2:    # Team Glow
            imageFile = constants.TEAM_GLOW_IMAGES[setTeamColor]
        else:
            imageFile = texture.image_file_name
        bpyImage = bpy.data.images.new(imageFile.split('\\')[-1].split('.')[0], 0, 0)
        bpyImage.source = 'FILE'
        imageFileExt = imageFile.split('\\')[-1].split('.')[-1]
        if imageFileExt == 'blp':
            bpyImage.filepath = alternativeResourceFolder + imageFile.split('.')[0] + textureExc
            print("alt folder\n", alternativeResourceFolder + imageFile.split('.')[0] + textureExc)
        else:
            bpyImage.filepath = resourceFolder + imageFile
            print("main folder\n", resourceFolder + imageFile)
        bpyImages.append(bpyImage)
    bpyMaterials = []
    for material in model.materials:
        bpyImagesOfLayer = []
        for layer in material.layers:
            bpyImagesOfLayer.append(bpyImages[layer.texture_id])
        materialName = bpyImagesOfLayer[-1].filepath.split('\\')[-1].split('.')[0]
        bpyMaterial = bpy.data.materials.new(name=materialName)
        bpyMaterial.shadow_method = 'NONE'
        # bpyMaterial.use_object_color = True
        bpyMaterial.use_nodes = True
        # bsdf_node = bpyMaterial.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
        # bsdf_node.color = (1.0, 1.0, 1.0, 1.0)
        # bpyMaterial.node_tree.nodes.get("Material Output")
        bpyMaterial.diffuse_color = (1.0, 1.0, 1.0, 1.0)
        textureSlotIndex = 0
        for bpyImage in bpyImagesOfLayer:
            texImage = bpyMaterial.node_tree.nodes.new('ShaderNodeTexImage')
            texImage.image = bpyImage
            bpyMaterial.node_tree.links.new(texImage.outputs.get("Color"), bpyMaterial.node_tree.nodes.get("Principled BSDF").inputs.get("Base Color"))
            # bpyMaterial.texture_slots.add()
            # bpyTexture = bpy.data.textures.new(name=materialName, type='IMAGE')
            # bpyMaterial.texture_slots[textureSlotIndex].texture = bpyTexture
            # textureSlotIndex += 1
            # bpyTexture.image = bpyImage
        bpyMaterials.append(bpyMaterial)
    bpyObjects = []
    for warCraft3Mesh in model.meshes:
        bpyMesh = bpy.data.meshes.new(warCraft3Mesh.name)
        bpyObject = bpy.data.objects.new(warCraft3Mesh.name, bpyMesh)
        bpy.context.scene.collection.objects.link(bpyObject)
        bpyMesh.from_pydata(warCraft3Mesh.vertices, (), warCraft3Mesh.triangles)
        bpyMesh.uv_layers.new()
        uvLayer = bpyMesh.uv_layers.active.data
        for tris in bpyMesh.polygons:
            for loopIndex in range(tris.loop_start, tris.loop_start + tris.loop_total):
                vertexIndex = bpyMesh.loops[loopIndex].vertex_index
                uvLayer[loopIndex].uv = (warCraft3Mesh.uvs[vertexIndex])
        bpyMaterial = bpyMaterials[warCraft3Mesh.material_id]
        bpyMesh.materials.append(bpyMaterial)
        # bpyImage = None
        # for textureSlot in bpyMaterial.texture_slots:
        #     if textureSlot:
        #         bpyImage = textureSlot.texture.image
        # if bpyImage:
        #     for triangleID in range(len(bpyObject.data.polygons)):
        #         bpyObject.data.uv_textures[0].data[triangleID].image = bpyImage
        for vertexGroupId in warCraft3Mesh.vertex_groups_ids:
            bpyObject.vertex_groups.new(name=str(vertexGroupId))
        for vertexIndex, vertexGroupIds in enumerate(warCraft3Mesh.vertex_groups):
            for vertexGroupId in vertexGroupIds:
                bpyObject.vertex_groups.get(str(vertexGroupId)).add([vertexIndex, ], 1.0, 'REPLACE')
        bpyObjects.append(bpyObject)
    return bpyObjects
