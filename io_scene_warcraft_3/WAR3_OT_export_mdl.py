import bpy
from bpy.props import StringProperty, BoolProperty, FloatProperty
from bpy.types import Operator
from bpy_extras.io_utils import orientation_helper, ExportHelper, axis_conversion
from mathutils import Matrix

from .classes.War3ExportSettings import War3ExportSettings


@orientation_helper(axis_forward='Y', axis_up='Z')
class WAR3_OT_export_mdl(Operator, ExportHelper):
    """MDL Exporter"""
    bl_idname = 'warcraft_3.mdl_exporter'
    bl_description = 'Warctaft 3 MDL Exporter'
    bl_label = 'Twilac .MDL'
    filename_ext = ".mdl"

    filter_glob: StringProperty(
            default="*.mdl", options={'HIDDEN'}
            )

    filepath: StringProperty(
            subtype="FILE_PATH"
            )

    use_selection: BoolProperty(
            name="Selected Objects",
            description="Export only selected objects on visible layers",
            default=False,
            )

    global_scale: FloatProperty(
            name="Scale",
            min=0.01,
            max=1000.0,
            default=1,
            )

    optimize_animation: BoolProperty(
            name="Optimize Keyframes",
            description="Remove keyframes if the resulting motion deviates less than the tolerance value."
            )

    use_actions: BoolProperty(
            name="Use Actions",
            description="Use actions instead of mdl-sequences"
            )

    optimize_tolerance: FloatProperty(
            name="Tolerance",
            min=0.001,
            soft_max=0.1,
            default=0.05,
            subtype='DISTANCE',
            unit='LENGTH'
            )

    def execute(self, context):
        filepath = self.filepath
        filepath = bpy.path.ensure_ext(filepath, self.filename_ext)

        settings = War3ExportSettings()
        settings.global_matrix = axis_conversion(
            to_forward=self.axis_forward,
            to_up=self.axis_up,
        ).to_4x4() @ Matrix.Scale(self.global_scale, 4)

        settings.use_selection = self.use_selection
        settings.optimize_animation = self.optimize_animation
        settings.optimize_tolerance = self.optimize_tolerance
        settings.use_actions = self.use_actions

        from .mdl_exporter.write_file.file_writer import file_writer
        file_writer(self, context, settings, filepath=filepath, mdl_version=800)

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "use_selection")
        layout.prop(self, "global_scale")
        layout.prop(self, "axis_forward")
        layout.prop(self, "axis_up")
        layout.separator()
        layout.prop(self, 'optimize_animation')
        layout.prop(self, 'use_actions')
        if self.optimize_animation:
            box = layout.box()
            box.label(text="EXPERIMENTAL", icon='ERROR')
            layout.prop(self, 'optimize_tolerance')
        if self.use_actions:
            box = layout.box()
            box.label(text="EXPERIMENTAL", icon='ERROR')
            box.label(text="Will export action and not marker based sequences. "
                           "This does not yet support Rarity or NonLooping")
            # layout.prop(self, 'use_actions')
