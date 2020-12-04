import re
from ..classes.WarCraft3Material import WarCraft3Material
from ..classes.WarCraft3Layer import WarCraft3Layer
from .parse_geoset_transformation import parse_geoset_transformation
from .mdl_reader import extract_bracket_content, chunkifier, get_between


def parse_materials(data, model):
    # print("parse_materials")
    materials_string = extract_bracket_content(data)
    material_chunks = chunkifier(materials_string)

    for material_chunk in material_chunks:
        material = WarCraft3Material()
        material_info = extract_bracket_content(material_chunk)
        layer_chunks = chunkifier(material_info)
        layers = []

        for chunk in layer_chunks:
            layer = WarCraft3Layer()
            layer_info = extract_bracket_content(chunk).split(",")

            for info in layer_info:
                label = info.strip().split(" ")[0]

                if label == "FilterMode":
                    material.image_file_name = info.strip().replace("\"", "").split(" ")[1]

                # if label == "Unshaded":
                #     print(info)
                #     material.replaceable_id = info.strip().replace(",", "").split(" ")[1]
                #     print(material.replaceable_id)
                else:
                    if info.find("TextureID") > -1:
                        if info.find("static TextureID") > -1:
                            layer.texture_id = int(get_between(info, "static TextureID ", ","))
                        else:
                            texture_chunk = re.split(",\n*\s*(?=TextureID)", chunk)[1]
                            layer.material_texture_id = parse_geoset_transformation(texture_chunk)
                            layer.texture_id = int(get_between(info, "TextureID ", "{"))
                        # layer.texture_id = int(get_between(info, "TextureID ", ","))
                        # layer.material_texture_id = layer.texture_id

                    if info.find("Alpha") > -1:
                        if info.find("static Alpha") > -1:
                            layer.material_alpha = float(get_between(info, "static Alpha ", ","))
                        else:
                            alpha_chunk = re.split(",\n*\s*(?=Alpha)", chunk)[1]
                            layer.material_alpha = parse_geoset_transformation(alpha_chunk)
                        # layer.material_alpha = float(get_between(info, "Alpha ", ","))

            layers.append(layer)

        material.layers = layers
        model.materials.append(material)
