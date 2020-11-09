from .. import constants


def parse_version(data):
    version = data.replace(",", "").split(" ")[1]
    print("mdl version: ", version)
    if version != constants.MDX_CURRENT_VERSION:
        raise Exception('unsupported MDX format version: {0}'.format(version))
