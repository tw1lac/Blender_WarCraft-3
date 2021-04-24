from ..classes.WarCraft3Helper import WarCraft3Helper
from .parse_node import parse_node
from ..classes.WarCraft3Model import WarCraft3Model


def parse_helpers(data, model):
    helper = WarCraft3Helper()
    helper.node = parse_node(data)

    model.nodes.append(helper)
