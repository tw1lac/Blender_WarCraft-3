import bpy

from .. import constants


def create_object_actions(model, bpyObjects, frameTime):
    geosetAnimations = model.geoset_animations
    sequences = model.sequences
    dataPathColor = 'color'
    for geosetAnimation in geosetAnimations:
        geosetId = geosetAnimation.geoset_id
        action = bpy.data.actions.new(name='#UNANIMATED' + ' ' + bpyObjects[geosetId].name)
        colorR = action.fcurves.new(dataPathColor, 0)
        colorG = action.fcurves.new(dataPathColor, 1)
        colorB = action.fcurves.new(dataPathColor, 2)
        colorA = action.fcurves.new(dataPathColor, 3)
        colorR.keyframe_points.insert(0.0, 1.0)
        colorG.keyframe_points.insert(0.0, 1.0)
        colorB.keyframe_points.insert(0.0, 1.0)
        colorA.keyframe_points.insert(0.0, 1.0)
    for sequence in sequences:
        intervalStart = sequence.interval_start
        intervalEnd = sequence.interval_end
        for geosetAnimation in geosetAnimations:
            geosetId = geosetAnimation.geoset_id
            colorAnim = geosetAnimation.animation_color
            alphaAnim = geosetAnimation.animation_alpha
            action = bpy.data.actions.new(name=sequence.name + ' ' + bpyObjects[geosetId].name)
            colorR = None
            colorG = None
            colorB = None
            colorA = None
            interpolationType = constants.INTERPOLATION_TYPE_NAMES[colorAnim.interpolation_type]
            for index in range(colorAnim.tracks_count):
                time = colorAnim.times[index]
                color = colorAnim.values[index]
                if intervalStart <= time and time <= intervalEnd or time == 0:
                    if not colorR:
                        colorR = action.fcurves.new(dataPathColor, 0)
                    if not colorG:
                        colorG = action.fcurves.new(dataPathColor, 1)
                    if not colorB:
                        colorB = action.fcurves.new(dataPathColor, 2)
                    if time == 0:
                        realTime = 0.0
                    else:
                        realTime = round((time - intervalStart) / frameTime, 0)
                    colorRKeyframe = colorR.keyframe_points.insert(realTime, color[0])
                    colorGKeyframe = colorG.keyframe_points.insert(realTime, color[1])
                    colorBKeyframe = colorB.keyframe_points.insert(realTime, color[2])
                    colorRKeyframe.interpolation = interpolationType
                    colorGKeyframe.interpolation = interpolationType
                    colorBKeyframe.interpolation = interpolationType
            if not colorR:
                colorR = action.fcurves.new(dataPathColor, 0)
                colorR.keyframe_points.insert(0, 1.0)
            if not colorG:
                colorG = action.fcurves.new(dataPathColor, 1)
                colorG.keyframe_points.insert(0, 1.0)
            if not colorB:
                colorB = action.fcurves.new(dataPathColor, 2)
                colorB.keyframe_points.insert(0, 1.0)
            interpolationType = constants.INTERPOLATION_TYPE_NAMES[alphaAnim.interpolation_type]
            for index in range(alphaAnim.tracks_count):
                time = alphaAnim.times[index]
                alpha = alphaAnim.values[index]
                if intervalStart <= time and time <= intervalEnd or time == 0:
                    if not colorA:
                        colorA = action.fcurves.new(dataPathColor, 3)
                    if time == 0:
                        realTime = 0.0
                    else:
                        realTime = round((time - intervalStart) / frameTime, 0)
                    colorAKeyframe = colorA.keyframe_points.insert(realTime, alpha)
                    colorAKeyframe.interpolation = interpolationType
            if not colorA:
                colorA = action.fcurves.new(dataPathColor, 3)
                colorA.keyframe_points.insert(0, 1.0)
