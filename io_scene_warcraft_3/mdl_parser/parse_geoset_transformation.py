import re
from ..classes.WarCraft3GeosetTransformation import WarCraft3GeosetTransformation
from .. import constants
from .mdl_reader import extract_bracket_content, extract_float_values, chunkifier


def parse_geoset_transformation(node_chunk):
    transformation = WarCraft3GeosetTransformation()
    transformation.tracks_count = int(node_chunk.split(" ")[1])

    transformation_chunk = extract_bracket_content(node_chunk)
    transformation.interpolation_type = constants.INTERPOLATION_TYPE_NUMBERS[transformation_chunk.split(",")[0].strip()]
    globalSequenceId = -1

    points_start = transformation_chunk.find(",")
    transformation_points = re.split(',\s*(?=\d+:)', transformation_chunk[points_start+1:])

    for point in transformation_points:
        if point != '' and re.match('\d+:', point.strip('\n\t')):
            time = int(point.split(":")[0])
            point_stuff = chunkifier(point)

            for stuff in point_stuff:
                line_start = stuff.split(" ")[0].strip('\n\t ,')
                line_values = extract_float_values(stuff)

                if len(line_values) == 4:
                    line_values = (line_values[3], line_values[0], line_values[1], line_values[2])

                if line_start == "InTan":
                    inTan = line_values

                if line_start == "OutTan":
                    outTan = line_values

                if re.match("\d+", line_start):
                    values = line_values
                    transformation.times.append(time)
                    transformation.values.append(values)

    return transformation
