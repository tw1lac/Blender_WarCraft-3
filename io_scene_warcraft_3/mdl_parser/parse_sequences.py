from ..classes.WarCraft3Sequence import WarCraft3Sequence
from .mdl_reader import extract_bracket_content, chunkifier


def parse_sequences(data, model):
    sequences_string = extract_bracket_content(data)
    sequence_chunks = chunkifier(sequences_string)

    for sequence_chunk in sequence_chunks:
        sequence = WarCraft3Sequence()
        sequence.name = sequence_chunk.strip().split("\"")[1]
        sequence_info = extract_bracket_content(sequence_chunk).split(",\n")

        for info in sequence_info:
            label = info.strip().split(" ")[0]

            if label == "Interval":
                interval = extract_bracket_content(info).strip().split(",")
                sequence.interval_start = int(interval[0].strip())
                sequence.interval_end = int(interval[1].strip())

            if label == "MoveSpeed":
                moveSpeed = float(info.strip().replace(",", "").split(" ")[1])

            if label == "NonLooping":
                flags = "NonLooping"

            if label == "MinimumExtent":
                extent = extract_bracket_content(info).strip().split(",")
                minimumExtent = (float(extent[0]), float(extent[1]), float(extent[2]))

            if label == "MaximumExtent":
                extent = extract_bracket_content(info).strip().split(",")
                maximumExtent = (float(extent[0]), float(extent[1]), float(extent[2]))

            if label == "BoundsRadius":
                boundsRadius = float(info.strip().replace(",", "").split(" ")[1])

            if label == "Rarity":
                rarity = float(info.strip().replace(",", "").split(" ")[1])

        model.sequences.append(sequence)
