from ..classes.WarCraft3GeosetAnimation import WarCraft3GeosetAnimation
from .mdl_reader import extract_bracket_content
from .mdl_reader import get_between


def parse_geoset_animations(data, model):
    geosetAnimation = WarCraft3GeosetAnimation()
    geosetAnimation.geoset_id = 0
    geoset_id = get_between(data, "GeosetId", ",")

    if geoset_id != "Multiple":
        geosetAnimation.geoset_id = int(geoset_id)


    animation_data = extract_bracket_content(data)
    animation_info = extract_bracket_content(data).split(",\n")

    for info in animation_info:
        label = info.strip().split(" ")[0]

        if label == "Interval":
            interval = extract_bracket_content(info).strip().split(",")
            geosetAnimation.interval_start = int(interval[0].strip())
            geosetAnimation.interval_end = int(interval[1].strip())

        if label == "MoveSpeed":
            moveSpeed = float(info.strip().replace(",", "").split(" ")[1])

        if label == "NonLooping":
            flags = "NonLooping"

        if label == "MinimumExtent":
            extent = extract_bracket_content(info).strip().split(",")
            minimumExtent = (float(extent[0]), float(extent[1]), float(extent[2]))

        if label == "MaximumExtent":
            extent = extract_bracket_content(info).strip().split(",")
            maximumExtent = (float(extent[0]), float(extent[1]), float(extent[2]))

        if label == "BoundsRadius":
            boundsRadius = float(info.strip().replace(",", "").split(" ")[1])
