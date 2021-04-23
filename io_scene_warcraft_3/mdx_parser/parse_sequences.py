from ..classes.WarCraft3Model import WarCraft3Model
from ..classes.WarCraft3Sequence import WarCraft3Sequence
from . import binary_reader


def parse_sequences(data, model: WarCraft3Model):
    r = binary_reader.Reader(data)
    data_size = len(data)

    if data_size % 132 != 0:
        raise Exception('bad sequence data (size % 132 != 0)')

    sequence_count = data_size // 132

    for _ in range(sequence_count):
        sequence = WarCraft3Sequence()
        sequence.name = r.gets(80)
        sequence.interval_start = r.getf('<I')[0]
        sequence.interval_end = r.getf('<I')[0]
        move_speed = r.getf('<f')[0]
        flags = r.getf('<I')[0]
        rarity = r.getf('<f')[0]
        sync_point = r.getf('<I')[0]
        bounds_radius = r.getf('<f')[0]
        minimum_extent = r.getf('<3f')
        maximum_extent = r.getf('<3f')
        model.sequences.append(sequence)
