from . import binary_reader
from .. import constants
from io_scene_warcraft_3.classes.WarCraft3Event import WarCraft3Event
from .parse_node import parse_node
from .parse_tracks import parse_tracks


def parse_events(data, model):
    data_size = len(data)
    r = binary_reader.Reader(data)
    while r.offset < data_size:
        event = WarCraft3Event()
        event.node = parse_node(r)
        if r.offset < data_size:
            chunk_id = r.gets(4)
            if chunk_id == constants.CHUNK_TRACKS:
                parse_tracks(r)
            else:
                r.offset -= 4
        model.nodes.append(event)
