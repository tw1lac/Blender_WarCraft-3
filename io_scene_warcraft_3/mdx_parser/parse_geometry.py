from ..classes.WarCraft3Mesh import WarCraft3Mesh
from .binary_reader import Reader
from .. import constants
from .get_vertex_groups import get_vertex_groups


def parse_geometry(data, version):
    r = Reader(data)
    mesh = WarCraft3Mesh()
    mesh.name = 'temp'

    # parse vertices
    chunk_id = r.getid(constants.CHUNK_VERTEX_POSITION)
    print(chunk_id)
    vertex_count = r.getf('<I')[0]
    print(vertex_count)

    for _ in range(vertex_count):
        vertex_position_x, vertex_position_y, vertex_position_z = r.getf('<3f')
        # print(vertex_position_x, ", ", vertex_position_y, ", ", vertex_position_z)
        mesh.vertices.append((vertex_position_x, vertex_position_y, vertex_position_z))

    # Read and ignore
    chunks_to_skip = [[constants.CHUNK_VERTEX_NORMAL, '<3f'], [constants.CHUNK_FACE_TYPE_GROUP, '<I'], [constants.CHUNK_FACE_GROUP, '<I']]
    for chunk in chunks_to_skip:
        chunk_id = r.getid(chunk[0])
        count = r.getf('<I')[0]

        for _ in range(count):
            chunk_thing = r.getf(chunk[1])

    # parse
    chunk_id = r.getid(constants.CHUNK_FACE)
    indices_count = r.getf('<I')[0]

    if indices_count % 3 != 0:
        raise Exception('bad indices (indices_count % 3 != 0)')

    for _ in range(indices_count // 3):
        vertex_index1, vertex_index2, vertex_index3 = r.getf('<3H')
        mesh.triangles.append((vertex_index1, vertex_index2, vertex_index3))

    # parse vertex groups
    chunk_id = r.getid(constants.CHUNK_VERTEX_GROUP)
    matrix_groups_count = r.getf('<I')[0]
    matrix_groups = []

    for _ in range(matrix_groups_count):
        matrix_group = r.getf('<B')[0]
        matrix_groups.append(matrix_group)

    # parse matrix Groups
    chunk_id = r.getid(constants.CHUNK_MATRIX_GROUP)
    matrix_groups_sizes_count = r.getf('<I')[0]
    matrix_groups_sizes = []

    for _ in range(matrix_groups_sizes_count):
        matrix_group_size = r.getf('<I')[0]
        matrix_groups_sizes.append(matrix_group_size)

    # parse MatrixIndices
    chunk_id = r.getid(constants.CHUNK_MATRIX_INDEX)
    matrix_indices_count = r.getf('<I')[0]
    matrix_indices = []

    for _ in range(matrix_indices_count):
        matrix_index = r.getf('<I')[0]
        matrix_indices.append(matrix_index)

    # parse vertex groups
    vertex_groups, vertex_groups_ids = get_vertex_groups(matrix_groups, matrix_groups_sizes, matrix_indices)
    mesh.vertex_groups = vertex_groups
    mesh.vertex_groups_ids = vertex_groups_ids
    mesh.material_id = r.getf('<I')[0]
    selection_group = r.getf('<I')[0]
    selection_flags = r.getf('<I')[0]

    # if constants.MDX_CURRENT_VERSION > 800:
    if version > 800:
        lod = r.getf('<I')[0]
        lod_name = r.gets(80)

    bounds_radius = r.getf('<f')[0]
    minimum_extent = r.getf('<3f')
    maximum_extent = r.getf('<3f')
    extents_count = r.getf('<I')[0]

    for _ in range(extents_count):
        bounds_radius = r.getf('<f')[0]
        minimum_extent = r.getf('<3f')
        maximum_extent = r.getf('<3f')

    # if constants.MDX_CURRENT_VERSION > 800:
    if version > 800:
        chunk_id = r.getid((constants.CHUNK_TANGENTS, constants.CHUNK_SKIN, constants.CHUNK_TEXTURE_VERTEX_GROUP))
        if chunk_id == constants.CHUNK_TANGENTS:
            tangent_size = r.getf('<I')[0]
            r.skip(16 * tangent_size)
            chunk_id = r.getid((constants.CHUNK_SKIN, constants.CHUNK_TEXTURE_VERTEX_GROUP))
        if chunk_id == constants.CHUNK_SKIN:
            skin_size = r.getf('<I')[0]
            r.skip(skin_size)
            chunk_id = r.getid(constants.CHUNK_TEXTURE_VERTEX_GROUP)
    else:
        chunk_id = r.getid(constants.CHUNK_TEXTURE_VERTEX_GROUP)
    texture_vertex_group_count = r.getf('<I')[0]

    # parse uv-coordinates
    chunk_id = r.getid(constants.CHUNK_VERTEX_TEXTURE_POSITION)
    vertex_texture_position_count = r.getf('<I')[0]

    for _ in range(vertex_texture_position_count):
        u, v = r.getf('<2f')
        mesh.uvs.append((u, 1 - v))

    return mesh
