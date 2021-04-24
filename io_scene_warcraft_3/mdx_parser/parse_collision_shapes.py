from . import binary_reader
from io_scene_warcraft_3.classes.WarCraft3CollisionShape import WarCraft3CollisionShape
from .parse_node import parse_node


def parse_collision_shapes(data, model):
    data_size = len(data)
    r = binary_reader.Reader(data)
    while r.offset < data_size:
        collision_shape = WarCraft3CollisionShape()
        collision_shape.node = parse_node(r)
        value_type = r.getf('<I')[0]
        if value_type == 0:
            vertices_count = 2
        elif value_type == 2:
            vertices_count = 1
        else:
            raise Exception('UNSUPPORTED COLLISION SHAPE TYPE:', value_type)
        for _ in range(vertices_count):
            position = r.getf('<3f')
        if value_type == 2:
            bounds_radius = r.getf('<f')[0]
        model.nodes.append(collision_shape)
