from . import binary_reader
from .. import constants
from io_scene_warcraft_3.classes.WarCraft3Mesh import WarCraft3Mesh
from .get_vertex_groups import get_vertex_groups


def parse_geometry(data):
    r = binary_reader.Reader(data)
    mesh = WarCraft3Mesh()
    mesh.name = 'temp'
    ############################################################################
    chunk_id = r.getid(constants.CHUNK_VERTEX_POSITION)
    vertex_count = r.getf('<I')[0]
    for _ in range(vertex_count):
        vertex_position_x, vertex_position_y, vertex_position_z = r.getf('<3f')
        mesh.vertices.append((vertex_position_x, vertex_position_y, vertex_position_z))
    ############################################################################
    ################################# NOT USED #################################
    ############################################################################
    chunk_id = r.getid(constants.CHUNK_VERTEX_NORMAL)
    normals_count = r.getf('<I')[0]
    for _ in range(normals_count):
        normal = r.getf('<3f')
    ############################################################################
    ################################# NOT USED #################################
    ############################################################################
    chunk_id = r.getid(constants.CHUNK_FACE_TYPE_GROUP)
    face_type_groups_count = r.getf('<I')[0]
    for _ in range(face_type_groups_count):
        face_type = r.getf('<I')[0]
    ############################################################################
    ################################# NOT USED #################################
    ############################################################################
    chunk_id = r.getid(constants.CHUNK_FACE_GROUP)
    face_group_count = r.getf('<I')[0]
    for _ in range(face_group_count):
        indexes_count = r.getf('<I')[0]
    ############################################################################
    chunk_id = r.getid(constants.CHUNK_FACE)
    indices_count = r.getf('<I')[0]
    if indices_count % 3 != 0:
        raise Exception('bad indices (indices_count % 3 != 0)')
    for _ in range(indices_count // 3):
        vertex_index1, vertex_index2, vertex_index3 = r.getf('<3H')
        mesh.triangles.append((vertex_index1, vertex_index2, vertex_index3))
    ############################################################################
    chunk_id = r.getid(constants.CHUNK_VERTEX_GROUP)
    matrix_groups_count = r.getf('<I')[0]
    matrix_groups = []
    for _ in range(matrix_groups_count):
        matrix_group = r.getf('<B')[0]
        matrix_groups.append(matrix_group)
    ############################################################################
    chunk_id = r.getid(constants.CHUNK_MATRIX_GROUP)
    matrix_groups_sizes_count = r.getf('<I')[0]
    matrix_groups_sizes = []
    for _ in range(matrix_groups_sizes_count):
        matrix_group_size = r.getf('<I')[0]
        matrix_groups_sizes.append(matrix_group_size)
    ############################################################################
    chunk_id = r.getid(constants.CHUNK_MATRIX_INDEX)
    matrix_indices_count = r.getf('<I')[0]
    matrix_indices = []
    for _ in range(matrix_indices_count):
        matrix_index = r.getf('<I')[0]
        matrix_indices.append(matrix_index)
    ############################################################################
    vertex_groups, vertex_groups_ids = get_vertex_groups(matrix_groups, matrix_groups_sizes, matrix_indices)
    mesh.vertex_groups = vertex_groups
    mesh.vertex_groups_ids = vertex_groups_ids
    mesh.material_id = r.getf('<I')[0]
    selection_group = r.getf('<I')[0]
    selection_flags = r.getf('<I')[0]
    bounds_radius = r.getf('<f')[0]
    minimum_extent = r.getf('<3f')
    maximum_extent = r.getf('<3f')
    extents_count = r.getf('<I')[0]
    for _ in range(extents_count):
        bounds_radius = r.getf('<f')[0]
        minimum_extent = r.getf('<3f')
        maximum_extent = r.getf('<3f')
    ############################################################################
    ################################# NOT USED #################################
    ############################################################################
    chunk_id = r.getid(constants.CHUNK_TEXTURE_VERTEX_GROUP)
    texture_vertex_group_count = r.getf('<I')[0]
    ############################################################################
    chunk_id = r.getid(constants.CHUNK_VERTEX_TEXTURE_POSITION)
    vertex_texture_position_count = r.getf('<I')[0]
    for _ in range(vertex_texture_position_count):
        u, v = r.getf('<2f')
        mesh.uvs.append((u, 1 - v))
    ############################################################################
    return mesh
