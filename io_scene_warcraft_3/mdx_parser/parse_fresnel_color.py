from ..classes.WarCraft3GeosetTransformation import WarCraft3GeosetTransformation
from .. import constants


def parse_fresnel_color(r):
    fresnel_color = WarCraft3GeosetTransformation()
    fresnel_color.tracks_count = r.getf('<I')[0]
    fresnel_color.interpolation_type = r.getf('<I')[0]
    global_sequence_id = r.getf('<I')[0]

    for _ in range(fresnel_color.tracks_count):
        time = r.getf('<I')[0]
        value = [r.getf('<f')[0], r.getf('<f')[0], r.getf('<f')[0]]
        fresnel_color.times.append(time)
        fresnel_color.values.append(value)

        if fresnel_color.interpolation_type > constants.INTERPOLATION_TYPE_LINEAR:
            in_tan = [r.getf('<f')[0], r.getf('<f')[0], r.getf('<f')[0]]
            out_tan = [r.getf('<f')[0], r.getf('<f')[0], r.getf('<f')[0]]

    return fresnel_color
