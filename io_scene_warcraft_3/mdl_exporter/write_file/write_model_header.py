def write_model_header(fw, model):
    fw("Model \"%s\" {\n" % model.name)
    if len(model.geosets):
        fw("\tNumGeosets %d,\n" % len(model.geosets))
    if len(model.objects['bone']):
        fw("\tNumBones %d,\n" % len(model.objects['bone']))
    if len(model.objects['attachment']):
        fw("\tNumAttachments %d,\n" % len(model.objects['attachment']))
    if len(model.objects['particle']):
        fw("\tNumParticleEmitters %d,\n" % len(model.objects['particle']))
    if len(model.objects['particle2']):
        fw("\tNumParticleEmitters2 %d,\n" % len(model.objects['particle2']))
    if len(model.objects['ribbon']):
        fw("\tNumRibbonEmitters %d,\n" % len(model.objects['ribbon']))
    if len(model.objects['eventobject']):
        fw("\tNumEvents %d,\n" % len(model.objects['eventobject']))
    if len(model.geoset_anims):
        fw("\tNumGeosetAnims %d,\n" % len(model.geoset_anims))
    if len(model.objects['light']):
        fw("\tNumLights %d,\n" % len(model.objects['light']))
    if len(model.objects['helper']):
        fw("\tNumHelpers %d,\n" % len(model.objects['helper']))

    fw("\tBlendTime %d,\n" % 150)
    # fw("\tMinimumExtent {%s, %s, %s},\n" % tuple(map(f2s, model.global_extents_min)))
    # fw("\tMaximumExtent {%s, %s, %s},\n" % tuple(map(f2s, model.global_extents_max)))
    # fw("\tBoundsRadius %s,\n" % f2s(calc_bounds_radius(model.global_extents_min, model.global_extents_max)))
    fw("}\n")
