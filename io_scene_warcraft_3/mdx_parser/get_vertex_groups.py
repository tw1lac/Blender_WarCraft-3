def get_vertex_groups(matrix_groups, matrix_groups_sizes, matrix_indices):
    i = 0
    matrix = []

    for matrixGroupSize in matrix_groups_sizes:
        matrix.append(matrix_indices[i: i + matrixGroupSize])
        i += matrixGroupSize

    vertex_groups = []
    vertex_groups_ids = set()

    for matrixGroup in matrix_groups:
        if matrixGroup < len(matrix):
            vertex_group = matrix[matrixGroup]
            vertex_groups.append(vertex_group)

            for vertexGroupId in vertex_group:
                vertex_groups_ids.add(vertexGroupId)

    if len(vertex_groups) == 0:
        for m_i in matrix_indices:
            vertex_groups.append([])
            vertex_groups_ids.add(m_i)

    vertex_groups_ids = list(vertex_groups_ids)
    vertex_groups_ids.sort()

    return vertex_groups, vertex_groups_ids
