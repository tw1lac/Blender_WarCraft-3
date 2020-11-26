from . import binary_reader


def parse_model(data, model):
    r = binary_reader.Reader(data)
    model.name = r.gets(80)
    animationFileName = r.gets(260)
    boundsRadius = r.getf('<f')[0]
    minimumExtent = r.getf('<3f')
    maximumExtent = r.getf('<3f')
    blendTime = r.getf('<I')[0]
