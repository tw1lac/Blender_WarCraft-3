
bl_info = {
    'name': 'Warcraft 3 (*.mdl/*.mdx)',
    'author': 'Pavel_Blend & twilac',
    'version': (0, 0, 0),
    'blender': (2, 80, 0),
    'category': 'Import-Export',
    'location': 'File > Import',
    'description': 'Import *.mdl/*.mdx files (3d models of WarCraft 3)',
    'doc_url': 'https://github.com/tw1lac/Blender_WarCraft-3',
    'tracker_url': 'https://github.com/tw1lac/Blender_WarCraft-3/issues'
    }


# On init-reload, if plugin.register was imported before, this reloads plugin.py
# PyCharm warning about plugin not being an module should be ignored, see: https://youtrack.jetbrains.com/issue/PY-36062
if "register" not in locals():
    print("init first load")
    from .plugin import register, unregister
else:
    print("init reload")
    import importlib
    from . import plugin
    importlib.reload(plugin)