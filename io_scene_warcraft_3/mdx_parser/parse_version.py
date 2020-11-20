from io_scene_warcraft_3 import constants
from io_scene_warcraft_3.mdx_parser import binary_reader


def parse_version(data):
    r = binary_reader.Reader(data)
    version = r.getf('<I')[0]
    if version in constants.MDX_VERSIONS:
        constants.MDX_CURRENT_VERSION = version
    else:
        raise Exception('unsupported MDX format version: {0}'.format(version))
