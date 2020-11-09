from io_scene_warcraft_3.classes.WarCraft3GeosetTransformation import WarCraft3GeosetTransformation
from io_scene_warcraft_3 import constants


def parse_geoset_alpha(r):
    alpha = WarCraft3GeosetTransformation()
    alpha.tracks_count = r.getf('<I')[0]
    alpha.interpolation_type = r.getf('<I')[0]
    globalSequenceId = r.getf('<I')[0]
    for _ in range(alpha.tracks_count):
        time = r.getf('<I')[0]
        value = r.getf('<f')[0]    # alpha value
        alpha.times.append(time)
        alpha.values.append(value)
        if alpha.interpolation_type > constants.INTERPOLATION_TYPE_LINEAR:
            inTan = r.getf('<f')[0]
            outTan = r.getf('<f')[0]
    return alpha
