import bpy
import mathutils

from io_scene_warcraft_3 import constants


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
                pose_bones(action, boneName, dataPath + '.location', frameTime, intervalEnd, intervalStart, translations, 0.0)

            if rotations:
                rotationFcurves = [None, None, None]
                interpolationType = constants.INTERPOLATION_TYPE_NAMES[rotations.interpolation_type]

                for index in range(rotations.tracks_count):
                    time = rotations.times[index]
                    rotation = rotations.values[index]
                    euler = mathutils.Quaternion(mathutils.Vector(rotation)).to_euler('XYZ')

                    if intervalStart <= time <= intervalEnd:
                        rotationFcurves = set_new_curves(action, boneName, dataPath + '.rotation_euler', rotationFcurves)
                        realTime = round((time - intervalStart) / frameTime, 0)

                        insert_xyz_keyframe_points(interpolationType, rotationFcurves, realTime, euler)

                set_new_curves(action, boneName, dataPath + '.rotation_euler', rotationFcurves, 0.0)

            if scalings:
                pose_bones(action, boneName, dataPath + '.scale', frameTime, intervalEnd, intervalStart,
                           scalings, 1.0)


def pose_bones(action, boneName, dataPath, frameTime, intervalEnd, intervalStart, adjustments, value):
    fcurves = [None, None, None]
    interpolationType = constants.INTERPOLATION_TYPE_NAMES[adjustments.interpolation_type]

    for index in range(adjustments.tracks_count):
        time = adjustments.times[index]
        adjustment = adjustments.values[index]

        if intervalStart <= time <= intervalEnd:
            fcurves = set_new_curves(action, boneName, dataPath, fcurves)
            realTime = round((time - intervalStart) / frameTime, 0)

            insert_xyz_keyframe_points(interpolationType, fcurves, realTime, adjustment)

    set_new_curves(action, boneName, dataPath, fcurves, value)


def set_new_curves(action, boneName, dataPath, fcurves, value=-1.0):
    for i in range(len(fcurves)):
        if not fcurves[i]:
            fcurves[i] = action.fcurves.new(dataPath, i, boneName)
            if value != -1.0:
                fcurves[i].keyframe_points.insert(0.0, value)
    return fcurves


def insert_xyz_keyframe_points(interpolationType, fcurves, realTime, movement):
    for i in range(len(fcurves)):
        keyframe = fcurves[i].keyframe_points.insert(realTime, movement[i])
        keyframe.interpolation = interpolationType


def new_fcurve(action, boneName, dataPath, value):
    for i in range(3):
        fcurve = action.fcurves.new(dataPath, i, boneName)
        fcurve.keyframe_points.insert(0.0, value)


def add_sequence_to_armature(sequenceName, armatureObject):
    warcraft3data = armatureObject.data.warcraft_3
    sequence = warcraft3data.sequencesList.add()
    sequence.name = sequenceName
