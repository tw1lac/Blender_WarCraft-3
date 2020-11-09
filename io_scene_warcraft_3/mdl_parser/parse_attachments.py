from ..classes.WarCraft3Attachment import WarCraft3Attachment
from .parse_node import parse_node


def parse_attachments(data, model):
    attachment = WarCraft3Attachment()
    attachment.node = parse_node(data)
    model.nodes.append(attachment)
