import bpy
import mathutils

from .. import constants


def create_armature_actions(armatureObject, model, frameTime):
    nodes = model.nodes
    sequences = model.sequences
    action = bpy.data.actions.new(name='#UNANIMATED')
    add_sequence_to_armature('#UNANIMATED', armatureObject)
    for node in nodes:
        boneName = node.node.name
        dataPath = 'pose.bones["' + boneName + '"]'
        new_fcurve(action, boneName, dataPath + '.location', 0.0)
        new_fcurve(action, boneName, dataPath + '.rotation_euler', 0.0)
        new_fcurve(action, boneName, dataPath + '.scale', 1.0)

    for sequence in sequences:
        intervalStart = sequence.interval_start
        intervalEnd = sequence.interval_end
        action = bpy.data.actions.new(name=sequence.name)
        add_sequence_to_armature(sequence.name, armatureObject)
        for node in nodes:
            boneName = node.node.name
            dataPath = 'pose.bones["' + boneName + '"]'
            translations = node.node.translations
            rotations = node.node.rotations
            scalings = node.node.scalings

            if translations:
                locationFcurveX = None
                locationFcurveY = None
                locationFcurveZ = None
                interpolationType = constants.INTERPOLATION_TYPE_NAMES[translations.interpolation_type]
                for index in range(translations.tracks_count):
                    time = translations.times[index]
                    translation = translations.values[index]
                    if intervalStart <= time and time <= intervalEnd:
                        locationFcurveX, locationFcurveY, locationFcurveZ = set_new_curves(action, boneName,
                                                                                           dataPath + '.location',
                                                                                           locationFcurveX,
                                                                                           locationFcurveY,
                                                                                           locationFcurveZ)
                        realTime = round((time - intervalStart) / frameTime, 0)

                        insert_xyz_keyframe_points(interpolationType, locationFcurveX, locationFcurveY, locationFcurveZ,
                                                   realTime, translation)
                set_new_curve_with_keyframe_points(action, boneName, dataPath + '.location',
                                                   locationFcurveX, locationFcurveY, locationFcurveZ, 0.0)

            if rotations:
                rotationFcurveX = None
                rotationFcurveY = None
                rotationFcurveZ = None
                interpolationType = constants.INTERPOLATION_TYPE_NAMES[rotations.interpolation_type]
                for index in range(rotations.tracks_count):
                    time = rotations.times[index]
                    rotation = rotations.values[index]
                    if intervalStart <= time and time <= intervalEnd:
                        rotationFcurveX, rotationFcurveY, rotationFcurveZ = set_new_curves(action, boneName,
                                                                                           dataPath + '.rotation_euler',
                                                                                           rotationFcurveX,
                                                                                           rotationFcurveY,
                                                                                           rotationFcurveZ)
                        euler = mathutils.Quaternion(mathutils.Vector(rotation)).to_euler('XYZ')
                        realTime = round((time - intervalStart) / frameTime, 0)

                        insert_xyz_keyframe_points(interpolationType, rotationFcurveX, rotationFcurveY, rotationFcurveZ,
                                                   realTime, euler)

                set_new_curve_with_keyframe_points(action, boneName, dataPath + '.rotation_euler',
                                                   rotationFcurveX, rotationFcurveY, rotationFcurveZ, 0.0)

            if scalings:
                scaleFcurveX = None
                scaleFcurveY = None
                scaleFcurveZ = None
                interpolationType = constants.INTERPOLATION_TYPE_NAMES[scalings.interpolation_type]
                for index in range(scalings.tracks_count):
                    time = scalings.times[index]
                    scale = scalings.values[index]
                    if intervalStart <= time and time <= intervalEnd:
                        scaleFcurveX, scaleFcurveY, scaleFcurveZ = set_new_curves(action, boneName,
                                                                                  dataPath + '.scale',
                                                                                  scaleFcurveX,
                                                                                  scaleFcurveY,
                                                                                  scaleFcurveZ)
                        realTime = round((time - intervalStart) / frameTime, 0)

                        insert_xyz_keyframe_points(interpolationType, scaleFcurveX, scaleFcurveY, scaleFcurveZ,
                                                   realTime, scale)

                set_new_curve_with_keyframe_points(action, boneName, dataPath + '.scale',
                                                   scaleFcurveX, scaleFcurveY, scaleFcurveZ, 1.0)


def set_new_curve_with_keyframe_points(action, boneName, dataPath, fcurveX, fcurveY, fcurveZ, value):
    if not fcurveX:
        fcurveX = action.fcurves.new(dataPath, 0, boneName)
        fcurveX.keyframe_points.insert(0.0, value)
    if not fcurveY:
        fcurveY = action.fcurves.new(dataPath, 1, boneName)
        fcurveY.keyframe_points.insert(0.0, value)
    if not fcurveZ:
        fcurveZ = action.fcurves.new(dataPath, 2, boneName)
        fcurveZ.keyframe_points.insert(0.0, value)


def set_new_curves(action, boneName, dataPath, fcurveX, fcurveY, fcurveZ):
    if not fcurveX:
        fcurveX = action.fcurves.new(dataPath, 0, boneName)
    if not fcurveY:
        fcurveY = action.fcurves.new(dataPath, 1, boneName)
    if not fcurveZ:
        fcurveZ = action.fcurves.new(dataPath, 2, boneName)
    return fcurveX, fcurveY, fcurveZ


def insert_xyz_keyframe_points(interpolationType, fcurveX, fcurveY, fcurveZ, realTime, movement):
    xKeyframe = fcurveX.keyframe_points.insert(realTime, movement[0])
    yKeyframe = fcurveY.keyframe_points.insert(realTime, movement[1])
    zKeyframe = fcurveZ.keyframe_points.insert(realTime, movement[2])
    xKeyframe.interpolation = interpolationType
    yKeyframe.interpolation = interpolationType
    zKeyframe.interpolation = interpolationType


def new_fcurve(action, boneName, dataPath, value):
    fcurveX = action.fcurves.new(dataPath, 0, boneName)
    fcurveY = action.fcurves.new(dataPath, 1, boneName)
    fcurveZ = action.fcurves.new(dataPath, 2, boneName)
    fcurveX.keyframe_points.insert(0.0, value)
    fcurveY.keyframe_points.insert(0.0, value)
    fcurveZ.keyframe_points.insert(0.0, value)


def add_sequence_to_armature(sequenceName, armatureObject):
    warcraft3data = armatureObject.data.warcraft_3
    sequence = warcraft3data.sequencesList.add()
    sequence.name = sequenceName
