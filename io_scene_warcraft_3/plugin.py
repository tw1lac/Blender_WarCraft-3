if "bpy" not in locals():
    print("load plugin")
    import bpy
    from .operators import WarCraft3OperatorImportMDX, WarCraft3OperatorAddSequenceToArmature, \
        WarCraft3OperatorRemoveSequenceToArmature, WarCraft3OperatorUpdateBoneSettings
    from .ui import WarCraft3PanelBone, WarCraft3PanelArmature
    from .preferences import WarCraft3Preferences
    from .types import WarCraft3ArmatureSequenceList, WarCraft3ArmatureProperties, WarCraft3BoneProperties
else:
    print("reload plugin")
    import importlib
    from . import operators
    from . import ui
    from . import preferences
    from . import types
    from .classes import classes_reload
    from . import constants
    from .importer import importer_reload
    from .mdx_parser import parser_reload, binary_reader
    from . import utils
    try:
        importlib.reload(operators)
        importlib.reload(ui)
        importlib.reload(preferences)
        importlib.reload(types)
        importlib.reload(binary_reader)
        importlib.reload(classes_reload)
        importlib.reload(constants)
        importlib.reload(importer_reload)
        importlib.reload(parser_reload)
        importlib.reload(utils)
    except ImportError:
        print("could not reload module")


def menu_import_mdx(self, context):
    self.layout.operator(WarCraft3OperatorImportMDX.bl_idname, text='Warcraft 3 (.mdl/.mdx)')


wc_classes = (
    WarCraft3OperatorImportMDX,
    WarCraft3OperatorAddSequenceToArmature,
    WarCraft3OperatorRemoveSequenceToArmature,
    WarCraft3OperatorUpdateBoneSettings,
    WarCraft3PanelBone,
    WarCraft3PanelArmature,
)

prop_classes = (
    WarCraft3Preferences,
    WarCraft3ArmatureSequenceList,
    WarCraft3ArmatureProperties,
    WarCraft3BoneProperties
)


def register():
    for cls in prop_classes:
        bpy.utils.register_class(cls)
    WarCraft3ArmatureProperties.bpy_type.warcraft_3 = bpy.props.PointerProperty(type=WarCraft3ArmatureProperties)
    WarCraft3BoneProperties.bpy_type.warcraft_3 = bpy.props.PointerProperty(type=WarCraft3BoneProperties)

    for cls in wc_classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_import.append(menu_import_mdx)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_import_mdx)
    del WarCraft3BoneProperties.bpy_type.warcraft_3
    del WarCraft3ArmatureProperties.bpy_type.warcraft_3
    for cls in reversed(wc_classes):
        bpy.utils.unregister_class(cls)
    for cls in reversed(prop_classes):
        bpy.utils.unregister_class(cls)

