from ..classes.WarCraft3Attachment import WarCraft3Attachment
from . import binary_reader
from .parse_attachment_visibility import parse_attachment_visibility
from .parse_node import parse_node


def parse_attachment(data, model):
    r = binary_reader.Reader(data)
    dataSize = len(data)
    attachment = WarCraft3Attachment()
    attachment.node = parse_node(r)
    path = r.gets(260)
    attachmentId = r.getf('<I')[0]

    if r.offset < dataSize:
        parse_attachment_visibility(r)

    model.nodes.append(attachment)
