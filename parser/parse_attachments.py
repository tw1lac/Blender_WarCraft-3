from .. import binary
from .parse_attachment import parse_attachment


def parse_attachments(data, model):
    dataSize = len(data)
    r = binary.Reader(data)
    while r.offset < dataSize:
        inclusiveSize = r.getf('<I')[0]
        attachDataSize = inclusiveSize - 4
        attachData = data[r.offset : r.offset + attachDataSize]
        r.skip(attachDataSize)
        parse_attachment(attachData, model)
