import bpy
import bmesh
import bpy
from mathutils import Vector

from .get_parent import get_parent
from ..classes.WarCraft3Mesh import WarCraft3Mesh
from .write_file.utils import rnd


def parse_mesh(model, billboard_lock, billboarded, context, materials, obj, parent, settings):
    mesh_geosets = set()
    mod = None
    if obj.data.use_auto_smooth:
        mod = obj.modifiers.new("EdgeSplitExport", 'EDGE_SPLIT')
        mod.split_angle = obj.data.auto_smooth_angle
        # mod.use_edge_angle = True

    deps_graph = context.evaluated_depsgraph_get()
    mesh = bpy.data.meshes.new_from_object(obj.evaluated_get(deps_graph), preserve_all_data_layers=True, depsgraph=deps_graph)

    if obj.data.use_auto_smooth:
        obj.modifiers.remove(mod)

    # Triangulate for web export
    bm = bmesh.new()
    bm.from_mesh(mesh)

    # # If an object has had a negative scale applied, normals will be inverted. This will fix that.
    # if any(s < 0 for s in obj.scale):
    #     bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    # bmesh.ops.triangulate(bm, faces=bm.faces)
    # bmesh.ops.transform(bm, matrix=matrix, verts=bm.verts)
    # bm.to_mesh(mesh)
    # bm.free()
    # del bm

    mesh.calc_normals_split()
    mesh.calc_loop_triangles()

    # armature = None

    # for m in obj.modifiers:
    #     if m.type == 'ARMATURE':
    #         armature = m
    #
    # bone_names = set()
    #
    # if armature is not None:
    #     bone_names = set(b.name for b in armature.object.data.bones)
    #
    # bone = None
    # if (armature is None and parent is None) or is_animated:
    #     bone = create_bone(anim_loc, anim_rot, anim_scale, obj, parent, settings)
    #     # bone = War3Object(obj.name)  # Object is animated or parent is missing - create a bone for it!
    #     #
    #     # bone.parent = parent  # Remember to make it the parent - parent is added to matrices further down
    #     # bone.pivot = settings.global_matrix @ Vector(obj.location)
    #     # bone.anim_loc = anim_loc
    #     # bone.anim_rot = anim_rot
    #     # bone.anim_scale = anim_scale
    #
    #     if bone.anim_loc is not None:
    #         register_global_sequence(model.global_seqs, bone.anim_loc)
    #         transform_vec(bone.anim_loc.keyframes, bone.anim_loc.interpolation, bone.anim_loc.handles_right,
    #                       bone.anim_loc.handles_left, obj.matrix_world.inverted())
    #         transform_vec(bone.anim_loc.keyframes, bone.anim_loc.interpolation, bone.anim_loc.handles_right,
    #                       bone.anim_loc.handles_left, settings.global_matrix)
    #
    #     if bone.anim_rot is not None:
    #         register_global_sequence(model.global_seqs, bone.anim_rot)
    #         transform_rot(bone.anim_rot.keyframes, obj.matrix_world.inverted())
    #         transform_rot(bone.anim_rot.keyframes, settings.global_matrix)
    #
    #     register_global_sequence(model.global_seqs, bone.anim_scale)
    #     bone.billboarded = billboarded
    #     bone.billboard_lock = billboard_lock
    #
    #     if geoset_anim is not None:
    #         model.geoset_anim_map[bone] = geoset_anim
    #     model.objects['bone'].add(bone)
    #     parent = bone.name

    for tri in mesh.loop_triangles:
        # p = mesh.polygons[f.index]
        # Textures and materials
        mat_name = "default"
        if obj.material_slots and len(obj.material_slots):
            mat = obj.material_slots[tri.material_index].material
            if mat is not None:
                mat_name = mat.name
                materials.add(mat)

        # if (mat_name, geoset_anim_hash) in model.geoset_map.keys():
        #     geoset = model.geoset_map[(mat_name, geoset_anim_hash)]
        # else:
        #     geoset = WarCraft3Mesh()
        #     geoset.mat_name = mat_name
        #     if geoset_anim is not None:
        #         geoset.geoset_anim = geoset_anim
        #         geoset_anim.geoset = geoset
        #
        #     model.geoset_map[(mat_name, geoset_anim_hash)] = geoset
        geoset = None

        geoset = WarCraft3Mesh()
        geoset.mat_name = mat_name
        # if geoset_anim is not None:
        #     geoset.geoset_anim = geoset_anim
        #     geoset_anim.geoset = geoset

        # model.geoset_map[(mat_name, geoset_anim_hash)] = geoset

        # Vertices, faces, and matrices
        vertex_map = {}
        for vert, loop in zip(tri.vertices, tri.loops):
            co = mesh.vertices[vert].co
            coord = (rnd(co.x), rnd(co.y), rnd(co.z))
            normal_raw = mesh.vertices[vert].normal if tri.use_smooth else tri.normal
            normal = (rnd(normal_raw.x), rnd(normal_raw.y), rnd(normal_raw.z))
            uv = mesh.uv_layers.active.data[loop].uv if len(mesh.uv_layers) else Vector((0.0, 0.0))
            uv[1] = 1 - uv[1]  # For some reason, uv Y coordinates appear flipped. This should fix that.
            tvert = (rnd(uv.x), rnd(uv.y))
            groups = None
            matrix = 0

            # if armature is not None:
            #     vertex_groups = sorted(mesh.vertices[vert].groups[:], key=lambda x: x.weight, reverse=True)
            #     # Sort bones by descending weight
            #     if len(vertex_groups):
            #         # Warcraft does not support vertex weights, so we exclude groups with too small influence
            #         groups = list(obj.vertex_groups[vg.group].name for vg in vertex_groups if
            #                       (obj.vertex_groups[vg.group].name in bone_names and vg.weight > 0.25))[:3]
            #         if not len(groups):
            #             for vg in vertex_groups:
            #                 # If we didn't find a group, just take the best match (the list is already sorted by weight)
            #                 if obj.vertex_groups[vg.group].name in bone_names:
            #                     groups = [obj.vertex_groups[vg.group].name]
            #                     break

            # if parent is not None and (groups is None or len(groups) == 0):
            #     groups = [parent]

            # if groups is not None:
            #     if groups not in geoset.matrices:
            #         geoset.matrices.append(groups)
            #     matrix = geoset.matrices.index(groups)

            vertex = (coord, normal, tvert, matrix)
            if vertex not in geoset.vertices:
                geoset.vertices.append(vertex)

            vertex_map[vert] = geoset.vertices.index(vertex)

        # Triangles, normals, vertices, and UVs
        geoset.triangles.append(
            (vertex_map[tri.vertices[0]], vertex_map[tri.vertices[1]], vertex_map[tri.vertices[2]]))

    #     mesh_geosets.add(geoset)
    # for geoset in mesh_geosets:
    #     geoset.objects.append(obj)
    #     if not len(geoset.matrices) and parent is not None:
    #         geoset.matrices.append([parent])

    # obj.to_mesh_clear()
    bpy.data.meshes.remove(mesh)
