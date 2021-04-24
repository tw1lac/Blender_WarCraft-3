import re
from ..classes.WarCraft3Material import WarCraft3Material
from ..classes.WarCraft3Layer import WarCraft3Layer
from .parse_geoset_transformation import parse_geoset_transformation
from .mdl_reader import extract_bracket_content, chunkifier, get_between
from ..classes.WarCraft3Model import WarCraft3Model


def parse_materials(data, model: WarCraft3Model):
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
                    layer.filterMode = get_between(info, "FilterMode ", ",")
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
                            # Flip-book texture on format time: textureID,
                            #   DontInterp,
                            # 	GlobalSeqId 0
                            # 	0: 0,
                            # 	...
                            texture_chunk = re.split(",\n*\\s*(?=TextureID)", chunk)[1]
                            layer.material_texture_id = parse_geoset_transformation(texture_chunk)
                            print(layer.material_texture_id.values)
                            layer.texture_id = int(get_between(info, "TextureID ", "{"))

                    if info.find("Alpha") > -1:
                        if info.find("static Alpha") > -1:
                            layer.material_alpha = float(get_between(info, "static Alpha ", ","))
                        else:
                            alpha_chunk = re.split(",\n*\\s*(?=Alpha)", chunk)[1]
                            layer.material_alpha = parse_geoset_transformation(alpha_chunk)
                        # layer.material_alpha = float(get_between(info, "Alpha ", ","))

                    if info.find("FresnelColor") > -1:
                        if info.find("static FresnelColor") > -1:
                            layer.fresnel_color = float(get_between(info, "static FresnelColor ", ","))
                        else:
                            alpha_chunk = re.split(",\n*\\s*(?=FresnelOpacity)", chunk)[1]
                            layer.material_alpha = parse_geoset_transformation(alpha_chunk)
                        # layer.material_alpha = float(get_between(info, "Alpha ", ","))

                    if info.find("FresnelOpacity") > -1:
                        if info.find("static FresnelOpacity") > -1:
                            layer.fresnel_opacity = float(get_between(info, "static FresnelOpacity ", ","))
                        else:
                            alpha_chunk = re.split(",\n*\\s*(?=FresnelOpacity)", chunk)[1]
                            layer.material_alpha = parse_geoset_transformation(alpha_chunk)
                        # layer.material_alpha = float(get_between(info, "Alpha ", ","))

                    if info.find("FresnelTeamColor") > -1:
                        if info.find("static FresnelTeamColor") > -1:
                            layer.fresnel_team_color = float(get_between(info, "static FresnelTeamColor ", ","))
                        else:
                            alpha_chunk = re.split(",\n*\\s*(?=FresnelTeamColor)", chunk)[1]
                            layer.material_alpha = parse_geoset_transformation(alpha_chunk)
                        # layer.material_alpha = float(get_between(info, "Alpha ", ","))

            layers.append(layer)

        material.layers = layers
        model.materials.append(material)
