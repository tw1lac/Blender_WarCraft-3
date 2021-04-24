
import bpy

from io_scene_warcraft_3.mdx_parser.load_mdx import load_mdx
from io_scene_warcraft_3.classes.MDXImportProperties import MDXImportProperties
from io_scene_warcraft_3 import utils, constants
from bpy_extras import io_utils


class WarCraft3OperatorImportMDX(bpy.types.Operator, io_utils.ImportHelper):
    bl_idname = 'warcraft_3.import_mdx'
    bl_label = 'Import *.mdx'
    bl_description = 'Import *.mdx files (3d models of WarCraft 3)'
    bl_options = {'UNDO'}

    filename_ext = '.mdx'
    filter_glob = bpy.props.StringProperty(default='*.mdx', options={'HIDDEN'})
    filepath = bpy.props.StringProperty(name='File Path', maxlen=1024, default='')
    useCustomFPS = bpy.props.BoolProperty(name='Use Custom FPS', default=False)
    animationFPS = bpy.props.FloatProperty(name='Animation FPS', default=30.0, min=1.0, max=1000.0)
    boneSize = bpy.props.FloatProperty(name='Bone Size', default=5.0, min=0.0001, max=1000.0)
    teamColor = bpy.props.FloatVectorProperty(
        name='Team Color',
        default=constants.TEAM_COLORS['RED'],
        min=0.0,
        max=1.0,
        size=3,
        subtype='COLOR',
        precision=3
        )
    setTeamColor = bpy.props.EnumProperty(
        items=[
            ('RED', 'Red', ''),
            ('DARK_BLUE', 'Dark Blue', ''),
            ('TURQUOISE', 'Turquoise', ''),
            ('VIOLET', 'Violet', ''),
            ('YELLOW', 'Yellow', ''),
            ('ORANGE', 'Orange', ''),
            ('GREEN', 'Green', ''),
            ('PINK', 'Pink', ''),
            ('GREY', 'Grey', ''),
            ('BLUE', 'Blue', ''),
            ('DARK_GREEN', 'Dark Green', ''),
            ('BROWN', 'Brown', ''),
            ('BLACK', 'Black', '')
            ],
        name='Set Team Color',
        update=utils.set_team_color_property,
        default='RED'
        )

    def draw(self, context):
        layout = self.layout
        split = layout.split(percentage=0.9)
        sub_split = split.split(percentage=0.5)
        sub_split.label('Team Color:')
        sub_split.prop(self.properties, 'setTeamColor', text='')
        split.prop(self.properties, 'teamColor', text='')
        layout.prop(self.properties, 'boneSize')
        layout.prop(self.properties, 'useCustomFPS')
        if self.properties.useCustomFPS:
            layout.prop(self.properties, 'animationFPS')

    def execute(self, context):
        import_properties = MDXImportProperties()
        import_properties.mdx_file_path = self.properties.filepath
        import_properties.set_team_color = self.properties.setTeamColor
        import_properties.bone_size = self.properties.boneSize
        import_properties.use_custom_fps = self.properties.useCustomFPS
        import_properties.fps = self.properties.animationFPS
        import_properties.calculate_frame_time()
        load_mdx(import_properties)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class WarCraft3OperatorAddSequenceToArmature(bpy.types.Operator):
    bl_idname = 'warcraft_3.add_sequence_to_armature'
    bl_label = 'WarCraft 3 Add Sequence to Armature'
    bl_description = 'WarCraft 3 Add Sequence to Armature'
    bl_options = {'UNDO'}

    def execute(self, context):
        if context.armature:
            warcraft3data = context.armature.warcraft_3
            sequence = warcraft3data.sequencesList.add()
            sequence.name = '#UNANIMATED'
        return {'FINISHED'}


class WarCraft3OperatorRemoveSequenceToArmature(bpy.types.Operator):
    bl_idname = 'warcraft_3.remove_sequence_to_armature'
    bl_label = 'WarCraft 3 Remove Sequence to Armature'
    bl_description = 'WarCraft 3 Remove Sequence to Armature'
    bl_options = {'UNDO'}

    def execute(self, context):
        if context.armature:
            warcraft3data = context.armature.warcraft_3
            warcraft3data.sequencesList.remove(warcraft3data.sequencesListIndex)
        return {'FINISHED'}


class WarCraft3OperatorUpdateBoneSettings(bpy.types.Operator):
    bl_idname = 'warcraft_3.update_bone_settings'
    bl_label = 'WarCraft 3 Update Bone Settings'
    bl_description = 'WarCraft 3 Update Bone Settings'
    bl_options = {'UNDO'}

    def execute(self, context):
        bpy_object = context.object
        for bone in bpy_object.data.bones:
            node_type = bone.warcraft_3.nodeType
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
        return {'FINISHED'}
