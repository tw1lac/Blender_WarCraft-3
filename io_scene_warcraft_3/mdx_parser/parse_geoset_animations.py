from ..classes.WarCraft3GeosetAnimation import WarCraft3GeosetAnimation
from ..classes.WarCraft3GeosetTransformation import WarCraft3GeosetTransformation
from .. import constants
from . import binary_reader
from .parse_geoset_alpha import parse_geoset_alpha
from .parse_geoset_color import parse_geoset_color
from ..classes.WarCraft3Model import WarCraft3Model


def parse_geoset_animations(data, model: WarCraft3Model):
    r = binary_reader.Reader(data)
    data_size = len(data)

    while r.offset < data_size:
        geoset_animation = WarCraft3GeosetAnimation()
        inclusive_size = r.offset + r.getf('<I')[0]
        alpha = r.getf('<f')[0]
        flags = r.getf('<I')[0]
        color = r.getf('<3f')
        geoset_animation.geoset_id = r.getf('<I')[0]

        while r.offset < inclusive_size:
            chunk_id = r.getid(constants.SUB_CHUNKS_GEOSET_ANIMATION)

            if chunk_id == constants.CHUNK_GEOSET_COLOR:
                geoset_animation.animation_color = parse_geoset_color(r)
            elif chunk_id == constants.CHUNK_GEOSET_ALPHA:
                geoset_animation.animation_alpha = parse_geoset_alpha(r)

        if not geoset_animation.animation_color:
            geoset_color = WarCraft3GeosetTransformation()
            geoset_color.tracks_count = 1
            geoset_color.interpolation_type = constants.INTERPOLATION_TYPE_NONE
            geoset_color.times = [0, ]
            geoset_color.values = [color, ]
            geoset_animation.animation_color = geoset_color

        if not geoset_animation.animation_alpha:
            geoset_alpha = WarCraft3GeosetTransformation()
            geoset_alpha.tracks_count = 1
            geoset_alpha.interpolation_type = constants.INTERPOLATION_TYPE_NONE
            geoset_alpha.times = [0, ]
            geoset_alpha.values = [alpha, ]
            geoset_animation.animation_alpha = geoset_alpha

        model.geoset_animations.append(geoset_animation)
