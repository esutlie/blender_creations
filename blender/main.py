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
build_mount = False
build_mount2 = False
build_chamber = True
shield = True

# This is for the neuropixel head mount system
if build_mount2:
    initialize_blender()
    mount = HeadMount2()
    mount.pixel()
    # mount.objects.append(mount.pixel())
    mount.objects.append(mount.holder(shield=shield))
    mount.objects.append(mount.cap(shield=shield))
    mount.objects.append(mount.cover(shield=shield))
    # mount.objects.append(mount.stopper())
    # mount.objects.append(mount.stabber())
    # mount.objects.append(mount.surgery())
    # mount.objects.append(mount.tube())
    # mount.objects.append(mount.stand())
    # mount.objects.append(mount.cleaner())
    # mount.objects.append(mount.headfix())

    # This exports the stl files
    if export:
        export_stl(mount)

# This is for the neuropixel head mount system
if build_mount:
    initialize_blender()
    mount = HeadMount()
    # mount.pixel()
    # mount.objects.append(mount.pixel())
    # mount.objects.append(mount.holder())
    mount.objects.append(mount.cap())
    mount.objects.append(mount.cover())
    # mount.objects.append(mount.stopper())
    # mount.objects.append(mount.stabber())
    # mount.objects.append(mount.surgery())
    # mount.objects.append(mount.tube())
    # mount.objects.append(mount.stand())
    # mount.objects.append(mount.cleaner())
    # mount.objects.append(mount.headfix())

    # This exports the stl files
    if export:
        export_stl(mount)

# This is for the chamber
if build_chamber:
    overrider = initialize_blender()
    chamber = Chamber(overrider)
    place_cursor(overrider, [0, chamber.center[1], 0])

    # This builds the components
    # chamber.objects.append(chamber.frame())
    # chamber.objects.append(chamber.base())
    # obj_blank = chamber.port(blank=True)
    obj_port = chamber.port(blank=False)
    # chamber.objects.append(obj_blank)
    # chamber.objects.append(obj_port)
    # chamber.cut_screw_holes(chamber.objects)
    # # chamber.objects.append(chamber.cam_attach())
    # chamber.objects.append(chamber.cam_cover())
    # chamber.objects.append(chamber.cable_cover())
    #
    # # This moves and duplicates the blank port
    # activate([obj_port])
    # bpy.ops.transform.rotate(value=chamber.angle_port, orient_axis='Z', center_override=chamber.center + [0])
    # bpy.ops.object.duplicate()
    # bpy.ops.transform.rotate(value=-2 * chamber.angle_port, orient_axis='Z', center_override=chamber.center + [0])

    # This exports the stl files
    if export:
        export_stl(chamber, scale=10)

if render_anatomy:
    load_skull((1.5, -.7, 0))
