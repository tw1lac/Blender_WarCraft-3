import bpy
import mathutils

from io_scene_warcraft_3 import constants


def create_armature_actions(armature_object, model, frame_time):
    nodes = model.nodes
    sequences = model.sequences
    action = bpy.data.actions.new(name='#UNANIMATED')
    add_sequence_to_armature('#UNANIMATED', armature_object)

    for node in nodes:
        bone_name = node.node.name
        data_path = 'pose.bones["' + bone_name + '"]'
        new_fcurve(action, bone_name, data_path + '.location', 0.0)
        new_fcurve(action, bone_name, data_path + '.rotation_euler', 0.0)
        new_fcurve(action, bone_name, data_path + '.scale', 1.0)

    for sequence in sequences:
        interval_start = sequence.interval_start
        interval_end = sequence.interval_end
        action = bpy.data.actions.new(name=sequence.name)
        add_sequence_to_armature(sequence.name, armature_object)

        for node in nodes:
            bone_name = node.node.name
            data_path = 'pose.bones["' + bone_name + '"]'
            translations = node.node.translations
            rotations = node.node.rotations
            scalings = node.node.scalings

            if translations:
                pose_bones(action, bone_name, data_path + '.location', frame_time, interval_end, interval_start, translations, 0.0)

            if rotations:
                rotation_fcurves = [None, None, None]
                interpolation_type = constants.INTERPOLATION_TYPE_NAMES[rotations.interpolation_type]

                for index in range(rotations.tracks_count):
                    time = rotations.times[index]
                    rotation = rotations.values[index]
                    euler = mathutils.Quaternion(mathutils.Vector(rotation)).to_euler('XYZ')

                    if interval_start <= time <= interval_end:
                        rotation_fcurves = set_new_curves(action, bone_name, data_path + '.rotation_euler', rotation_fcurves)
                        real_time = round((time - interval_start) / frame_time, 0)

                        insert_xyz_keyframe_points(interpolation_type, rotation_fcurves, real_time, euler)

                set_new_curves(action, bone_name, data_path + '.rotation_euler', rotation_fcurves, 0.0)

            if scalings:
                pose_bones(action, bone_name, data_path + '.scale', frame_time, interval_end, interval_start,
                           scalings, 1.0)


def pose_bones(action, bone_name, data_path, frame_time, interval_end, interval_start, adjustments, value):
    fcurves = [None, None, None]
    interpolation_type = constants.INTERPOLATION_TYPE_NAMES[adjustments.interpolation_type]

    for index in range(adjustments.tracks_count):
        time = adjustments.times[index]
        adjustment = adjustments.values[index]

        if interval_start <= time <= interval_end:
            fcurves = set_new_curves(action, bone_name, data_path, fcurves)
            real_time = round((time - interval_start) / frame_time, 0)

            insert_xyz_keyframe_points(interpolation_type, fcurves, real_time, adjustment)

    set_new_curves(action, bone_name, data_path, fcurves, value)


def set_new_curves(action, bone_name, data_path, fcurves, value=-1.0):
    for i in range(len(fcurves)):
        if not fcurves[i]:
            fcurves[i] = action.fcurves.new(data_path, i, bone_name)
            if value != -1.0:
                fcurves[i].keyframe_points.insert(0.0, value)
    return fcurves


def insert_xyz_keyframe_points(interpolation_type, fcurves, real_time, movement):
    for i in range(len(fcurves)):
        keyframe = fcurves[i].keyframe_points.insert(real_time, movement[i])
        keyframe.interpolation = interpolation_type


def new_fcurve(action, bone_name, data_path, value):
    for i in range(3):
        fcurve = action.fcurves.new(data_path, i, bone_name)
        fcurve.keyframe_points.insert(0.0, value)


def add_sequence_to_armature(sequence_name, armature_object):
    warcraft3data = armature_object.data.warcraft_3
    sequence = warcraft3data.sequencesList.add()
    sequence.name = sequence_name
