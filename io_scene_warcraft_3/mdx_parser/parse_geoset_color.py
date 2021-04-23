from ..classes.WarCraft3GeosetTransformation import WarCraft3GeosetTransformation
from .. import constants


def parse_geoset_color(r):
    color = WarCraft3GeosetTransformation()
    color.tracks_count = r.getf('<I')[0]
    color.interpolation_type = r.getf('<I')[0]
    global_sequence_id = r.getf('<I')[0]

    for _ in range(color.tracks_count):
        time = r.getf('<I')[0]
        value = r.getf('<3f')    # color value
        color.times.append(time)
        color.values.append(value)

        if color.interpolation_type > constants.INTERPOLATION_TYPE_LINEAR:
            in_tan = r.getf('<3f')
            out_tan = r.getf('<3f')

    return color
