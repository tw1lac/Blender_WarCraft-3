import bpy
import mathutils
from bpy.types import Object

from io_scene_warcraft_3 import constants
from io_scene_warcraft_3.classes.WarCraft3Model import WarCraft3Model


def create_armature_actions(armature_object: Object, model: WarCraft3Model, frame_time: float):
    print("adding animations")
    nodes = model.nodes
    sequences = model.sequences
    action = bpy.data.actions.new(name='#UNANIMATED')
    add_sequence_to_armature('#UNANIMATED', armature_object)

    action_all = bpy.data.actions.new(name='all sequences')
    add_sequence_to_armature('all sequences', armature_object)
    timeline_markers = bpy.data.scenes[0].timeline_markers

    for node in nodes:
        add_unanimated_to_bones(action, node)
        add_unanimated_to_bones(action_all, node)

    for sequence in sequences:
        print("adding sequence " + sequence.name)
        interval_start = sequence.interval_start
        interval_end = sequence.interval_end
        action = bpy.data.actions.new(name=sequence.name)
        add_sequence_to_armature(sequence.name, armature_object)

        int_start = round(interval_start / frame_time, 0)
        int_end = round(interval_end / frame_time, 0)

        timeline_markers.new(sequence.name, frame=int_start)
        timeline_markers.new(sequence.name, frame=int_end)

        for node in nodes:
            add_actions_to_bones(action, frame_time, 0, interval_end, interval_start, node, True)
            add_actions_to_bones(action_all, frame_time, interval_start, interval_end, interval_start, node, False)


def add_unanimated_to_bones(action, node):
    bone_name = node.node.name
    data_path = 'pose.bones["' + bone_name + '"]'
    new_fcurve(action, bone_name, data_path + '.location', 0.0)
    new_fcurve(action, bone_name, data_path + '.rotation_euler', 0.0)
    new_fcurve(action, bone_name, data_path + '.scale', 1.0)


def add_actions_to_bones(action, frame_time, sequence_start, interval_end, interval_start, node, is_new_action):
    bone_name = node.node.name
    # dataPath = 'pose.bones["' + bone_name + '"]'
    translations = node.node.translations
    rotations = node.node.rotations
    scalings = node.node.scalings

    if translations:
        create_transformation_curves(action, bone_name, 'location', frame_time, interval_end, interval_start, sequence_start,
                                     translations, 0.0,
                                     lambda translation: translation, is_new_action)
    if rotations:
        create_transformation_curves(action, bone_name, 'rotation_euler', frame_time, interval_end, interval_start,
                                     sequence_start, rotations, 0.0,
                                     lambda rotation: (mathutils.Quaternion(mathutils.Vector(rotation)).to_euler('XYZ')), is_new_action)

    if scalings:
        create_transformation_curves(action, bone_name, 'scale', frame_time, interval_end, interval_start, sequence_start,
                                     scalings, 1.0,
                                     lambda scaling: scaling, is_new_action)


def create_transformation_curves(action, bone_name, data_path_addition, frame_time,
                                 interval_end, interval_start, sequence_start,
                                 transformations, transformation_zero_value, value_conversion, is_new_action):
    data_path = 'pose.bones["' + bone_name + '"].' + data_path_addition
    starting_keyframe = round(sequence_start / frame_time, 0)
    interpolation_type = constants.INTERPOLATION_TYPE_NAMES[transformations.interpolation_type]

    if is_new_action:
        transformation_fcurves = [None, None, None]
    else:
        current_fcurve = action.fcurves.find(data_path)
        current_fcurve_index = action.fcurves.values().index(current_fcurve)

        transformation_fcurves = [action.fcurves[current_fcurve_index], action.fcurves[current_fcurve_index + 1],
                                  action.fcurves[current_fcurve_index + 2]]

        # set the keyframe before and after the sequence to T-pose not ge weird
        # transitions between actions in "all sequences" in the case transformation is not set
        trans_zero_values = [transformation_zero_value, transformation_zero_value, transformation_zero_value]
        end_keyframe = round(interval_end / frame_time, 0)
        insert_xyz_keyframe_points(interpolation_type, transformation_fcurves, starting_keyframe - 1, trans_zero_values)
        insert_xyz_keyframe_points(interpolation_type, transformation_fcurves, end_keyframe + 1, trans_zero_values)

    for index in range(transformations.tracks_count):
        time = transformations.times[index]
        transformation = transformations.values[index]
        converted_values = value_conversion(transformation)

        if interval_start <= time <= interval_end:

            if time == interval_start and not is_new_action:
                end_keyframe = round(interval_end / frame_time, 0)

                # set the keyframes before and after the sequence to so same as the first keyframe not ge weird
                # transitions between actions in "all sequences"
                insert_xyz_keyframe_points(interpolation_type, transformation_fcurves, starting_keyframe - 1,
                                           converted_values)
                insert_xyz_keyframe_points(interpolation_type, transformation_fcurves, end_keyframe + 1,
                                           converted_values)

            real_time = round((time + sequence_start - interval_start) / frame_time, 0)

            transformation_fcurves = set_new_curves(action, bone_name, data_path, transformation_fcurves,
                                                    starting_keyframe)
            insert_xyz_keyframe_points(interpolation_type, transformation_fcurves, real_time, converted_values)

    set_new_curves(action, bone_name, data_path, transformation_fcurves, starting_keyframe, transformation_zero_value)


def set_new_curves(action, bone_name, data_path, fcurves, starting_keyframe, value=-1.0):
    for i in range(len(fcurves)):
        if not fcurves[i]:
            fcurves[i] = action.fcurves.new(data_path, index=i, action_group=bone_name)
            if value != -1.0:
                fcurves[i].keyframe_points.insert(starting_keyframe, value)
            # try:
            #     fcurves[i] = action.fcurves.new(data_path, index=i, action_group=bone_name)
            #     if value != -1.0:
            #         fcurves[i].keyframe_points.insert(starting_keyframe, value)
            # except:
            #     print("fcurve did already exist")
    return fcurves


def insert_xyz_keyframe_points(interpolation_type, fcurves, real_time, movement):
    for i in range(len(fcurves)):
        keyframe = fcurves[i].keyframe_points.insert(real_time, movement[i])
        keyframe.interpolation = interpolation_type


def new_fcurve(action, bone_name, data_path, value):
    for i in range(3):
        fcurve = action.fcurves.new(data_path, index=i, action_group=bone_name)
        fcurve.keyframe_points.insert(0.0, value)
    # try:
    #     for i in range(3):
    #         fcurve = action.fcurves.new(data_path, index=i, action_group=bone_name)
    #         fcurve.keyframe_points.insert(0.0, value)
    # except:
    #     print("fcurve did already exist")


def add_sequence_to_armature(sequence_name, armature_object):
    warcraft3data = armature_object.data.warcraft_3
    sequence = warcraft3data.sequencesList.add()
    sequence.name = sequence_name
