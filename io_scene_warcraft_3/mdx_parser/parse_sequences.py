from . import binary_reader
from io_scene_warcraft_3.classes.WarCraft3Sequence import WarCraft3Sequence


def parse_sequences(data, model):
    r = binary_reader.Reader(data)
    dataSize = len(data)
    if dataSize % 132 != 0:
        raise Exception('bad sequence data (size % 132 != 0)')
    sequenceCount = dataSize // 132
    for _ in range(sequenceCount):
        sequence = WarCraft3Sequence()
        sequence.name = r.gets(80)
        sequence.interval_start = r.getf('<I')[0]
        sequence.interval_end = r.getf('<I')[0]
        moveSpeed = r.getf('<f')[0]
        flags = r.getf('<I')[0]
        rarity = r.getf('<f')[0]
        syncPoint = r.getf('<I')[0]
        boundsRadius = r.getf('<f')[0]
        minimumExtent = r.getf('<3f')
        maximumExtent = r.getf('<3f')
        model.sequences.append(sequence)
