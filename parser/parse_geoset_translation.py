from .. import constants
from ..classes.WarCraft3GeosetTransformation import WarCraft3GeosetTransformation


def parse_geoset_translation(r):
    translation = WarCraft3GeosetTransformation()
    translation.tracks_count = r.getf('<I')[0]
    translation.interpolation_type = r.getf('<I')[0]
    globalSequenceId = r.getf('<I')[0]
    for _ in range(translation.tracks_count):
        time = r.getf('<I')[0]
        values = r.getf('<3f')    # translation values
        translation.times.append(time)
        translation.values.append(values)
        if translation.interpolation_type > constants.INTERPOLATION_TYPE_LINEAR:
            inTan = r.getf('<3f')
            outTan = r.getf('<3f')
    return translation
