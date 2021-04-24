
import bpy
from . import constants


ACTION_NAME_UNANIMATED = '#UNANIMATED'


def set_animation(self, context):
    set_animation_name = context.armature.warcraft_3.sequencesList[context.armature.warcraft_3.sequencesListIndex].name
    if len(set_animation_name) and bpy.data.actions.get(set_animation_name, None):
        armature_object = context.object
        if armature_object.animation_data is None:
            armature_object.animation_data_create()
        set_action = bpy.data.actions[set_animation_name]
        armature_object.animation_data.action = set_action
        bpy.context.scene.frame_start = set_action.frame_range[0]
        bpy.context.scene.frame_end = set_action.frame_range[1]
        for action in bpy.data.actions:
            for bpy_object in bpy.context.scene.objects:
                set_object_animation_name = set_animation_name + ' ' + bpy_object.name
                if action.name == set_object_animation_name:
                    if bpy_object.animation_data is None:
                        bpy_object.animation_data_create()
                    bpy_object.animation_data.action = action
    else:
        action = bpy.data.actions.get(ACTION_NAME_UNANIMATED, None)
        if action:
            armature_object = context.object
            if armature_object.animation_data is None:
                armature_object.animation_data_create()
            set_action = bpy.data.actions[ACTION_NAME_UNANIMATED]
            armature_object.animation_data.action = set_action
            bpy.context.scene.frame_start = set_action.frame_range[0]
            bpy.context.scene.frame_end = set_action.frame_range[1]
            for bpy_object in bpy.context.scene.objects:
                object_action_name = ACTION_NAME_UNANIMATED + ' ' + bpy_object.name
                if bpy.data.actions.get(object_action_name, None):
                    if bpy_object.animation_data is None:
                        bpy_object.animation_data_create()
                    bpy_object.animation_data.action = bpy.data.actions[object_action_name]


def set_team_color_property(self, context):
    self.teamColor = constants.TEAM_COLORS[self.setTeamColor]


def set_bone_node_type(self, context):
    bone = context.active_bone
    if bone:
        node_type = bone.warcraft_3.nodeType
        bpy_object = context.object
        bone_group = bpy_object.pose.bone_groups.get(node_type.lower() + 's', None)
        if not bone_group:
            if node_type in {'BONE', 'ATTACHMENT', 'COLLISION_SHAPE', 'EVENT', 'HELPER'}:
                bpy.ops.pose.group_add()
                bone_group = bpy_object.pose.bone_groups.active
                bone_group.name = node_type.lower() + 's'
                if node_type == 'BONE':
                    bone_group.color_set = 'THEME04'
                elif node_type == 'ATTACHMENT':
                    bone_group.color_set = 'THEME09'
                elif node_type == 'COLLISION_SHAPE':
                    bone_group.color_set = 'THEME02'
                elif node_type == 'EVENT':
                    bone_group.color_set = 'THEME03'
                elif node_type == 'HELPER':
                    bone_group.color_set = 'THEME01'
            else:
                bone_group = None
        bpy_object.pose.bones[bone.name].bone_group = bone_group
