import datetime
import getpass

from ...classes.WarCraft3Model import WarCraft3Model
from .write_model_header import write_model_header
from .write_geosets import write_geosets
from ..parse_scene import parse_scene


def file_writer(operator, context, settings, filepath="", mdl_version=800):

    scene = context.scene

    current_frame = scene.frame_current
    scene.frame_set(0)

    model = WarCraft3Model()
    parse_scene(model, context, settings)

    scene.frame_set(current_frame)

    with open(filepath, 'w') as output:
        fw = output.write

        date = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")
        fw("// Exported on %s by %s\n" % (date, getpass.getuser()))

        fw("Version {\n\tFormatVersion %d,\n}\n" % mdl_version)
        # HEADER
        write_model_header(fw, model)

        # # SEQUENCES
        # write_sequences(fw, model)
        #
        # # GLOBAL SEQUENCES
        # write_global_sequences(fw, model)
        #
        # # TEXTURES
        # write_textures(fw, model)
        #
        # # MATERIALS
        # save_materials(fw, model)
        #
        # # TEXTURE ANIMATIONS
        # material_names = save_texture_animations(fw, model)
        material_names = ["ugg","ugg","ugg","ugg","ugg","ugg","ugg","ugg","ugg","ugg","ugg"]

        # GEOSETS
        write_geosets(fw, material_names, model)

        # # GEOSET ANIMS
        # write_geoset_animations(fw, model)
        #
        # # BONES
        # write_bones(fw, model)
        #
        # # LIGHTS
        # write_lights(fw, model)
        #
        # # HELPERS
        # write_helpers(fw, model)
        #
        # # ATTACHMENT POINTS
        # write_attachment_points(fw, model)
        #
        # # PIVOT POINTS
        # write_pivot_points(fw, model)
        #
        # # MODEL EMITTERS
        # write_model_emitters(fw, model)
        #
        # # PARTICLE EMITTERS
        # write_particle_emitters(fw, model)
        #
        # # RIBBON EMITTERS
        # write_ribbon_emitters(fw, model)
        #
        # # CAMERAS
        # write_cameras(fw, model, settings)
        #
        # # EVENT OBJECTS
        # write_event_objects(fw, model)
        #
        # # COLLISION SHAPES
        # write_collision_shape(fw, model)
