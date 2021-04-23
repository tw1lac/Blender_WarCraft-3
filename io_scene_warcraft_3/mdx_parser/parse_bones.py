from ..classes.WarCraft3Bone import WarCraft3Bone
from . import binary_reader
from .parse_node import parse_node
from ..classes.WarCraft3Model import WarCraft3Model


def parse_bones(data, model: WarCraft3Model):
    r = binary_reader.Reader(data)
    data_size = len(data)

    while r.offset < data_size:
        bone = WarCraft3Bone()
        bone.node = parse_node(r)
        bone.geoset_id = r.getf('<I')[0]
        geoset_animation_id = r.getf('<I')[0]
        model.nodes.append(bone)
