import io_scene_warcraft_3.classes
from io_scene_warcraft_3 import binary
from io_scene_warcraft_3.parser.parse_node import parse_node


def parse_helpers(data, model):
    dataSize = len(data)
    r = binary.Reader(data)
    while r.offset < dataSize:
        helper = io_scene_warcraft_3.classes.WarCraft3Helper.WarCraft3Helper()
        helper.node = parse_node(r)
        model.nodes.append(helper)