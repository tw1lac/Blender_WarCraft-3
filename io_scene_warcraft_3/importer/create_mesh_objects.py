import bpy



def create_mesh_objects(model, bpyMaterials):
    print("creating mesh")
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

        for vertexGroupId in warCraft3Mesh.vertex_groups_ids:
            bpyObject.vertex_groups.new(name=str(vertexGroupId))

        for vertexIndex in range(len(warCraft3Mesh.skin_weights)):
            skin_weight = warCraft3Mesh.skin_weights[vertexIndex]
            if skin_weight[0] != 255 and skin_weight[4] != 0:
                bpyObject.vertex_groups.get(str(skin_weight[0])).add([vertexIndex, ], skin_weight[4]/255.0, 'REPLACE')
            if skin_weight[1] != 255 and skin_weight[5] != 0:
                bpyObject.vertex_groups.get(str(skin_weight[1])).add([vertexIndex, ], skin_weight[5]/255.0, 'REPLACE')
            if skin_weight[2] != 255 and skin_weight[6] != 0:
                bpyObject.vertex_groups.get(str(skin_weight[2])).add([vertexIndex, ], skin_weight[6]/255.0, 'REPLACE')
            if skin_weight[3] != 255 and skin_weight[7] != 0:
                bpyObject.vertex_groups.get(str(skin_weight[3])).add([vertexIndex, ], skin_weight[7]/255.0, 'REPLACE')

        for vertexIndex, vertexGroupIds in enumerate(warCraft3Mesh.vertex_groups):
            for vertexGroupId in vertexGroupIds:
                bpyObject.vertex_groups.get(str(vertexGroupId)).add([vertexIndex, ], 1.0, 'REPLACE')

        bpyObjects.append(bpyObject)
    return bpyObjects


