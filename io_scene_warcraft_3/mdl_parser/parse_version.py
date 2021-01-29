from .mdl_reader import extract_bracket_content
from .. import constants


def parse_version(data):
    version_data_internal = extract_bracket_content(data)
    version = version_data_internal.replace(",", "").split(" ")[1].strip()
    print("mdl version: ", version)
    if int(version) != constants.MDX_CURRENT_VERSION:
        raise Exception('unsupported MDX format version: {0}'.format(version))
