from ..classes.WarCraft3GeosetTransformation import WarCraft3GeosetTransformation
from .. import constants


def parse_material_texture_id(r):
    texture_id = WarCraft3GeosetTransformation()
    texture_id.tracks_count = r.getf('<I')[0]
    texture_id.interpolation_type = r.getf('<I')[0]
    global_sequence_id = r.getf('<I')[0]

    for _ in range(texture_id.tracks_count):
        time = r.getf('<I')[0]
        value = r.getf('<I')[0]    # texture id value
        texture_id.times.append(time)
        texture_id.values.append(value)

        if texture_id.interpolation_type > constants.INTERPOLATION_TYPE_LINEAR:
            in_tan = r.getf('<f')[0]
            out_tan = r.getf('<f')[0]
