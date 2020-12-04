import bpy
import mathutils

from io_scene_warcraft_3 import constants


def create_armature_actions(armatureObject, model, frameTime):
    print("adding animations")
    nodes = model.nodes
    sequences = model.sequences
    action = bpy.data.actions.new(name='#UNANIMATED')
    add_sequence_to_armature('#UNANIMATED', armatureObject)

    action_all = bpy.data.actions.new(name='all sequences')
    add_sequence_to_armature('all sequences', armatureObject)
    timeline_markers = bpy.data.scenes[0].timeline_markers

    for node in nodes:
        add_unanimated_to_bones(action, node)
        add_unanimated_to_bones(action_all, node)

    for sequence in sequences:
        print("adding sequence " + sequence.name)
        intervalStart = sequence.interval_start
        intervalEnd = sequence.interval_end
        action = bpy.data.actions.new(name=sequence.name)
        add_sequence_to_armature(sequence.name, armatureObject)

        intStart = round(intervalStart / frameTime, 0)
        intEnd = round(intervalEnd / frameTime, 0)

        timeline_markers.new(sequence.name, frame=intStart)
        timeline_markers.new(sequence.name, frame=intEnd)

        for node in nodes:
            add_actions_to_bones(action, frameTime, 0, intervalEnd, intervalStart, node, True)
            add_actions_to_bones(action_all, frameTime, intervalStart, intervalEnd, intervalStart, node, False)


def add_unanimated_to_bones(action, node):
    boneName = node.node.name
    dataPath = 'pose.bones["' + boneName + '"]'
    new_fcurve(action, boneName, dataPath + '.location', 0.0)
    new_fcurve(action, boneName, dataPath + '.rotation_euler', 0.0)
    new_fcurve(action, boneName, dataPath + '.scale', 1.0)


def add_actions_to_bones(action, frameTime, sequence_start, intervalEnd, intervalStart, node, is_new_action):
    boneName = node.node.name
    # dataPath = 'pose.bones["' + boneName + '"]'
    translations = node.node.translations
    rotations = node.node.rotations
    scalings = node.node.scalings

    if translations:
        create_transformation_curves(action, boneName, 'location', frameTime, intervalEnd, intervalStart, sequence_start,
                                     translations, 0.0,
                                     lambda translation: translation, is_new_action)
    if rotations:
        create_transformation_curves(action, boneName, 'rotation_euler', frameTime, intervalEnd, intervalStart, sequence_start,
                                     rotations, 0.0,
                                     lambda rotation: (mathutils.Quaternion(mathutils.Vector(rotation)).to_euler('XYZ')), is_new_action)

    if scalings:
        create_transformation_curves(action, boneName, 'scale', frameTime, intervalEnd, intervalStart, sequence_start,
                                     scalings, 1.0,
                                     lambda scaling: scaling, is_new_action)


def create_transformation_curves(action, boneName, data_path_addition, frameTime, intervalEnd, intervalStart, sequence_start,
                                 transformations, transformation_zero_value, value_conversion, is_new_action):
    dataPath = 'pose.bones["' + boneName + '"].' + data_path_addition
    starting_keyframe = round(sequence_start / frameTime, 0)
    interpolationType = constants.INTERPOLATION_TYPE_NAMES[transformations.interpolation_type]

    if is_new_action:
        transformation_fcurves = [None, None, None]
    else:
        current_fcurve = action.fcurves.find(dataPath)
        current_fcurve_index = action.fcurves.values().index(current_fcurve)

        transformation_fcurves = [action.fcurves[current_fcurve_index], action.fcurves[current_fcurve_index + 1],
                                  action.fcurves[current_fcurve_index + 2]]

        # set the keyframe before and after the sequence to T-pose not ge weird
        # transitions between actions in "all sequences" in the case transformation is not set
        trans_zero_values = [transformation_zero_value, transformation_zero_value, transformation_zero_value]
        end_keyframe = round(intervalEnd / frameTime, 0)
        insert_xyz_keyframe_points(interpolationType, transformation_fcurves, starting_keyframe - 1, trans_zero_values)
        insert_xyz_keyframe_points(interpolationType, transformation_fcurves, end_keyframe + 1, trans_zero_values)

    for index in range(transformations.tracks_count):
        time = transformations.times[index]
        transformation = transformations.values[index]
        converted_values = value_conversion(transformation)

        if intervalStart <= time and time <= intervalEnd:

            if time == intervalStart and not is_new_action:
                end_keyframe = round(intervalEnd / frameTime, 0)

                # set the keyframes before and after the sequence to so same as the first keyframe not ge weird
                # transitions between actions in "all sequences"
                insert_xyz_keyframe_points(interpolationType, transformation_fcurves, starting_keyframe - 1,
                                           converted_values)
                insert_xyz_keyframe_points(interpolationType, transformation_fcurves, end_keyframe + 1,
                                           converted_values)

            realTime = round((time + sequence_start - intervalStart) / frameTime, 0)

            transformation_fcurves = set_new_curves(action, boneName, dataPath, transformation_fcurves,
                                                    starting_keyframe)
            insert_xyz_keyframe_points(interpolationType, transformation_fcurves, realTime, converted_values)

    set_new_curves(action, boneName, dataPath, transformation_fcurves, starting_keyframe, transformation_zero_value)


def set_new_curves(action, boneName, dataPath, fcurves, starting_keyframe, value=-1.0):
    for i in range(len(fcurves)):
        if not fcurves[i]:
            try:
                fcurves[i] = action.fcurves.new(dataPath, index=i, action_group=boneName)
                if value != -1.0:
                    fcurves[i].keyframe_points.insert(starting_keyframe, value)
            except:
                print("fcurve did already exist")
    return fcurves


def insert_xyz_keyframe_points(interpolationType, fcurves, realTime, movement):
    for i in range(len(fcurves)):
        keyframe = fcurves[i].keyframe_points.insert(realTime, movement[i])
        keyframe.interpolation = interpolationType


def new_fcurve(action, boneName, dataPath, value):
    try:
        for i in range(3):
            fcurve = action.fcurves.new(dataPath, index=i, action_group=boneName)
            fcurve.keyframe_points.insert(0.0, value)
    except:
        print("fcurve did already exist")


def add_sequence_to_armature(sequenceName, armatureObject):
    warcraft3data = armatureObject.data.warcraft_3
    sequence = warcraft3data.sequencesList.add()
    sequence.name = sequenceName
