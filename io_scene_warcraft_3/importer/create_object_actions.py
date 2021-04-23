from typing import List

import bpy
from bpy.types import Object

from io_scene_warcraft_3 import constants
from io_scene_warcraft_3.classes.WarCraft3Model import WarCraft3Model


def create_object_actions(model: WarCraft3Model, bpy_objects: List[Object], frame_time: float):
    print("creating object animations")
    geoset_animations = model.geoset_animations
    sequences = model.sequences
    data_path_color = 'color'

    for geosetAnimation in geoset_animations:
        geoset_id = geosetAnimation.geoset_id
        action = bpy.data.actions.new(name='#UNANIMATED' + ' ' + bpy_objects[geoset_id].name)
        color_r = action.fcurves.new(data_path_color, index=0)
        color_g = action.fcurves.new(data_path_color, index=1)
        color_b = action.fcurves.new(data_path_color, index=2)
        color_a = action.fcurves.new(data_path_color, index=3)
        color_r.keyframe_points.insert(0.0, 1.0)
        color_g.keyframe_points.insert(0.0, 1.0)
        color_b.keyframe_points.insert(0.0, 1.0)
        color_a.keyframe_points.insert(0.0, 1.0)

    for sequence in sequences:
        interval_start = sequence.interval_start
        interval_end = sequence.interval_end
        for geosetAnimation in geoset_animations:
            geoset_id = geosetAnimation.geoset_id
            color_anim = geosetAnimation.animation_color
            alpha_anim = geosetAnimation.animation_alpha
            action = bpy.data.actions.new(name=sequence.name + ' ' + bpy_objects[geoset_id].name)
            color_r = None
            color_g = None
            color_b = None
            color_a = None
            interpolation_type = constants.INTERPOLATION_TYPE_NAMES[color_anim.interpolation_type]

            for index in range(color_anim.tracks_count):
                time = color_anim.times[index]
                color = color_anim.values[index]
                if interval_start <= time <= interval_end or time == 0:
                    if not color_r:
                        color_r = action.fcurves.new(data_path_color, index=0)
                    if not color_g:
                        color_g = action.fcurves.new(data_path_color, index=1)
                    if not color_b:
                        color_b = action.fcurves.new(data_path_color, index=2)
                    if time == 0:
                        real_time = 0.0
                    else:
                        real_time = round((time - interval_start) / frame_time, 0)
                    color_r_keyframe = color_r.keyframe_points.insert(real_time, color[0])
                    color_g_keyframe = color_g.keyframe_points.insert(real_time, color[1])
                    color_b_keyframe = color_b.keyframe_points.insert(real_time, color[2])
                    color_r_keyframe.interpolation = interpolation_type
                    color_g_keyframe.interpolation = interpolation_type
                    color_b_keyframe.interpolation = interpolation_type
            if not color_r:
                color_r = action.fcurves.new(data_path_color, index=0)
                color_r.keyframe_points.insert(0, 1.0)
            if not color_g:
                color_g = action.fcurves.new(data_path_color, index=1)
                color_g.keyframe_points.insert(0, 1.0)
            if not color_b:
                color_b = action.fcurves.new(data_path_color, index=2)
                color_b.keyframe_points.insert(0, 1.0)
            interpolation_type = constants.INTERPOLATION_TYPE_NAMES[alpha_anim.interpolation_type]

            for index in range(alpha_anim.tracks_count):
                time = alpha_anim.times[index]
                alpha = alpha_anim.values[index]
                if interval_start <= time <= interval_end or time == 0:
                    if not color_a:
                        color_a = action.fcurves.new(data_path_color, index=3)
                    if time == 0:
                        real_time = 0.0
                    else:
                        real_time = round((time - interval_start) / frame_time, 0)
                    color_a_keyframe = color_a.keyframe_points.insert(real_time, alpha)
                    color_a_keyframe.interpolation = interpolation_type
            if not color_a:
                color_a = action.fcurves.new(data_path_color, index=3)
                color_a.keyframe_points.insert(0, 1.0)
