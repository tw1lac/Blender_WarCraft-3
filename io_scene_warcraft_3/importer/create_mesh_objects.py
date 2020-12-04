import bpy

from io_scene_warcraft_3.importer.create_material import create_material


def create_mesh_objects(model, bpyMaterials):
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


