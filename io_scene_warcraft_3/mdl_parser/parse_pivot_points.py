from .mdl_reader import extract_bracket_content, extract_float_values, chunkifier


def parse_pivot_points(data, model):
    pivot_points = chunkifier(extract_bracket_content(data))

    for pivot_point in pivot_points:
        model.pivot_points.append(extract_float_values(pivot_point))
