from ..classes.WarCraft3Helper import WarCraft3Helper
from . import binary_reader
from .parse_node import parse_node
from ..classes.WarCraft3Model import WarCraft3Model


def parse_helpers(data, model):
    data_size = len(data)
    r = binary_reader.Reader(data)

    while r.offset < data_size:
        helper = WarCraft3Helper()
        helper.node = parse_node(r)
        model.nodes.append(helper)
