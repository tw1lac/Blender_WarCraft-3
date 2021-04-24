from .. import constants
from io_scene_warcraft_3.classes.WarCraft3GeosetTransformation import WarCraft3GeosetTransformation


def parse_geoset_scaling(r):
    scaling = WarCraft3GeosetTransformation()
    scaling.tracks_count = r.getf('<I')[0]
    scaling.interpolation_type = r.getf('<I')[0]
    global_sequence_id = r.getf('<I')[0]
    for _ in range(scaling.tracks_count):
        time = r.getf('<I')[0]
        values = r.getf('<3f')    # scaling values
        scaling.times.append(time)
        scaling.values.append(values)
        if scaling.interpolation_type > constants.INTERPOLATION_TYPE_LINEAR:
            in_tan = r.getf('<3f')
            out_tan = r.getf('<3f')
    return scaling
