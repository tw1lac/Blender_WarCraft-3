from io_scene_warcraft_3.classes.WarCraft3CollisionShape import WarCraft3CollisionShape
from io_scene_warcraft_3 import binary
from io_scene_warcraft_3.parser.parse_node import parse_node


def parse_collision_shapes(data, model):
    dataSize = len(data)
    r = binary.Reader(data)
    while r.offset < dataSize:
        collisionShape = WarCraft3CollisionShape()
        collisionShape.node = parse_node(r)
        type = r.getf('<I')[0]
        if type == 0:
            verticesCount = 2
        elif type == 2:
            verticesCount = 1
        else:
            raise Exception('UNSUPPORTED COLLISION SHAPE TYPE:', type)
        for _ in range(verticesCount):
            position = r.getf('<3f')
        if type == 2:
            boundsRadius = r.getf('<f')[0]
        model.nodes.append(collisionShape)
