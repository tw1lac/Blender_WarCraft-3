from io_scene_warcraft_3.classes.WarCraft3Helper import WarCraft3Helper
from io_scene_warcraft_3.mdx_parser import binary_reader
from io_scene_warcraft_3.mdx_parser.parse_node import parse_node


def parse_helpers(data, model):
    dataSize = len(data)
    r = binary_reader.Reader(data)
    while r.offset < dataSize:
        helper = WarCraft3Helper()
        helper.node = parse_node(r)
        model.nodes.append(helper)
