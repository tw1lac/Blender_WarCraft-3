import bpy

from io_scene_warcraft_3 import constants


def create_mesh_objects(model, bpy_materials):
    print("creating mesh")
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

        for vertex_index in range(len(warCraft3Mesh.skin_weights)):
            skin_weight = warCraft3Mesh.skin_weights[vertex_index]
            if sum(skin_weight[4:]) > 300:
                for i in range(0, 5):
                    sw = skin_weight[i + 4]
                    if sw != 0:
                        bpy_object.vertex_groups[str(skin_weight[i])].add([vertex_index, ], sw / 255.0, 'REPLACE')

        for vertex_index, vertexGroupIds in enumerate(warCraft3Mesh.vertex_groups):
            for vertexGroupId in vertexGroupIds:
                bpy_object.vertex_groups[str(vertexGroupId)].add([vertex_index, ], 1.0, 'REPLACE')
        bpy_objects.append(bpy_object)
    return bpy_objects
