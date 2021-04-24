
bl_info = {
    'name': 'WarCraft 3',
    'author': 'Pavel_Blend, twilac',
    'version': (0, 0, 0),
    'blender': (2, 7, 8),
    'category': 'Import-Export',
    'location': 'File > Import',
    'description': 'Import *.mdx files (3d models of WarCraft 3)',
    'wiki_url': 'https://github.com/PavelBlend/Blender_WarCraft-3',
    'tracker_url': 'https://github.com/PavelBlend/Blender_WarCraft-3/issues'
    }


if "register" not in locals():
    print("init first load")
    from .plugin import register, unregister
else:
    print("init reload")
    import importlib
    from . import plugin
    importlib.reload(plugin)

