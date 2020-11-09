from ..classes.WarCraft3Texture import WarCraft3Texture
from .mdl_reader import extract_bracket_content, chunkifier


def parse_textures(data, model):
    textures_string = extract_bracket_content(data)
    texture_chunks = chunkifier(textures_string)

    for texture_chunk in texture_chunks:
        label = texture_chunk.strip().split(" ")[0]
        if label == "Bitmap":
            texture = WarCraft3Texture()
            texture_info = extract_bracket_content(texture_chunk)
            label = texture_info.strip().split(" ")[0]

            if label == "Image":
                texture.image_file_name = texture_info.strip().split("\"")[1]

            if label == "ReplaceableId":
                texture.replaceable_id = int(texture_info.strip().replace(",", "").split(" ")[1])

            model.textures.append(texture)
