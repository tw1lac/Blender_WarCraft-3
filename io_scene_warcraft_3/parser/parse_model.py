from io_scene_warcraft_3 import binary


def parse_model(data, model):
    r = binary.Reader(data)
    model.name = r.gets(80)
    animationFileName = r.gets(260)
    boundsRadius = r.getf('<f')[0]
    minimumExtent = r.getf('<3f')
    maximumExtent = r.getf('<3f')
    blendTime = r.getf('<I')[0]