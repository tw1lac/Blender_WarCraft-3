from io_scene_warcraft_3.classes.WarCraft3Node import WarCraft3Node
from io_scene_warcraft_3 import constants
from io_scene_warcraft_3.mdx_parser.parse_geoset_transformation import parse_geoset_transformation
from io_scene_warcraft_3.mdx_parser.parse_geoset_rotation import parse_geoset_rotation
from io_scene_warcraft_3.mdx_parser.parse_geoset_scaling import parse_geoset_scaling
from io_scene_warcraft_3.mdx_parser.parse_geoset_translation import parse_geoset_translation


def parse_node(r):
    node = WarCraft3Node()
    inclusiveSize = r.offset + r.getf('<I')[0]
    node.name = r.gets(80)
    node.id = r.getf('<I')[0]
    node.parent = r.getf('<I')[0]
    if node.parent == 0xffffffff:
        node.parent = None
    flags = r.getf('<I')[0]

    # while r.offset < inclusiveSize:
    #     chunkId = r.getid(constants.SUB_CHUNKS_NODE)
    #     if chunkId == constants.CHUNK_GEOSET_TRANSLATION:
    #         node.translations = parse_geoset_translation(r)
    #     elif chunkId == constants.CHUNK_GEOSET_ROTATION:
    #         node.rotations = parse_geoset_rotation(r)
    #     elif chunkId == constants.CHUNK_GEOSET_SCALING:
    #         node.scalings = parse_geoset_scaling(r)

    while r.offset < inclusiveSize:
        chunkId = r.getid(constants.SUB_CHUNKS_NODE)
        if chunkId == constants.CHUNK_GEOSET_TRANSLATION:
            node.translations = parse_geoset_transformation(r, '<3f')
        elif chunkId == constants.CHUNK_GEOSET_ROTATION:
            node.rotations = parse_geoset_transformation(r, '<4f')
        elif chunkId == constants.CHUNK_GEOSET_SCALING:
            node.scalings = parse_geoset_transformation(r, '<3f')

    return node
