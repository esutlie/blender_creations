import os
import sys
import bpy

directory = os.path.dirname(bpy.data.filepath)
if directory not in sys.path:
    sys.path.append(directory)

import importlib
import helper_functions
import builds

importlib.reload(helper_functions)
importlib.reload(builds)

from helper_functions import *
from builds import *

# /Applications/Blender.app/Contents/MacOS/Blender in terminal to open blender
# On windows, open blender app, then click "window -> toggle system console"

render_anatomy = False
export = True
build_mount2 = True
build_chamber = False
shield = False

# This is for the neuropixel 2 head mount system
if build_mount2:
    initialize_blender()
    # clearance_modifiers = [0, .1, .2, .3, .4, .5, .6]
    # clearance_modifiers = [.2, .3, .35, .4, .5]
    clearance_modifiers = [0]
    for c in clearance_modifiers:
        mount = HeadMount2(clearance_modifier2=c)
        # mount.pixel()
        # mount.objects.append(mount.pixel())
        mount.objects.append(mount.holder(shield=shield, type='holder', name='holder' + str(c)))
        mount.objects.append(mount.cap(shield=shield, name='cap' + str(c)))
        mount.objects.append(mount.cover(shield=shield, name='cover' + str(c)))
        mount.objects.append(mount.hat(name='hat' + str(c)))
        mount.objects.append(mount.holder(shield=shield, type='surgery', name='surgery' + str(c)))
        mount.objects.append(mount.holder(shield=shield, type='stopper', name='stopper' + str(c)))
        # mount.objects.append(mount.holder(shield=shield, type='grinder'))
        tube = mount.tube()
        mount.objects.append(tube[0])
        mount.objects.append(tube[1])
        mount.objects.append(mount.tube(play=True))
        mount.objects.append(mount.stand())
        mount.objects.append(mount.stand(test=False))
        mount.objects.append(mount.cleaner())
        # mount.objects.append(mount.headfix())

        # for clear in [.08, .09, .1, .11, .12]:
        #     mount1 = HeadMount2(cap_clearance=clear)
        #     mount.objects.append(mount1.cover(shield=shield, name='cover' + str(clear)))
        #     mount.objects.append(mount1.cap(shield=shield, name='cap' + str(clear)))
        #
        # for radius, dove_x in zip([.96, .98, .99, 1, 1.01, 1.02], [2.55, 2.58, 2.61, 2.64, 2.67, 2.7]):
        #     mount1 = HeadMount2(DOVE_OUTER_WIDTH=dove_x, holder_screw_radius=radius)
        #     mount.objects.append(
        #         mount1.holder(shield=shield, type='holder', name='holder' + str(radius) + ',' + str(dove_x)))

        # This exports the stl files
        if export:
            export_stl(mount)

# # This is for the neuropixel head mount system
# if build_mount:
#     initialize_blender()
#     mount = HeadMount()
#     # mount.pixel()
#     # mount.objects.append(mount.pixel())
#     # mount.objects.append(mount.holder())
#     # mount.objects.append(mount.cap())
#     # mount.objects.append(mount.cover())
#     # mount.objects.append(mount.stopper())
#     # mount.objects.append(mount.stabber())
#     # mount.objects.append(mount.surgery())
#     # mount.objects.append(mount.tube())
#     # mount.objects.append(mount.stand())
#     # mount.objects.append(mount.cleaner())
#     # mount.objects.append(mount.headfix())
#
#     # This exports the stl files
#     if export:
#         export_stl(mount)

# This is for the chamber
if build_chamber:
    overrider = initialize_blender()
    chamber = Chamber(overrider)
    place_cursor(overrider, [0, chamber.center[1], 0])

    # This builds the components
    chamber.objects.append(chamber.frame())
    chamber.objects.append(chamber.base(flat_side=False, have_floor=False))
    obj_port = chamber.port(blank=False)
    obj_blank = chamber.port(blank=True)
    chamber.objects.append(chamber.blank_tri())
    chamber.objects.append(obj_blank)
    chamber.objects.append(obj_port)
    chamber.objects.append(chamber.tictac())
    chamber.cut_screw_holes(chamber.objects)
    chamber.objects.append(chamber.cam_attach())
    chamber.objects.append(chamber.cam_cover())
    chamber.objects.append(chamber.cable_cover(hole=True))
    chamber.objects.append(chamber.sol_holder(test=False, num=3))

    # This moves and duplicates the blank port
    activate([obj_port])
    bpy.ops.transform.rotate(value=-chamber.angle_port, orient_axis='Z', center_override=chamber.center + [0])
    bpy.ops.object.duplicate()
    bpy.ops.transform.rotate(value=2 * chamber.angle_port, orient_axis='Z', center_override=chamber.center + [0])

    # This exports the stl files
    if export:
        export_stl(chamber, scale=10)

if render_anatomy:
    load_skull((1.5, -.7, 0))
