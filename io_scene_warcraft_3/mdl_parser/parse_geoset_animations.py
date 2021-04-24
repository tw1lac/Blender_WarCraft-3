import re

from .. import constants
from ..classes.WarCraft3GeosetAnimation import WarCraft3GeosetAnimation
from .parse_geoset_transformation import parse_geoset_transformation
from .mdl_reader import extract_bracket_content, chunkifier, get_between, extract_float_values
from ..classes.WarCraft3GeosetTransformation import WarCraft3GeosetTransformation
from ..classes.WarCraft3Model import WarCraft3Model


def parse_geoset_animations(data, model):
    geoset_animation = WarCraft3GeosetAnimation()
    geoset_animation.geoset_id = 0
    geoset_id = get_between(data, "GeosetId", ",")

    if geoset_id != "Multiple":
        geoset_animation.geoset_id = int(geoset_id)

    animation_data = extract_bracket_content(data)
    animation_info = extract_bracket_content(data).split(",\n")

    for info in animation_info:
        label = info.strip().split(" ")[0]

        if info.find("TextureID") > -1:
            if info.find("static TextureID") > -1:
                geoset_animation.texture_id = int(get_between(info, "static TextureID ", ","))
            else:
                texture_chunk = re.split("\\s*(?=TextureID)", animation_data, 1)[1]
                geoset_animation.material_texture_id = parse_geoset_transformation(texture_chunk)
            # layer.texture_id = int(get_between(info, "TextureID ", ","))
            # layer.material_texture_id = layer.texture_id

        if info.find("Alpha") > -1:
            if info.find("static Alpha") > -1:
                geoset_animation.animation_alpha = make_fake_animation(float(get_between(info, "static Alpha ", ",")))
            else:
                # print(animation_data)
                split = re.split("\\s*(?=Alpha)", animation_data, 1)
                # print("animation_data:", split)
                alpha_chunk = split[len(split)-1]
                geoset_animation.animation_alpha = parse_geoset_transformation(alpha_chunk)
            # layer.material_alpha = float(get_between(info, "Alpha ", ","))

        if info.find("Color") > -1:
            if info.find("static Color") > -1:
                geoset_animation.animation_color = make_fake_animation(extract_float_values(get_between(info, "static Color ", "END")))
            else:
                color_chunk = re.split("\\s*(?=Color)", animation_data, 1)[1]
                geoset_animation.animation_color = parse_geoset_transformation(color_chunk)
            # layer.material_alpha = float(get_between(info, "Alpha ", ","))

        if label == "Interval":
            interval = extract_bracket_content(info).strip().split(",")
            geoset_animation.interval_start = int(interval[0].strip())
            geoset_animation.interval_end = int(interval[1].strip())

        if label == "MoveSpeed":
            move_speed = float(info.strip().replace(",", "").split(" ")[1])

        if label == "NonLooping":
            flags = "NonLooping"

        if label == "MinimumExtent":
            extent = extract_bracket_content(info).strip().split(",")
            minimum_extent = (float(extent[0]), float(extent[1]), float(extent[2]))

        if label == "MaximumExtent":
            extent = extract_bracket_content(info).strip().split(",")
            maximum_extent = (float(extent[0]), float(extent[1]), float(extent[2]))

        if label == "BoundsRadius":
            bounds_radius = float(info.strip().replace(",", "").split(" ")[1])

        if not geoset_animation.animation_color:
            geoset_animation.animation_color = make_fake_animation([0, 0, 0])
        if not geoset_animation.animation_alpha:
            geoset_animation.animation_alpha = make_fake_animation(1)

    model.geoset_animations.append(geoset_animation)


def make_fake_animation(values):
    fake_transform = WarCraft3GeosetTransformation()
    fake_transform.tracks_count = 1
    fake_transform.interpolation_type = constants.INTERPOLATION_TYPE_NONE
    fake_transform.times = [0, ]
    fake_transform.values = [values]
    return fake_transform
