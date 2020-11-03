from io_scene_warcraft_3.classes.WarCraft3Mesh import WarCraft3Mesh
from io_scene_warcraft_3 import binary, constants
from io_scene_warcraft_3.parser.get_vertex_groups import get_vertex_groups


def parse_geometry(data):
    r = binary.Reader(data)
    mesh = WarCraft3Mesh()
    mesh.name = 'temp'
    ############################################################################
    chunkId = r.getid(constants.CHUNK_VERTEX_POSITION)
    vertexCount = r.getf('<I')[0]
    for _ in range(vertexCount):
        vertexPositionX, vertexPositionY, vertexPositionZ = r.getf('<3f')
        mesh.vertices.append((vertexPositionX, vertexPositionY, vertexPositionZ))
    ############################################################################
    ################################# NOT USED #################################
    ############################################################################
    chunkId = r.getid(constants.CHUNK_VERTEX_NORMAL)
    normalsCount = r.getf('<I')[0]
    for _ in range(normalsCount):
        normal = r.getf('<3f')
    ############################################################################
    ################################# NOT USED #################################
    ############################################################################
    chunkId = r.getid(constants.CHUNK_FACE_TYPE_GROUP)
    faceTypeGroupsCount = r.getf('<I')[0]
    for _ in range(faceTypeGroupsCount):
        faceType = r.getf('<I')[0]
    ############################################################################
    ################################# NOT USED #################################
    ############################################################################
    chunkId = r.getid(constants.CHUNK_FACE_GROUP)
    faceGroupCount = r.getf('<I')[0]
    for _ in range(faceGroupCount):
        indexesCount = r.getf('<I')[0]
    ############################################################################
    chunkId = r.getid(constants.CHUNK_FACE)
    indicesCount = r.getf('<I')[0]
    if indicesCount % 3 != 0:
        raise Exception('bad indices (indicesCount % 3 != 0)')
    for _ in range(indicesCount // 3):
        vertexIndex1, vertexIndex2, vertexIndex3 = r.getf('<3H')
        mesh.triangles.append((vertexIndex1, vertexIndex2, vertexIndex3))
    ############################################################################
    chunkId = r.getid(constants.CHUNK_VERTEX_GROUP)
    matrixGroupsCount = r.getf('<I')[0]
    matrixGroups = []
    for _ in range(matrixGroupsCount):
        matrixGroup = r.getf('<B')[0]
        matrixGroups.append(matrixGroup)
    ############################################################################
    chunkId = r.getid(constants.CHUNK_MATRIX_GROUP)
    matrixGroupsSizesCount = r.getf('<I')[0]
    matrixGroupsSizes = []
    for _ in range(matrixGroupsSizesCount):
        matrixGroupSize = r.getf('<I')[0]
        matrixGroupsSizes.append(matrixGroupSize)
    ############################################################################
    chunkId = r.getid(constants.CHUNK_MATRIX_INDEX)
    matrixIndicesCount = r.getf('<I')[0]
    matrixIndices = []
    for _ in range(matrixIndicesCount):
        matrixIndex = r.getf('<I')[0]
        matrixIndices.append(matrixIndex)
    ############################################################################
    vertexGroups, vertexGroupsIds = get_vertex_groups(matrixGroups, matrixGroupsSizes, matrixIndices)
    mesh.vertex_groups = vertexGroups
    mesh.vertex_groups_ids = vertexGroupsIds
    mesh.material_id = r.getf('<I')[0]
    selectionGroup = r.getf('<I')[0]
    selectionFlags = r.getf('<I')[0]
    boundsRadius = r.getf('<f')[0]
    minimumExtent = r.getf('<3f')
    maximumExtent = r.getf('<3f')
    extentsCount = r.getf('<I')[0]
    for _ in range(extentsCount):
        boundsRadius = r.getf('<f')[0]
        minimumExtent = r.getf('<3f')
        maximumExtent = r.getf('<3f')
    ############################################################################
    ################################# NOT USED #################################
    ############################################################################
    chunkId = r.getid(constants.CHUNK_TEXTURE_VERTEX_GROUP)
    textureVertexGroupCount = r.getf('<I')[0]
    ############################################################################
    chunkId = r.getid(constants.CHUNK_VERTEX_TEXTURE_POSITION)
    vertexTexturePositionCount = r.getf('<I')[0]
    for _ in range(vertexTexturePositionCount):
        u, v = r.getf('<2f')
        mesh.uvs.append((u, 1 - v))
    ############################################################################
    return mesh
