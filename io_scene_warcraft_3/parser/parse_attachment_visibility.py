import io_scene_warcraft_3.classes
from io_scene_warcraft_3 import constants


def parse_attachment_visibility(r):
    chunkId = r.getid(constants.CHUNK_ATTACHMENT_VISIBILITY)
    visibility = io_scene_warcraft_3.classes.WarCraft3GeosetTransformation.WarCraft3GeosetTransformation()
    visibility.tracks_count = r.getf('<I')[0]
    visibility.interpolation_type = r.getf('<I')[0]
    globalSequenceId = r.getf('<I')[0]
    for _ in range(visibility.tracks_count):
        time = r.getf('<I')[0]
        value = r.getf('<f')[0]    # visibility value
        visibility.times.append(time)
        visibility.values.append(value)
        if visibility.interpolation_type > constants.INTERPOLATION_TYPE_LINEAR:
            inTan = r.getf('<f')[0]
            outTan = r.getf('<f')[0]