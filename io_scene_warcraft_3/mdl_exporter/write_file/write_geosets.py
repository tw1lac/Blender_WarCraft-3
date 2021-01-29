from .utils import f2s, calc_bounds_radius


def write_geosets(fw, material_names, model):
    if len(model.geosets):
        for geoset in model.meshes:
            fw("Geoset {\n")
            # Vertices
            fw("\tVertices %d {\n" % len(geoset.vertices))
            for vertex in geoset.vertices:
                fw("\t\t{%s, %s, %s},\n" % tuple(map(f2s, vertex[0])))
            fw("\t}\n")
            # Normals
            fw("\tNormals %d {\n" % len(geoset.vertices))
            for normal in geoset.vertices:
                fw("\t\t{%s, %s, %s},\n" % tuple(map(f2s, normal[1])))
            fw("\t}\n")

            # TVertices
            fw("\tTVertices %d {\n" % len(geoset.vertices))
            for tvertex in geoset.vertices:
                fw("\t\t{%s, %s},\n" % tuple(map(f2s, tvertex[2])))
            fw("\t}\n")

            # VertexGroups
            fw("\tVertexGroup {\n")
            for vertgroup in geoset.vertices:
                fw("\t\t%d,\n" % vertgroup[3])
            fw("\t}\n")

            # Faces
            fw("\tFaces %d %d {\n" % (len(geoset.triangles), len(geoset.triangles) * 3))
            fw("\t\tTriangles {\n")
            for triangle in geoset.triangles:
                fw("\t\t\t{%d, %d, %d},\n" % triangle[:])

            fw("\t\t}\n")
            fw("\t}\n")

            # fw("\tGroups %d %d {\n" % (len(geoset.matrices), sum(len(mtrx) for mtrx in geoset.matrices)))
            # for matrix in geoset.matrices:
            #     fw("\t\tMatrices {%s},\n" % ','.join(str(model.object_indices[g]) for g in matrix))
            # fw("\t}\n")

            # fw("\tMinimumExtent {%s, %s, %s},\n" % tuple(map(f2s, geoset.min_extent)))
            # fw("\tMaximumExtent {%s, %s, %s},\n" % tuple(map(f2s, geoset.max_extent)))
            # fw("\tBoundsRadius %s,\n" % f2s(calc_bounds_radius(geoset.min_extent, geoset.max_extent)))
            #
            # for sequence in model.sequences:
            #     fw("\tAnim {\n")
            #
            #     # As of right now, we just use the geoset bounds.
            #     fw("\t\tMinimumExtent {%s, %s, %s},\n" % tuple(map(f2s, geoset.min_extent)))
            #     fw("\t\tMaximumExtent {%s, %s, %s},\n" % tuple(map(f2s, geoset.max_extent)))
            #     fw("\t\tBoundsRadius %s,\n" % f2s(calc_bounds_radius(geoset.min_extent, geoset.max_extent)))
            #
            #     fw("\t}\n")

            # fw("\tMaterialID %d,\n" % material_names.index(geoset.mat_name))
            fw("\tMaterialID %d,\n" % geoset.material_id)

            fw("}\n")
