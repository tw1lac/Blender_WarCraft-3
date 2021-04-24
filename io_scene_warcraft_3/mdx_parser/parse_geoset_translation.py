from .. import constants
from io_scene_warcraft_3.classes.WarCraft3GeosetTransformation import WarCraft3GeosetTransformation


def parse_geoset_translation(r):
    translation = WarCraft3GeosetTransformation()
    translation.tracks_count = r.getf('<I')[0]
    translation.interpolation_type = r.getf('<I')[0]
    global_sequence_id = r.getf('<I')[0]
    for _ in range(translation.tracks_count):
        time = r.getf('<I')[0]
        values = r.getf('<3f')    # translation values
        translation.times.append(time)
        translation.values.append(values)
        if translation.interpolation_type > constants.INTERPOLATION_TYPE_LINEAR:
            in_tan = r.getf('<3f')
            out_tan = r.getf('<3f')
    return translation
