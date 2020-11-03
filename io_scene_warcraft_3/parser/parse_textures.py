import io_scene_warcraft_3.classes
from io_scene_warcraft_3 import binary


def parse_textures(data, model):
    r = binary.Reader(data)
    dataSize = len(data)
    if dataSize % 268 != 0:
        raise Exception('bad Texture data (size % 268 != 0)')
    texturesCount = dataSize // 268
    for _ in range(texturesCount):
        texture = io_scene_warcraft_3.classes.WarCraft3Texture.WarCraft3Texture()
        texture.replaceable_id = r.getf('<I')[0]
        texture.image_file_name = r.gets(260)
        flags = r.getf('<I')[0]
        model.textures.append(texture)