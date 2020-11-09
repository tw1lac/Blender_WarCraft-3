from ..classes.WarCraft3Event import WarCraft3Event
from .parse_node import parse_node


def parse_events(data, model):
    event = WarCraft3Event()
    event.node = parse_node(data)
    model.nodes.append(event)
