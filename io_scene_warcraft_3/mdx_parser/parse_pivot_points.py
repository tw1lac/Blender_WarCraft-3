from . import binary_reader
from ..classes.WarCraft3Model import WarCraft3Model


def parse_pivot_points(data, model: WarCraft3Model):
    data_size = len(data)
    r = binary_reader.Reader(data)

    if data_size % 12 != 0:
        raise Exception('bad Pivot Point data (size % 12 != 0)')

    pivot_points_count = data_size // 12

    for _ in range(pivot_points_count):
        model.pivot_points.append(r.getf('<3f'))
