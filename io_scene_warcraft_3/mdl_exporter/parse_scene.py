from .parse_mesh import parse_mesh
from .get_parent import get_parent


def parse_scene(model, context, settings):
    scene = context.scene

    objects = []
    materials = set()

    if settings.use_selection:
        objects = (obj for obj in scene.objects if obj.select_get() and obj.visible_get())
    else:
        objects = (obj for obj in scene.objects if obj.visible_get())

    for obj in objects:
        parent = get_parent(obj)

        billboarded = False
        billboard_lock = (False, False, False)
        if hasattr(obj, "mdl_billboard"):
            bb = obj.mdl_billboard
            billboarded = bb.billboarded
            billboard_lock = (bb.billboard_lock_z, bb.billboard_lock_y, bb.billboard_lock_x)
            # NOTE: Axes are listed backwards (same as with colors)

        # # Animations
        # visibility = get_visibility(model.sequences, obj)
        #
        # # Particle Systems
        # if len(obj.particle_systems):
        #     add_particle_systems(model, billboard_lock, billboarded, materials, obj, parent, settings)
        #
        # # Collision Shapes
        # elif obj.type == 'EMPTY' and obj.name.startswith('Collision'):
        #     create_collision_shapes(model, obj, parent, settings)

        if obj.type == 'MESH' :#or obj.type == 'CURVE':
            parse_mesh(model, billboard_lock, billboarded, context, materials, obj, parent, settings)

        # elif obj.type == 'EMPTY':
        #     add_empties_animations(model, billboard_lock, billboarded, obj, parent, settings)
        #
        # elif obj.type == 'ARMATURE':
        #     add_bones(model, billboard_lock, billboarded, obj, parent, settings)
        #
        # elif obj.type in ('LAMP', 'LIGHT'):
        #     add_lights(model, billboard_lock, billboarded, obj, settings)
        #
        # elif obj.type == 'CAMERA':
        #     model.cameras.append(obj)