from ..classes.WarCraft3CollisionShape import WarCraft3CollisionShape
from .parse_node import parse_node


def parse_collision_shapes(data, model):
    collisionShape = WarCraft3CollisionShape()
    collisionShape.node = parse_node(data)
    model.nodes.append(collisionShape)
