from .parse_mdx import parse_mdx


def load_mdx(importProperties):
    mdxFile = open(importProperties.mdx_file_path, 'rb')
    mdxFileData = mdxFile.read()
    mdxFile.close()
    parse_mdx(mdxFileData, importProperties)
