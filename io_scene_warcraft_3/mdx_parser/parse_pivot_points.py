from io_scene_warcraft_3 import binary


def parse_pivot_points(data, model):
    dataSize = len(data)
    r = binary.Reader(data)
    if dataSize % 12 != 0:
        raise Exception('bad Pivot Point data (size % 12 != 0)')
    pivotPointsCount = dataSize // 12
    for _ in range(pivotPointsCount):
        model.pivot_points.append(r.getf('<3f'))
