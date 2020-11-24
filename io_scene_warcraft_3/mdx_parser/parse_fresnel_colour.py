from io_scene_warcraft_3.classes.WarCraft3GeosetTransformation import WarCraft3GeosetTransformation
from io_scene_warcraft_3 import constants


def parse_fresnel_colour(r):
    fresnel_colour = WarCraft3GeosetTransformation()
    fresnel_colour.tracks_count = r.getf('<I')[0]
    fresnel_colour.interpolation_type = r.getf('<I')[0]
    globalSequenceId = r.getf('<I')[0]
    for _ in range(fresnel_colour.tracks_count):
        time = r.getf('<I')[0]
        value = [r.getf('<f')[0], r.getf('<f')[0], r.getf('<f')[0]]
        fresnel_colour.times.append(time)
        fresnel_colour.values.append(value)
        if fresnel_colour.interpolation_type > constants.INTERPOLATION_TYPE_LINEAR:
            inTan = [r.getf('<f')[0], r.getf('<f')[0], r.getf('<f')[0]]
            outTan = [r.getf('<f')[0], r.getf('<f')[0], r.getf('<f')[0]]
    return fresnel_colour
