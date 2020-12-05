import bpy

from io_scene_warcraft_3 import constants


def create_material(model, setTeamColor):
    print("creating materials")
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
        if texture.replaceable_id == 1:  # Team Color
            imageFile = constants.TEAM_COLOR_IMAGES[setTeamColor]
        elif texture.replaceable_id == 2:  # Team Glow
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
        if material.hd:
            bpyMaterial.blend_method = 'HASHED'
            bpyMaterial.shadow_method = 'HASHED'
            shader = bpyMaterial.node_tree.nodes.get("Principled BSDF")
            diffuse = bpyMaterial.node_tree.nodes.new('ShaderNodeMixRGB')
            diffuse.blend_type = 'COLOR'
            i = 0
            for bpyImage in bpyImagesOfLayer:
                texImage = bpyMaterial.node_tree.nodes.new('ShaderNodeTexImage')
                texImage.image = bpyImage
                if i == 0:
                    bpyMaterial.node_tree.links.new(texImage.outputs.get("Color"), diffuse.inputs.get("Color1"))
                    bpyMaterial.node_tree.links.new(diffuse.outputs.get("Color"), shader.inputs.get("Base Color"))
                    bpyMaterial.node_tree.links.new(texImage.outputs.get("Alpha"), shader.inputs.get("Alpha"))
                elif i == 1:
                    normalMap = bpyMaterial.node_tree.nodes.new('ShaderNodeNormalMap')
                    bpyMaterial.node_tree.links.new(texImage.outputs.get("Color"), normalMap.inputs.get("Color"))
                    bpyMaterial.node_tree.links.new(normalMap.outputs.get("Normal"), shader.inputs.get("Normal"))
                elif i == 2:
                    orm = bpyMaterial.node_tree.nodes.new('ShaderNodeSeparateRGB')
                    bpyMaterial.node_tree.links.new(texImage.outputs.get("Color"), orm.inputs.get("Image"))
                    # I don't currently know how to do occlusion
                    bpyMaterial.node_tree.links.new(orm.outputs.get("G"), shader.inputs.get("Roughness"))
                    bpyMaterial.node_tree.links.new(orm.outputs.get("B"), shader.inputs.get("Metallic"))
                    bpyMaterial.node_tree.links.new(texImage.outputs.get("Alpha"), diffuse.inputs.get("Fac"))
                elif i == 3:
                    bpyMaterial.node_tree.links.new(texImage.outputs.get("Color"), shader.inputs.get("Emission"))
                elif i == 4:
                    bpyMaterial.node_tree.links.new(texImage.outputs.get("Color"), diffuse.inputs.get("Color2"))
                #else:
                    # skip the environmental map, possibly change the world's map to it
                print(bpyImage.filepath, " at place ", i)
                i+=1
        else:
            for bpyImage in bpyImagesOfLayer:
                texImage = bpyMaterial.node_tree.nodes.new('ShaderNodeTexImage')
                texImage.image = bpyImage
                bpyMaterial.node_tree.links.new(texImage.outputs.get("Color"),
                                                bpyMaterial.node_tree.nodes.get("Principled BSDF").inputs.get("Base Color"))
                # bpyMaterial.texture_slots.add()
                # bpyTexture = bpy.data.textures.new(name=materialName, type='IMAGE')
                # bpyMaterial.texture_slots[textureSlotIndex].texture = bpyTexture
                # textureSlotIndex += 1
                # bpyTexture.image = bpyImage
        bpyMaterials.append(bpyMaterial)

    # bpyMaterial = bpyMaterials[warCraft3Mesh.material_id]
    # bpyMesh.materials.append(bpyMaterial)
    # # bpyImage = None
    # # for textureSlot in bpyMaterial.texture_slots:
    # #     if textureSlot:
    # #         bpyImage = textureSlot.texture.image
    # # if bpyImage:
    # #     for triangleID in range(len(bpyObject.data.polygons)):
    # #         bpyObject.data.uv_textures[0].data[triangleID].image = bpyImage

    return bpyMaterials