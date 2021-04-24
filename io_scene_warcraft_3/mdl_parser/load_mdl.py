from .parse_mdl import parse_mdl, parse_mdl2
from ..classes.MDXImportProperties import MDXImportProperties


def load_mdl(import_properties: MDXImportProperties):
    mdx_file = open(import_properties.mdx_file_path, 'r')
    mdx_file_data = mdx_file.read()
    mdx_file.close()
    parse_mdl(mdx_file_data, import_properties)
    print("Done!")


# this is for commandline testing
def load_mdl2():
    mdx_file = open('FILEPATH', 'r')
    mdx_file_data = mdx_file.read()
    mdx_file.close()
    parse_mdl2(mdx_file_data)
