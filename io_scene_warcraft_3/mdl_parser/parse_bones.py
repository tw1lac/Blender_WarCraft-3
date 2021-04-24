from ..classes.WarCraft3Bone import WarCraft3Bone
from .mdl_reader import get_between
from .parse_node import parse_node
from ..classes.WarCraft3Model import WarCraft3Model


def parse_bones(data, model: WarCraft3Model):
    bone = WarCraft3Bone()
    bone.geoset_id = 0
    geoset_id = get_between(data, "GeosetId", ",")

    if geoset_id != "Multiple":
        bone.geoset_id = int(geoset_id)

    geoset_animation_id = get_between(data, "GeosetAnimId", ",")
    bone.node = parse_node(data)

    model.nodes.append(bone)
