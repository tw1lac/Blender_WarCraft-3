from . import binary_reader
from io_scene_warcraft_3.classes.WarCraft3Bone import WarCraft3Bone
from .parse_node import parse_node


def parse_bones(data, model):
    r = binary_reader.Reader(data)
    data_size = len(data)
    while r.offset < data_size:
        bone = WarCraft3Bone()
        bone.node = parse_node(r)
        bone.geoset_id = r.getf('<I')[0]
        geoset_animation_id = r.getf('<I')[0]
        model.nodes.append(bone)
