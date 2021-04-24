from . import binary_reader
from io_scene_warcraft_3.classes.WarCraft3Attachment import WarCraft3Attachment
from .parse_attachment_visibility import parse_attachment_visibility
from .parse_node import parse_node


def parse_attachment(data, model):
    r = binary_reader.Reader(data)
    data_size = len(data)
    attachment = WarCraft3Attachment()
    attachment.node = parse_node(r)
    path = r.gets(260)
    attachment_id = r.getf('<I')[0]
    if r.offset < data_size:
        parse_attachment_visibility(r)
    model.nodes.append(attachment)
