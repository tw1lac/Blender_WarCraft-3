def get_vertex_groups(matrixGroups, matrixGroupsSizes, matrixIndices):
    i = 0
    matrix = []

    for matrixGroupSize in matrixGroupsSizes:
        matrix.append(matrixIndices[i: i + matrixGroupSize])
        i += matrixGroupSize

    vertexGroups = []
    vertexGroupsIds = set()

    for matrixGroup in matrixGroups:
        if matrixGroup < len(matrix):
            vertexGroup = matrix[matrixGroup]
            vertexGroups.append(vertexGroup)

            for vertexGroupId in vertexGroup:
                vertexGroupsIds.add(vertexGroupId)

    if len(vertexGroups) == 0:
        for m_i in matrixIndices:
            vertexGroups.append([])
            vertexGroupsIds.add(m_i)

    vertexGroupsIds = list(vertexGroupsIds)
    vertexGroupsIds.sort()

    return vertexGroups, vertexGroupsIds