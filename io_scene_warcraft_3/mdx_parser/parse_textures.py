from ..classes.WarCraft3Model import WarCraft3Model
from ..classes.WarCraft3Texture import WarCraft3Texture
from . import binary_reader


def parse_textures(data, model):
    r = binary_reader.Reader(data)
    data_size = len(data)

    if data_size % 268 != 0:
        raise Exception('bad Texture data (size % 268 != 0)')

    textures_count = data_size // 268

    for _ in range(textures_count):
        texture = WarCraft3Texture()
        texture.replaceable_id = r.getf('<I')[0]
        texture.image_file_name = r.gets(260)
        flags = r.getf('<I')[0]
        model.textures.append(texture)
