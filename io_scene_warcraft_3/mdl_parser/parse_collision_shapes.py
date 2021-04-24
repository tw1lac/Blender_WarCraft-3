from ..classes.WarCraft3CollisionShape import WarCraft3CollisionShape
from .parse_node import parse_node
from ..classes.WarCraft3Model import WarCraft3Model


def parse_collision_shapes(data, model):
    collision_shape = WarCraft3CollisionShape()
    collision_shape.node = parse_node(data)
    model.nodes.append(collision_shape)
