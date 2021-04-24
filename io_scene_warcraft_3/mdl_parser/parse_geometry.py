from ..classes.WarCraft3Mesh import WarCraft3Mesh
from .mdl_reader import chunkifier, extract_bracket_content, extract_float_values, extract_int_values

from .get_vertex_groups import get_vertex_groups


def parse_geometry(geoset_chunks):
    print("parse_geometry")
    mesh = WarCraft3Mesh()
    mesh.name = 'temp'

    matrix_indices = []
    matrix_groups_sizes = []
    matrix_groups = []

    for data_chunk in geoset_chunks:
        label = data_chunk.split(" ", 1)[0]

        if label == "Vertices":
            verts = chunkifier(extract_bracket_content(data_chunk))

            for vert in verts:
                mesh.vertices.append(extract_float_values(vert))

        if label == "Faces":
            triangles = chunkifier(extract_bracket_content(extract_bracket_content(data_chunk)))

            for triangle in triangles:
                triangle_values = extract_float_values(triangle)

                if len(triangle_values) == 3:
                    mesh.triangles.append(triangle_values)

                else:
                    for i in range(len(triangle_values)//3):
                        mesh.triangles.append(triangle_values[i*3:i*3+3])

        if label == "VertexGroup":
            vert_groups = extract_int_values(data_chunk)
            matrix_groups = vert_groups

        if label == "Groups":
            matrices = chunkifier(extract_bracket_content(data_chunk))

            for matrix in matrices:
                matrix_values = extract_int_values(matrix)
                matrix_groups_sizes.append(len(matrix_values))

                for value in matrix_values:
                    matrix_indices.append(value)

        if label == "TVertices":
            t_vertices = chunkifier(extract_bracket_content(data_chunk))

            for t_vertice in t_vertices:
                u, v = extract_float_values(t_vertice)
                mesh.uvs.append((u, 1 - v))

        if label == "SkinWeights":
            weights = chunkifier(extract_bracket_content(data_chunk))

            for weight in weights:
                mesh.skin_weights.append(extract_int_values(weight))

    vertex_groups, vertex_groups_ids = get_vertex_groups(matrix_groups, matrix_groups_sizes, matrix_indices)
    mesh.vertex_groups = vertex_groups
    mesh.vertex_groups_ids = vertex_groups_ids

    return mesh
