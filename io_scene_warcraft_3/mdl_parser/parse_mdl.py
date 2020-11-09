from ..classes.WarCraft3Model import WarCraft3Model
from ..importer import importer
from .mdl_reader import Reader
from .parse_attachments import parse_attachments
from .parse_bones import parse_bones
from .parse_collision_shapes import parse_collision_shapes
from .parse_events import parse_events
from .parse_geoset_animations import parse_geoset_animations
from .parse_geosets import parse_geosets
from .parse_helpers import parse_helpers
from .parse_materials import parse_materials
from .parse_model import parse_model
from .parse_pivot_points import parse_pivot_points
from .parse_sequences import parse_sequences
from .parse_textures import parse_textures
from .parse_version import parse_version


def parse_mdl(data, importProperties):
    reader = Reader(data)
    model = WarCraft3Model()
    data_chunks = reader.chunks
    for chunk in data_chunks:
        label = chunk.split(" ", 1)[0]
        if label == "Version":
            parse_version(chunk)
        elif label == "Geoset":
            parse_geosets(chunk, model)
        elif label == "Textures":
            parse_textures(chunk, model)
        elif label == "Materials":
            parse_materials(chunk, model)
        elif label == "Model":
            parse_model(chunk, model)
        elif label == "Bone":
            parse_bones(chunk, model)
        elif label == "PivotPoints":
            parse_pivot_points(chunk, model)
        elif label == "Helper":
            parse_helpers(chunk, model)
        elif label == "Attachment":
            parse_attachments(chunk, model)
        elif label == "EventObject":
            parse_events(chunk, model)
        elif label == "CollisionShape":
            parse_collision_shapes(chunk, model)
        elif label == "Sequences":
            parse_sequences(chunk, model)
        elif label == "GeosetAnim":
            parse_geoset_animations(chunk, model)
    importer.load_warcraft_3_model(model, importProperties)


# this is for commandline testing
def parse_mdl2(data):
    print("parse_mdl2")
    reader = Reader(data)
    model = WarCraft3Model()
    data_chunks = reader.chunks
    # print(data_chunks)
    for chunk in data_chunks:
        label = chunk.split(" ", 1)[0]
        # print("label: ", label)
        if label == "Version":
            print("parse: Version")
            parse_version(chunk)

        elif label == "Geoset":
            print("parse: Geoset")
            parse_geosets(chunk, model)

        elif label == "Textures":
            print("parse: Textures")
            parse_textures(chunk, model)

        elif label == "Materials":
            print("parse: Materials")
            parse_materials(chunk, model)

        elif label == "Model":
            print("parse: Model")
            parse_model(chunk, model)

        elif label == "Bone":
            # print("parse: Bone")
            parse_bones(chunk, model)

        elif label == "PivotPoints":
            print("parse: PivotPoints")
            parse_pivot_points(chunk, model)

        elif label == "Helper":
            # print("parse: Helper")
            parse_helpers(chunk, model)

        elif label == "Attachment":
            # print("parse: Attachment")
            parse_attachments(chunk, model)

        elif label == "EventObject":
            # print("parse: EventObject")
            parse_events(chunk, model)

        elif label == "CollisionShape":
            # print("parse: CollisionShape")
            parse_collision_shapes(chunk, model)

        elif label == "Sequences":
            print("parse: Sequences")
            parse_sequences(chunk, model)

        elif label == "GeosetAnim":
            print("parse: GeosetAnim")
            parse_geoset_animations(chunk, model)

    importer.load_warcraft_3_model2(model)
