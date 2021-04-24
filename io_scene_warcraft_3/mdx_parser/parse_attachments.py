from . import binary_reader
from .parse_attachment import parse_attachment
from ..classes.WarCraft3Model import WarCraft3Model


def parse_attachments(data, model):
    data_size = len(data)
    r = binary_reader.Reader(data)

    while r.offset < data_size:
        inclusive_size = r.getf('<I')[0]
        attach_data_size = inclusive_size - 4
        attach_data = data[r.offset : r.offset + attach_data_size]
        r.skip(attach_data_size)
        parse_attachment(attach_data, model)
