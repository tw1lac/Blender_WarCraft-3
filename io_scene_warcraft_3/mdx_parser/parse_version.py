from io_scene_warcraft_3 import constants
from io_scene_warcraft_3.mdx_parser import binary


def parse_version(data):
    r = binary.Reader(data)
    version = r.getf('<I')[0]
    if version != constants.MDX_CURRENT_VERSION:
        raise Exception('unsupported MDX format version: {0}'.format(version))
