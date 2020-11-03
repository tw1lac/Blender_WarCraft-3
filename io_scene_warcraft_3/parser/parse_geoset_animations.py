from io_scene_warcraft_3.classes.WarCraft3GeosetAnimation import WarCraft3GeosetAnimation
from io_scene_warcraft_3.classes.WarCraft3GeosetTransformation import WarCraft3GeosetTransformation
from io_scene_warcraft_3 import binary, constants
from io_scene_warcraft_3.parser.parse_geoset_alpha import parse_geoset_alpha
from io_scene_warcraft_3.parser.parse_geoset_color import parse_geoset_color


def parse_geoset_animations(data, model):
    r = binary.Reader(data)
    dataSize = len(data)
    while r.offset < dataSize:
        geosetAnimation = WarCraft3GeosetAnimation()
        inclusiveSize = r.offset + r.getf('<I')[0]
        alpha = r.getf('<f')[0]
        flags = r.getf('<I')[0]
        color = r.getf('<3f')
        geosetAnimation.geoset_id = r.getf('<I')[0]
        while r.offset < inclusiveSize:
            chunkId = r.getid(constants.SUB_CHUNKS_GEOSET_ANIMATION)
            if chunkId == constants.CHUNK_GEOSET_COLOR:
                geosetAnimation.animation_color = parse_geoset_color(r)
            elif chunkId == constants.CHUNK_GEOSET_ALPHA:
                geosetAnimation.animation_alpha = parse_geoset_alpha(r)
        if not geosetAnimation.animation_color:
            geosetColor = WarCraft3GeosetTransformation()
            geosetColor.tracks_count = 1
            geosetColor.interpolation_type = constants.INTERPOLATION_TYPE_NONE
            geosetColor.times = [0, ]
            geosetColor.values = [color, ]
            geosetAnimation.animation_color = geosetColor
        if not geosetAnimation.animation_alpha:
            geosetAlpha = WarCraft3GeosetTransformation()
            geosetAlpha.tracks_count = 1
            geosetAlpha.interpolation_type = constants.INTERPOLATION_TYPE_NONE
            geosetAlpha.times = [0, ]
            geosetAlpha.values = [alpha, ]
            geosetAnimation.animation_alpha = geosetAlpha
        model.geoset_animations.append(geosetAnimation)
