from .. import constants
from io_scene_warcraft_3.classes.WarCraft3GeosetTransformation import WarCraft3GeosetTransformation


def parse_geoset_rotation(r):
    rotation = WarCraft3GeosetTransformation()
    rotation.tracks_count = r.getf('<I')[0]
    rotation.interpolation_type = r.getf('<I')[0]
    global_sequence_id = r.getf('<I')[0]
    for _ in range(rotation.tracks_count):
        time = r.getf('<I')[0]
        rot_x, rot_y, rot_z, rot_w = r.getf('<4f')
        if rotation.interpolation_type > constants.INTERPOLATION_TYPE_LINEAR:
            in_tan = r.getf('<4f')
            out_tan = r.getf('<4f')
        values = (rot_w, rot_x, rot_y, rot_z)    # rotation values
        rotation.times.append(time)
        rotation.values.append(values)
    return rotation
