from ..classes.WarCraft3Attachment import WarCraft3Attachment
from .parse_node import parse_node
from ..classes.WarCraft3Model import WarCraft3Model


def parse_attachments(data, model: WarCraft3Model):
    attachment = WarCraft3Attachment()
    attachment.node = parse_node(data)
    model.nodes.append(attachment)
