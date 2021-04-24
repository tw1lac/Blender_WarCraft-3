from .mdl_reader import extract_bracket_content
from .. import constants
from ..classes.WarCraft3Model import WarCraft3Model


def parse_version(data, model):
    version_data_internal = extract_bracket_content(data)
    version = version_data_internal.replace(",", "").split(" ")[1].strip()
    print("mdl version: ", version)
    if int(version) in constants.MDX_VERSIONS:
        model.version = version
        constants.MDX_CURRENT_VERSION = version
    else:
        print("Version %s is not supported; the model will load as %s which might cause issues"
              % (version, model.version))
        # raise Exception('unsupported MDX format version: {0}'.format(version))
