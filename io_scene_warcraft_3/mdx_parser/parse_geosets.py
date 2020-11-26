from . import binary_reader
from .parse_geometry import parse_geometry


def parse_geosets(data, model):
    dataSize = len(data)
    r = binary_reader.Reader(data)

    while r.offset < dataSize:
        inclusiveSize = r.getf('<I')[0]
        geoDataSize = inclusiveSize - 4
        geoData = data[r.offset : r.offset + geoDataSize]
        r.skip(geoDataSize)
        mesh = parse_geometry(geoData)
        model.meshes.append(mesh)
