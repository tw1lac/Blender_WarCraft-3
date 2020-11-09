from .parse_mdl import parse_mdl, parse_mdl2


def load_mdl(importProperties):
    mdxFile = open(importProperties.mdx_file_path, 'r')
    mdxFileData = mdxFile.read()
    mdxFile.close()
    parse_mdl(mdxFileData, importProperties)


# this is for commandline testing
def load_mdl2():
    mdxFile = open('FILEPATH', 'r')
    mdxFileData = mdxFile.read()
    mdxFile.close()
    parse_mdl2(mdxFileData)
