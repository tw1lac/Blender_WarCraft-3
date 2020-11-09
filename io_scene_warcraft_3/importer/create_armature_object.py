import bpy


def create_armature_object(model, bpyObjects, boneSize):
    nodes = model.nodes
    pivotPoints = model.pivot_points
    bpyArmature = bpy.data.armatures.new(model.name + ' Nodes')
    bpyArmature.display_type = 'STICK'
    bpyObject = bpy.data.objects.new(model.name + ' Nodes', bpyArmature)
    bpyObject.show_in_front = True
    bpy.context.scene.collection.objects.link(bpyObject)
    bpyObject.select_set(True)
    bpy.context.view_layer.objects.active = bpyObject
    # bpy.context.scene.objects.active = bpyObject
    bpy.ops.object.mode_set(mode='EDIT')

    nodeTypes = set()
    boneTypes = {}

    for indexNode, node in enumerate(nodes):
        nodePosition = pivotPoints[indexNode]
        boneName = node.node.name
        nodeTypes.add(node.type)
        bone = bpyArmature.edit_bones.new(boneName)
        bone.head = nodePosition
        bone.tail = nodePosition
        bone.tail[1] += boneSize
        boneTypes[boneName] = node.type

    nodeTypes = list(nodeTypes)
    nodeTypes.sort()

    for indexNode, node in enumerate(nodes):
        bone = bpyArmature.edit_bones[indexNode]
        if node.node.parent is not None:
            parent = bpyArmature.edit_bones[node.node.parent]
            bone.parent = parent
            # bone.use_connect = True

    for mesh in bpyObjects:
        mesh.modifiers.new(name='Armature', type='ARMATURE')
        mesh.modifiers['Armature'].object = bpyObject
        for vertexGroup in mesh.vertex_groups:
            vertexGroupIndex = int(vertexGroup.name)
            boneName = bpyArmature.edit_bones[vertexGroupIndex].name
            vertexGroup.name = boneName

    bpy.ops.object.mode_set(mode='POSE')
    boneGroups = {}

    for nodeType in nodeTypes:
        bpy.ops.pose.group_add()
        boneGroup = bpyObject.pose.bone_groups.active
        boneGroup.name = nodeType + 's'
        boneGroups[nodeType] = boneGroup
        if nodeType == 'bone':
            boneGroup.color_set = 'THEME04'
        elif nodeType == 'attachment':
            boneGroup.color_set = 'THEME09'
        elif nodeType == 'collision_shape':
            boneGroup.color_set = 'THEME02'
        elif nodeType == 'event':
            boneGroup.color_set = 'THEME03'
        elif nodeType == 'helper':
            boneGroup.color_set = 'THEME01'

    for bone in bpyObject.pose.bones:
        bone.rotation_mode = 'XYZ'
        bone.bone_group = boneGroups[boneTypes[bone.name]]

    for bone in bpyArmature.bones:
        bone.warcraft_3.nodeType = boneTypes[bone.name].upper()

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.active_object.select_set(False)

    return bpyObject
