import bpy
import mathutils

from io_scene_warcraft_3 import constants


def create_armature_actions(armatureObject, model, frameTime):
    nodes = model.nodes
    sequences = model.sequences
    action = bpy.data.actions.new(name='#UNANIMATED')
    add_sequence_to_armature('#UNANIMATED', armatureObject)

    for node in nodes:
        add_unanimated_to_bones(action, node)

    for sequence in sequences:
        intervalStart = sequence.interval_start
        intervalEnd = sequence.interval_end
        action = bpy.data.actions.new(name=sequence.name)
        add_sequence_to_armature(sequence.name, armatureObject)

        for node in nodes:
            add_actions_to_bones(action, frameTime, intervalEnd, intervalStart, node)


def add_unanimated_to_bones(action, node):
    boneName = node.node.name
    dataPath = 'pose.bones["' + boneName + '"]'
    new_fcurve(action, boneName, dataPath + '.location', 0.0)
    new_fcurve(action, boneName, dataPath + '.rotation_euler', 0.0)
    new_fcurve(action, boneName, dataPath + '.scale', 1.0)


def add_actions_to_bones(action, frameTime, intervalEnd, intervalStart, node):
    boneName = node.node.name
    dataPath = 'pose.bones["' + boneName + '"]'
    translations = node.node.translations
    rotations = node.node.rotations
    scalings = node.node.scalings

    if translations:
        create_transformation_curves(action, boneName, 'location', frameTime, intervalEnd, intervalStart,
                                     translations, 0.0,
                                     lambda translation: translation)
    if rotations:
        create_transformation_curves(action, boneName, 'rotation_euler', frameTime, intervalEnd, intervalStart,
                                     rotations, 0.0,
                                     lambda rotation: (mathutils.Quaternion(mathutils.Vector(rotation)).to_euler('XYZ')))

    if scalings:
        create_transformation_curves(action, boneName, 'scale', frameTime, intervalEnd, intervalStart,
                                     scalings, 1.0,
                                     lambda scaling: scaling)


def create_transformation_curves(action, boneName, data_path_addition, frameTime, intervalEnd, intervalStart,
                                 transformations, transformation_zero_value, value_conversion):
    dataPath = 'pose.bones["' + boneName + '"].'+ data_path_addition
    # starting_keyframe = round(sequence_start / frameTime, 0)

    interpolationType = constants.INTERPOLATION_TYPE_NAMES[transformations.interpolation_type]
    transformationfcurves = [None, None, None]

    for index in range(transformations.tracks_count):
        time = transformations.times[index]
        transformation = transformations.values[index]
        converted_values = value_conversion(transformation)

        if intervalStart <= time <= intervalEnd:
            realTime = round((time - intervalStart) / frameTime, 0)
            transformationfcurves = set_new_curves(action, boneName, dataPath, transformationfcurves, 0)
            insert_xyz_keyframe_points(interpolationType, transformationfcurves, realTime, converted_values)

    set_new_curves(action, boneName, dataPath, transformationfcurves, transformation_zero_value)


def set_new_curves(action, boneName, dataPath, fcurves, value=-1.0):
    for i in range(len(fcurves)):
        if not fcurves[i]:
            fcurves[i] = action.fcurves.new(dataPath, index=i, action_group=boneName)
            if value != -1.0:
                fcurves[i].keyframe_points.insert(0.0, value)
    return fcurves


def insert_xyz_keyframe_points(interpolationType, fcurves, realTime, movement):
    for i in range(len(fcurves)):
        keyframe = fcurves[i].keyframe_points.insert(realTime, movement[i])
        keyframe.interpolation = interpolationType


def new_fcurve(action, boneName, dataPath, value):
    for i in range(3):
        fcurve = action.fcurves.new(dataPath, index=i, action_group=boneName)
        fcurve.keyframe_points.insert(0.0, value)


def add_sequence_to_armature(sequenceName, armatureObject):
    warcraft3data = armatureObject.data.warcraft_3
    sequence = warcraft3data.sequencesList.add()
    sequence.name = sequenceName
