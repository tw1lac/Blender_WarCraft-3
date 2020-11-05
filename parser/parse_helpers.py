from .. import binary
from ..classes.WarCraft3Helper import WarCraft3Helper
from .parse_node import parse_node


def parse_helpers(data, model):
    dataSize = len(data)
    r = binary.Reader(data)
    while r.offset < dataSize:
        helper = WarCraft3Helper()
        helper.node = parse_node(r)
        model.nodes.append(helper)
