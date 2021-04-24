import bpy


def create_armature_object(model, bpy_objects, bone_size):
    nodes = model.nodes
    pivot_points = model.pivot_points
    bpy_armature = bpy.data.armatures.new(model.name + ' Nodes')
    bpy_armature.draw_type = 'STICK'
    bpy_object = bpy.data.objects.new(model.name + ' Nodes', bpy_armature)
    bpy_object.show_x_ray = True
    bpy.context.scene.objects.link(bpy_object)
    bpy.context.scene.objects.active = bpy_object
    bpy.ops.object.mode_set(mode='EDIT')
    node_types = set()
    bone_types = {}

    for indexNode, node in enumerate(nodes):
        node_position = pivot_points[indexNode]
        bone_name = node.node.name
        node_types.add(node.type)
        bone = bpy_armature.edit_bones.new(bone_name)
        bone.head = node_position
        bone.tail = node_position
        bone.tail[1] += bone_size
        bone_types[bone_name] = node.type

    node_types = list(node_types)
    node_types.sort()

    for indexNode, node in enumerate(nodes):
        bone = bpy_object.data.edit_bones[indexNode]
        if node.node.parent:
            parent = bpy_object.data.edit_bones[node.node.parent]
            bone.parent = parent
            # bone.use_connect = True

    for mesh in bpy_objects:
        mesh.modifiers.new(name='Armature', type='ARMATURE')
        mesh.modifiers['Armature'].object = bpy_object

        for vertexGroup in mesh.vertex_groups:
            vertex_group_index = int(vertexGroup.name)
            bone_name = bpy_object.data.edit_bones[vertex_group_index].name
            vertexGroup.name = bone_name

    bpy.ops.object.mode_set(mode='POSE')
    bone_groups = {}

    for nodeType in node_types:
        bpy.ops.pose.group_add()
        bone_group = bpy_object.pose.bone_groups.active
        bone_group.name = nodeType + 's'
        bone_groups[nodeType] = bone_group
        if nodeType == 'bone':
            bone_group.color_set = 'THEME04'
        elif nodeType == 'attachment':
            bone_group.color_set = 'THEME09'
        elif nodeType == 'collision_shape':
            bone_group.color_set = 'THEME02'
        elif nodeType == 'event':
            bone_group.color_set = 'THEME03'
        elif nodeType == 'helper':
            bone_group.color_set = 'THEME01'
    for bone in bpy_object.pose.bones:
        bone.rotation_mode = 'XYZ'
        bone.bone_group = bone_groups[bone_types[bone.name]]
    for bone in bpy_object.data.bones:
        bone.warcraft_3.nodeType = bone_types[bone.name].upper()
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects.active = None
    return bpy_object
