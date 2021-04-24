from ..classes.WarCraft3Node import WarCraft3Node
from .. import constants
from .parse_geoset_transformation import parse_geoset_transformation
from .parse_geoset_rotation import parse_geoset_rotation
from .parse_geoset_scaling import parse_geoset_scaling
from .parse_geoset_translation import parse_geoset_translation


def parse_node(r):
    node = WarCraft3Node()
    inclusive_size = r.offset + r.getf('<I')[0]
    node.name = r.gets(80)
    node.id = r.getf('<I')[0]
    node.parent = r.getf('<I')[0]

    if node.parent == 0xffffffff:
        node.parent = None

    flags = r.getf('<I')[0]

    # while r.offset < inclusive_size:
    #     chunk_id = r.getid(constants.SUB_CHUNKS_NODE)
    #     if chunk_id == constants.CHUNK_GEOSET_TRANSLATION:
    #         node.translations = parse_geoset_translation(r)
    #     elif chunk_id == constants.CHUNK_GEOSET_ROTATION:
    #         node.rotations = parse_geoset_rotation(r)
    #     elif chunk_id == constants.CHUNK_GEOSET_SCALING:
    #         node.scalings = parse_geoset_scaling(r)

    while r.offset < inclusive_size:
        chunk_id = r.getid(constants.SUB_CHUNKS_NODE)

        if chunk_id == constants.CHUNK_GEOSET_TRANSLATION:
            node.translations = parse_geoset_transformation(r, '<3f')
        elif chunk_id == constants.CHUNK_GEOSET_ROTATION:
            node.rotations = parse_geoset_transformation(r, '<4f')
        elif chunk_id == constants.CHUNK_GEOSET_SCALING:
            node.scalings = parse_geoset_transformation(r, '<3f')

    return node
