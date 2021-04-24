from .mdl_reader import extract_bracket_content, chunkifier, get_between
from .parse_geometry import parse_geometry
from ..classes.WarCraft3Mesh import WarCraft3Mesh
from ..classes.WarCraft3Model import WarCraft3Model


def parse_geosets(data, model):
    geoset_data_internal = extract_bracket_content(data)
    geoset_data_chunks = chunkifier(geoset_data_internal)

    mesh = parse_geometry(geoset_data_chunks)

    if data.find("MaterialID") > -1:
        mesh.material_id = int(get_between(data, "MaterialID ", ","))

    # for chunk in geoset_data_chunks:
    #     label = chunk.split(" ", 1)[0]
    #     if label == "Anim":
    #         print("Anim!")
    #         parse_geoset_animations(chunk, model)

    model.meshes.append(mesh)
