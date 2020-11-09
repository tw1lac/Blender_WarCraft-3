from io_scene_warcraft_3.classes.WarCraft3Event import WarCraft3Event
from io_scene_warcraft_3 import constants
from io_scene_warcraft_3.mdx_parser import binary_reader
from io_scene_warcraft_3.mdx_parser.parse_node import parse_node
from io_scene_warcraft_3.mdx_parser.parse_tracks import parse_tracks


def parse_events(data, model):
    dataSize = len(data)
    r = binary_reader.Reader(data)
    while r.offset < dataSize:
        event = WarCraft3Event()
        event.node = parse_node(r)
        if r.offset < dataSize:
            chunkId = r.gets(4)
            if chunkId == constants.CHUNK_TRACKS:
                parse_tracks(r)
            else:
                r.offset -= 4
        model.nodes.append(event)
