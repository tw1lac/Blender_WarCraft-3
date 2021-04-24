from . import binary_reader
from .. import constants


def parse_version(data):
    r = binary_reader.Reader(data)
    version = r.getf('<I')[0]
    if version != constants.MDX_CURRENT_VERSION:
        raise Exception('unsupported MDX format version: {0}'.format(version))
