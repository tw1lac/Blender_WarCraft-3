from io_scene_warcraft_3.classes.WarCraft3Bone import WarCraft3Bone
from io_scene_warcraft_3.mdx_parser import binary
from io_scene_warcraft_3.mdx_parser.parse_node import parse_node


def parse_bones(data, model):
    r = binary.Reader(data)
    dataSize = len(data)
    while r.offset < dataSize:
        bone = WarCraft3Bone()
        bone.node = parse_node(r)
        bone.geoset_id = r.getf('<I')[0]
        geosetAnimationId = r.getf('<I')[0]
        model.nodes.append(bone)
