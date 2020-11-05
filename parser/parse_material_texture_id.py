from .. import constants
from ..classes.WarCraft3GeosetTransformation import WarCraft3GeosetTransformation


def parse_material_texture_id(r):
    textureId = WarCraft3GeosetTransformation()
    textureId.tracks_count = r.getf('<I')[0]
    textureId.interpolation_type = r.getf('<I')[0]
    globalSequenceId = r.getf('<I')[0]
    for _ in range(textureId.tracks_count):
        time = r.getf('<I')[0]
        value = r.getf('<f')[0]    # texture id value
        textureId.times.append(time)
        textureId.values.append(value)
        if textureId.interpolation_type > constants.INTERPOLATION_TYPE_LINEAR:
            inTan = r.getf('<f')[0]
            outTan = r.getf('<f')[0]
