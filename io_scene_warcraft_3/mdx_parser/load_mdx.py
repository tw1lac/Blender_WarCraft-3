from .parse_mdx import parse_mdx
from ..classes.MDXImportProperties import MDXImportProperties


def load_mdx(import_properties: MDXImportProperties):
    mdx_file = open(import_properties.mdx_file_path, 'rb')
    mdx_file_data = mdx_file.read()
    mdx_file.close()
    parse_mdx(mdx_file_data, import_properties)
    print("Done!")
