from ..classes.WarCraft3Event import WarCraft3Event
from .parse_node import parse_node
from ..classes.WarCraft3Model import WarCraft3Model


def parse_events(data, model):
    event = WarCraft3Event()
    event.node = parse_node(data)
    model.nodes.append(event)
