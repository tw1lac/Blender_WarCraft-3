from ..classes.WarCraft3Mesh import WarCraft3Mesh
from .binary_reader import Reader
from .. import constants
from .get_vertex_groups import get_vertex_groups


def parse_geometry(data):
    r = Reader(data)
    mesh = WarCraft3Mesh()
    mesh.name = 'temp'

    # parse vertices
    chunkId = r.getid(constants.CHUNK_VERTEX_POSITION)
    print(chunkId)
    vertexCount = r.getf('<I')[0]
    print(vertexCount)

    for _ in range(vertexCount):
        vertexPositionX, vertexPositionY, vertexPositionZ = r.getf('<3f')
        # print(vertexPositionX, ", ", vertexPositionY, ", ", vertexPositionZ)
        mesh.vertices.append((vertexPositionX, vertexPositionY, vertexPositionZ))

    # Read and ignore
    chunks_to_skip = [[constants.CHUNK_VERTEX_NORMAL, '<3f'], [constants.CHUNK_FACE_TYPE_GROUP, '<I'], [constants.CHUNK_FACE_GROUP, '<I']]
    for chunk in chunks_to_skip:
        chunkId = r.getid(chunk[0])
        count = r.getf('<I')[0]

        for _ in range(count):
            chunk_thing = r.getf(chunk[1])

    # parse
    chunkId = r.getid(constants.CHUNK_FACE)
    indicesCount = r.getf('<I')[0]

    if indicesCount % 3 != 0:
        raise Exception('bad indices (indicesCount % 3 != 0)')

    for _ in range(indicesCount // 3):
        vertexIndex1, vertexIndex2, vertexIndex3 = r.getf('<3H')
        mesh.triangles.append((vertexIndex1, vertexIndex2, vertexIndex3))

    # parse vertex groups
    chunkId = r.getid(constants.CHUNK_VERTEX_GROUP)
    matrixGroupsCount = r.getf('<I')[0]
    matrixGroups = []

    for _ in range(matrixGroupsCount):
        matrixGroup = r.getf('<B')[0]
        matrixGroups.append(matrixGroup)

    # parse matrix Groups
    chunkId = r.getid(constants.CHUNK_MATRIX_GROUP)
    matrixGroupsSizesCount = r.getf('<I')[0]
    matrixGroupsSizes = []

    for _ in range(matrixGroupsSizesCount):
        matrixGroupSize = r.getf('<I')[0]
        matrixGroupsSizes.append(matrixGroupSize)

    # parse MatrixIndices
    chunkId = r.getid(constants.CHUNK_MATRIX_INDEX)
    matrixIndicesCount = r.getf('<I')[0]
    matrixIndices = []

    for _ in range(matrixIndicesCount):
        matrixIndex = r.getf('<I')[0]
        matrixIndices.append(matrixIndex)

    # parse vertex groups
    vertexGroups, vertexGroupsIds = get_vertex_groups(matrixGroups, matrixGroupsSizes, matrixIndices)
    mesh.vertex_groups = vertexGroups
    mesh.vertex_groups_ids = vertexGroupsIds
    mesh.material_id = r.getf('<I')[0]
    selectionGroup = r.getf('<I')[0]
    selectionFlags = r.getf('<I')[0]

    if constants.MDX_CURRENT_VERSION > 800:
        lod = r.getf('<I')[0]
        lodName = r.gets(80)

    boundsRadius = r.getf('<f')[0]
    minimumExtent = r.getf('<3f')
    maximumExtent = r.getf('<3f')
    extentsCount = r.getf('<I')[0]

    for _ in range(extentsCount):
        boundsRadius = r.getf('<f')[0]
        minimumExtent = r.getf('<3f')
        maximumExtent = r.getf('<3f')

    if constants.MDX_CURRENT_VERSION > 800:
        chunkId = r.getid((constants.CHUNK_TANGENTS, constants.CHUNK_SKIN, constants.CHUNK_TEXTURE_VERTEX_GROUP))
        if chunkId == constants.CHUNK_TANGENTS:
            tangentSize = r.getf('<I')[0]
            r.skip(16 * tangentSize)
            chunkId = r.getid((constants.CHUNK_SKIN, constants.CHUNK_TEXTURE_VERTEX_GROUP))
        if chunkId == constants.CHUNK_SKIN:
            skinSize = r.getf('<I')[0]
            r.skip(skinSize)
            chunkId = r.getid(constants.CHUNK_TEXTURE_VERTEX_GROUP)
    else:
        chunkId = r.getid(constants.CHUNK_TEXTURE_VERTEX_GROUP)
    textureVertexGroupCount = r.getf('<I')[0]

    # parse uv-coordinates
    chunkId = r.getid(constants.CHUNK_VERTEX_TEXTURE_POSITION)
    vertexTexturePositionCount = r.getf('<I')[0]

    for _ in range(vertexTexturePositionCount):
        u, v = r.getf('<2f')
        mesh.uvs.append((u, 1 - v))

    return mesh
