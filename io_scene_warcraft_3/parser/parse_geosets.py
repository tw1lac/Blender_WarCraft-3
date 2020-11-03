from io_scene_warcraft_3 import binary
from io_scene_warcraft_3.parser.parse_geometry import parse_geometry


def parse_geosets(data, model):
    dataSize = len(data)
    r = binary.Reader(data)
    while r.offset < dataSize:
        inclusiveSize = r.getf('<I')[0]
        geoDataSize = inclusiveSize - 4
        geoData = data[r.offset : r.offset + geoDataSize]
        r.skip(geoDataSize)
        mesh = parse_geometry(geoData)
        model.meshes.append(mesh)
