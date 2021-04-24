from . import binary_reader
from ..classes.WarCraft3Model import WarCraft3Model


def parse_model(data, model):
    r = binary_reader.Reader(data)
    model.name = r.gets(80)
    animation_file_name = r.gets(260)
    bounds_radius = r.getf('<f')[0]
    minimum_extent = r.getf('<3f')
    maximum_extent = r.getf('<3f')
    blend_time = r.getf('<I')[0]
