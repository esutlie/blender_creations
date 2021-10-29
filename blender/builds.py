"""piece builders for blender 2.8"""

import bpy
from math import tan, sqrt, floor
from helper_functions import *
import numpy as np

INF = [100, -100]
INF_POS = [100, 0]
INF_NEG = [0, -100]


# __all__ = [
#     "HeadMount",
#     "HeadMount2",
#     "Chamber"
# ]


class HeadMount2:
    def __init__(self, cap_clearance=.08, DOVE_OUTER_WIDTH=2.7, holder_screw_radius=1):
        self.objects = []

        # This: pixel settings
        self.PIXEL_TOP = [7, 1.6, 7]
        self.PIXEL_BOTTOM = [5, 1.5, 6]  # Increased from [4, 1.5, 6]
        self.PIXEL_PROBE = [.75, .024, 10]
        self.PIXEL_PROBE_Y = .2  # Pretty sure this is the right number, hopefully the same across probes
        self.PIXEL_X_OFFSET = .1  # works at least for the probe I'm using
        # self.DOVE_OUTER_WIDTH = 2.2
        # self.DOVE_DEPTH = .9
        # self.DOVE_ANGLE = 45
        self.DOVE_OUTER_WIDTH = 2.6  # 2.8, 2.78 are too large, 2.7 is too small
        self.DOVE_DEPTH = .75
        self.DOVE_ANGLE = 59 * pi / 180
        self.DOVE_INNER_WIDTH = self.DOVE_OUTER_WIDTH - 2 * self.DOVE_DEPTH / tan(self.DOVE_ANGLE)
        self.DOVE_Z_SPACER = .5
        self.DOVE_HEIGHT = 8.1

        # This: Major screw sizes
        self.SCREWHEAD_LOWER_RADIUS = 1.15
        self.SCREWHEAD_DEPTH = 1
        self.SCREWHEAD_UPPER_RADIUS = self.SCREWHEAD_DEPTH + self.SCREWHEAD_LOWER_RADIUS + .1
        self.SCREW_THREAD_RADIUS = 1.05
        self.DRIVER_WIDTH = 3
        self.SCREW_LENGTH = 16

        # clearance for cap should .11
        # clearance for cover should be .15
        self.cap_clearance = .08
        # self.cap_clearance = .15  # was .13
        # self.cover_clearance = .18  # was .16
        self.cover_clearance = .08

        self.protrusion = 5
        self.hex_radius = 2.4

        self.lip_height = 1
        self.lip_outer_radius = .9
        self.lip_inner_radius = .6

        self.squeezer_bump_size = .8
        self.squeezer_z_shape = [1, 1.2, 1.2, 5]
        self.squeezer_width = 5
        self.squeezer_thickness = .1
        # self.squeezer_clearance = clearance
        self.squeezer_handle_gap = 1
        self.squeezer_handle_thickness = 2
        self.squeezer_handle_length = 14
        self.squeezer_bottom_thickness = 2
        self.squeezer_rotate_center = 7
        self.squeeze_length = 15

        self.squeezer_handle_size = [self.squeezer_width, 100, self.squeezer_width]
        self.holder_clearance = .1

        # holder settings
        self.holder_space_below_dove = 2
        self.holder_height = self.PIXEL_BOTTOM[2] + self.holder_space_below_dove - self.DOVE_Z_SPACER
        self.holder_y_extension = 1
        self.holder_wall_thickness = 1
        self.holder_inner_wall_thickness = .5
        self.holder_screw_radius = self.SCREW_THREAD_RADIUS

        self.dove2_width = 2
        # self.dove2_width = 2.95
        self.dove2_depth = 1
        # self.dove2_clearance = self.cap_clearance  # should be .13

        holder_x = self.PIXEL_BOTTOM[0] + 2 * self.holder_wall_thickness + 2 * self.holder_clearance
        holder_y = self.holder_y_extension + self.PIXEL_BOTTOM[1] + self.DOVE_DEPTH + \
                   self.holder_inner_wall_thickness + self.dove2_depth
        self.holder_size = [holder_x, holder_y, self.holder_height]

        self.pixel_xyz = [0, 0, self.PIXEL_PROBE[2] - self.protrusion - self.lip_height]
        self.holder_xyz = [0, -self.PIXEL_PROBE_Y - self.holder_y_extension,
                           self.pixel_xyz[2] + self.DOVE_Z_SPACER - self.holder_space_below_dove]

        self.handle_size = [self.hex_radius * 2 + .5, 4.5, 3]
        # self.handle_size = [5.9, 4.5, 3]  #old params with hex

        # cap settings
        self.cap_wall_thickness = .8
        # self.cap_top_extention = 0
        self.cap_top_extention = 1.5
        self.cap_size = list(map(lambda x: x + 2 * (self.cap_wall_thickness + self.cap_clearance), self.holder_size))
        self.cap_size[2] = self.holder_xyz[2] + self.holder_size[2] + self.cap_top_extention
        self.cap_bottom_thickness = 1.5
        self.cap_bottom_lip = .7
        self.cap_window_width = 1
        self.cap_window_base_thickness = self.cap_bottom_thickness + .001

        self.head_fix_size = [18, 2, 2]
        # self.head_fix_dims = [4, 2, 2]
        self.head_fix_cylinder_radius = .7
        self.headfix_bar_z = 1.5

        self.cap_bottom_bevel = 2
        self.ground_wire_depth = .5
        self.ground_wire_x = self.cap_size[0] / 2 - 3
        self.wire_location = [-self.ground_wire_x, -self.cap_size[1] / 2 + .01, self.cap_size[2] / 2]
        self.plug_width = 1
        self.plug_depth = 2
        self.plug_wall = .5

        # cover settings
        self.headstage_size = [17, 3, 12]
        self.cover_thickness = 1.3
        self.cover_squeezer_clearance = .7
        self.cover_holder_space = self.holder_size[2]
        self.cover_lip_depth = 1.5
        self.screw_hole_radius = .6  # for self-tapping
        self.screw_hole_x_offset = 6.7
        self.screw_hole_z_offset = 7.5
        self.flex_space = 2
        self.cover_midsection_x = 5

        self.hex_location = [0, self.holder_size[1] / 2 + self.holder_xyz[1], self.cap_size[2] - self.hex_radius]
        self.hex_cut_depth = 1.7
        self.screw_divot_depth = .5
        self.screw_divot_radius = 1.1
        self.base_bevel = .5

        self.secure_screw_location = [0, self.holder_size[1] / 2 + self.holder_xyz[1],
                                      self.cap_size[2] - self.SCREW_THREAD_RADIUS - self.cover_thickness]
        self.cover_overhang = 2 * (self.SCREW_THREAD_RADIUS + self.cover_thickness)
        self.cover_size = [self.cap_size[0] + 2 * self.cover_thickness,
                           self.cap_size[1] + 2 * self.cover_thickness,
                           self.cover_thickness + self.holder_size[2] + self.cover_overhang]
        self.cover_move_z = self.cover_thickness - self.cover_size[2] / 2 + self.cover_holder_space + \
                            self.cap_size[2] + self.cover_clearance
        self.cover_xyz = [0, self.holder_size[1] / 2 + self.cover_clearance + self.holder_xyz[1],
                          -self.cover_size[2] / 2 + self.cover_thickness + 2 * self.holder_size[2] +
                          self.holder_xyz[2] + self.cap_top_extention]
                          # self.cover_clearance + self.holder_xyz[2] + self.cap_top_extention]

        self.tracking_cylinder_radius = 2
        self.bevel_offset = 1
        self.screwhead_top = .15  # was .35
        self.extra_side_screw = .8

        # headfix paramaters
        self.bridge_thickness = 5
        self.bridge_y = 10
        self.headfix_clearance = .4
        self.bridge_width = self.cap_size[0] + 3 * self.headfix_clearance
        self.headfix_thickness = 3
        self.headfix_inner_bevel = 2
        self.headfix_outer_bevel = sqrt(3 ** 2 / 2)
        self.stereotax_bevel = 2 * sqrt(1 ** 2 / 2)
        self.headfix_screw_radius = 1.1
        self.stereotax_width = 44
        self.stereotax_bar_thickness = 4.3
        self.stereotax_bar_length = 20

        self.headfix_bar_slant = 10  # degrees

        self.screw_y = 5 / 2 + self.DOVE_DEPTH + self.PIXEL_BOTTOM[1] - self.PIXEL_PROBE_Y
        # self.SCREWHEAD_LOWER_RADIUS = 1.15
        # self.SCREWHEAD_DEPTH = 1
        # self.SCREWHEAD_UPPER_RADIUS = self.SCREWHEAD_DEPTH + self.SCREWHEAD_LOWER_RADIUS + .1
        # self.SCREW_THREAD_RADIUS = 1.05
        # self.DRIVER_WIDTH = 3
        # self.SCREW_LENGTH = 16.5

        self.screw_cover_size = [self.cover_midsection_x + self.cover_thickness, self.SCREWHEAD_UPPER_RADIUS + 2.5, 1]
        self.screw_cover_location = [0, self.screw_y,
                                     self.screw_cover_size[2] / 2 + self.cover_thickness + self.cover_holder_space +
                                     self.cap_size[2] + self.cover_clearance + self.cover_clearance]

        self.surgery_post_separation = 4
        self.post_diameter = .82  # 21 gauge
        self.needle_diameter = .45  # 26 gauge

        # This defines everything for the stand
        self.stand_thickness = 2
        self.inset = 1
        self.stand_ridge = .6

        self.eppendorf_height = 30
        self.stand_cover_depth = 6
        self.stand_extra_lower_distance = 2.5  # should be tuned for how far the screw extends down
        self.stand_front = 3
        self.stand_size = [self.cover_size[0] + self.stand_thickness * 2,
                           self.cover_size[1] + self.stand_thickness * 2 + self.cover_thickness + self.stand_front,
                           self.eppendorf_height + self.stand_cover_depth + self.stand_extra_lower_distance + 10]
        self.stand_clearance = .2
        self.cleaner_clearance = .35
        self.base_width = 30
        self.base_thickness = 3
        self.stand_base_size = [self.stand_size[0] + 2 * self.base_width,
                                self.stand_size[1] + 2 * self.base_width - self.stand_front, self.base_thickness]
        self.stand_lid_size = [self.stand_base_size[0] - 2 * self.base_thickness,
                               self.stand_base_size[1] - 2 * self.base_thickness,
                               self.stand_size[2] + 2 * self.cover_size[2]]
        self.stand_lid_thickness = 1

        self.cleaner_thickness = 1.5
        self.eppendorf_tube_diameter = 8
        self.hex_depth = 2
        self.added_cleaner_space = 1

        # This is all the extra stuff

        self.dove_bevel = .2
        self.pixel_dove_bevel = .1

        self.shield_thickness = .7

        self.ground_pin_loc = [-2.5, -4.3, 0]
        self.ground_inner_radius = .5
        self.ground_outer_radius = .6
        self.ground_cap_radius = .9

    def pixel(self):
        # This makes the object
        pixel = add_cube(self.PIXEL_TOP, [0, 0, 0], 'pixel')
        for side in [INF_POS, INF_NEG]:
            select_verts(pixel, side, INF, INF_NEG)
            bevel((self.PIXEL_TOP[0] - self.PIXEL_BOTTOM[0]) / 2 - .01)
        mode('OBJECT')
        translate([0, 0, self.PIXEL_TOP[2] / 2 + self.PIXEL_BOTTOM[2] - .01])
        pixel_bot = add_cube(self.PIXEL_BOTTOM, [0, 0, 0], 'pixel_bot')
        translate([0, 0, self.PIXEL_BOTTOM[2] / 2 - .005])
        probe = add_cube(self.PIXEL_PROBE, (self.PIXEL_X_OFFSET, 0, 0), 'probe')
        translate([0, 0, -self.PIXEL_PROBE[2] / 2])
        dove = add_cube([self.DOVE_OUTER_WIDTH, self.DOVE_DEPTH, self.DOVE_HEIGHT], (0, 0, 0), 'dove')
        translate([0, (self.PIXEL_BOTTOM[1] + self.DOVE_DEPTH) / 2 - .001,
                   self.DOVE_Z_SPACER + self.DOVE_HEIGHT / 2])
        select_verts(dove, INF, INF_NEG, INF)
        resize([self.DOVE_INNER_WIDTH / self.DOVE_OUTER_WIDTH, 1, 1])
        mode('OBJECT')

        boolean_modifier(pixel, pixel_bot, modifier='UNION')
        boolean_modifier(pixel, dove, modifier='UNION')
        translate([0, self.PIXEL_BOTTOM[1] / 2 - self.PIXEL_PROBE_Y, 0])
        boolean_modifier(pixel, probe, modifier='UNION')
        delete([pixel_bot, probe, dove])

        activate([pixel])
        translate(self.pixel_xyz)
        return pixel

    def holder(self, shield=False, type='holder', name='holder'):
        # This makes the piece that permanently attaches to the pixel
        holder_location = [0, self.holder_size[1] / 2, self.holder_size[2] / 2]
        holder = add_cube(self.holder_size, holder_location, type)
        for x in [[0, 100], [-100, 0]]:
            select_verts(holder, x, [self.holder_size[1], 100], [-100, 100])
            bpy.ops.mesh.bevel(offset=self.bevel_offset, segments=10)
        bpy.ops.object.mode_set(mode='OBJECT')

        # This makes the cap dovetail
        dove2_size = [self.dove2_width, self.dove2_depth, self.holder_size[2] + 5]
        dove2_location = [0, self.holder_size[1] - dove2_size[1] / 2 + .001,
                          self.holder_size[2] / 2 - self.holder_wall_thickness]
        cap_dovetail = add_cube(dove2_size, dove2_location, 'cap_dovetail')
        select_verts(cap_dovetail, [-dove2_size[0] / 2, dove2_size[0] / 2], [0, dove2_location[1]], [-100, 100])
        ratio = 1 + 2 * dove2_size[1] / sqrt(3) / dove2_size[0]
        bpy.ops.transform.resize(value=(ratio, 1, 1))
        boolean_modifier(holder, cap_dovetail)
        select_verts(holder, [-self.dove2_width / 2, self.dove2_width / 2], [self.holder_size[1], 100], [-100, 100])
        bpy.ops.mesh.bevel(offset=self.dove_bevel, segments=1)
        delete([cap_dovetail])

        activate([holder])
        select_verts(holder, [-ratio * dove2_size[0] / 2, ratio * dove2_size[0] / 2],
                     [self.holder_size[1] - dove2_size[1], 100], [-100, 0])
        bpy.ops.mesh.bevel(offset=self.base_bevel, segments=1)
        mode('OBJECT')

        if type == 'holder':
            # This makes the dovetail cutout
            cutter_size = [self.PIXEL_BOTTOM[0] + 2 * self.holder_clearance,
                           self.PIXEL_BOTTOM[1] + self.holder_y_extension,
                           20]
            dovetail = [self.DOVE_INNER_WIDTH, self.DOVE_DEPTH, 10]
            xyz_location = [0, cutter_size[1] / 2 - .001,
                            dovetail[2] / 2 + self.holder_space_below_dove - self.holder_clearance]
            cutter = add_cube(cutter_size, xyz_location, 'cutter')
            select_verts(cutter, [-100, 100], [0, 100], [-100, 100])
            bpy.ops.mesh.extrude_region()
            ratio = list(map(lambda x, y: x / y, dovetail, cutter_size))
            bpy.ops.transform.resize(value=(ratio[0], 1, ratio[2]))
            bpy.ops.mesh.extrude_context_move(TRANSFORM_OT_translate={"value": (0, dovetail[1], 0)})
            bpy.ops.transform.resize(value=(self.DOVE_OUTER_WIDTH / self.DOVE_INNER_WIDTH, 1, 1))
            for side in [1, -1]:
                select_verts(cutter, [side * dovetail[0] / 2, 0], [0, 100], [-100, 100])
                bpy.ops.mesh.bevel(offset=self.pixel_dove_bevel, segments=1)
            boolean_modifier(holder, cutter)
            delete([cutter])

            # This makes the handle piece
            # handle_size = [self.handle_width, self.handle_length, self.handle_thickness]
            handle_location = [0, self.handle_size[1] / 2 + cutter_size[1] + dovetail[1] + .001,
                               self.holder_size[2] - self.handle_size[2] / 2 - .001]
            handle = add_cube(self.handle_size, (0, 0, 0), 'handle')
            for side in [1, -1]:
                select_verts(handle, [side * 100, 0], [0, 100], [-100, 100])
                bpy.ops.mesh.bevel(offset=1.3, segments=1)

            mode(('OBJECT'))
            translate(handle_location)
            boolean_modifier(holder, handle, modifier='UNION')
            delete([handle])

            # This makes the cutout for the hex
            hex_location = [0, 5 / 2 + cutter_size[1] + dovetail[1] + .001,
                            self.holder_size[2] - self.handle_size[2] / 2 - .001]
            # hex_location = [0, self.screw_y-self.holder_xyz[1],
            #                 self.holder_size[2] - handle_size[2] / 2 - .001]
            hex_cut = add_cylinder(self.hex_radius, self.hex_cut_depth, 6, 'hex_cut')
            translate(hex_location)
            rotate(pi / 6, 'Z')
            select_verts(hex_cut, INF, [-100, -self.hex_radius], INF)
            translate((-self.hex_radius, 0, 0))
            mode('OBJECT')
            rotate(pi, 'Z')
            boolean_modifier(holder, hex_cut)
            delete([hex_cut])

            # This makes the cutout for the screw to come through
            screw_location = [0, 5 / 2 + cutter_size[1] + dovetail[1] + .001,
                              self.holder_size[2] - self.handle_size[2] / 2 - .001]
            bpy.ops.mesh.primitive_cylinder_add(radius=self.holder_screw_radius, depth=self.SCREW_LENGTH,
                                                location=screw_location)
            screw_cut = bpy.context.active_object
            boolean_modifier(holder, screw_cut)
            delete([screw_cut])

        elif type == 'surgery':
            # This makes the needle cut pieces
            cut_size = [self.holder_size[0] + 1, self.holder_xyz[1] * 2, self.holder_size[2] + 1]
            cut_location = [0, 0, self.holder_size[2] / 2]
            cut = add_cube(cut_size, cut_location, 'cut')
            boolean_modifier(holder, cut, fast_solver=True)
            delete([cut])

            post_size = [self.post_diameter, self.post_diameter, self.holder_size[2] + 1]
            post_location = [0, 0, self.holder_size[2] / 2]
            post = add_cube(post_size, post_location, 'post')
            bpy.ops.transform.rotate(value=pi / 4, orient_axis='Z')
            bpy.ops.transform.translate(value=[self.surgery_post_separation / 2, -self.holder_xyz[1] + .001, 0])
            boolean_modifier(holder, post)
            activate([post])
            bpy.ops.transform.translate(value=[-self.surgery_post_separation, 0, 0])
            boolean_modifier(holder, post)
            delete([post])

            needle_size = [self.needle_diameter, self.needle_diameter, self.holder_size[2] + 1]
            needle_location = [0, 0, self.holder_size[2] / 2]
            needle = add_cube(needle_size, needle_location, 'needle')
            bpy.ops.transform.rotate(value=pi / 4, orient_axis='Z')
            bpy.ops.transform.translate(value=[self.PIXEL_X_OFFSET, -self.holder_xyz[1] + .001, 0])
            boolean_modifier(holder, needle)
            delete([needle])
        if type == 'stopper':
            # This makes the cutout for the securing hex nut
            embed_depth = self.holder_size[2] / 2
            bpy.ops.mesh.primitive_cylinder_add(radius=self.hex_radius, depth=self.hex_depth, vertices=6,
                                                location=(0, 0, self.holder_size[2] - embed_depth))
            hex_cut = bpy.context.active_object
            bpy.ops.transform.rotate(value=pi / 6, orient_axis='Z')
            hex_y = (self.holder_size[1] - self.dove2_depth) / 2
            bpy.ops.transform.translate(value=(0, hex_y, 0))
            select_verts(hex_cut, [-100, 100], [-100, -self.hex_radius], [-100, 100])
            translate((-self.hex_radius, 0, 0))
            boolean_modifier(holder, hex_cut)
            delete([hex_cut])

            # This makes the cutout for the screw to come through
            loc = (0, hex_y, self.SCREW_LENGTH / 2 + self.holder_size[2] - embed_depth)
            bpy.ops.mesh.primitive_cylinder_add(radius=self.SCREW_THREAD_RADIUS, depth=self.SCREW_LENGTH, location=loc)
            screw_cut = bpy.context.active_object
            boolean_modifier(holder, screw_cut)
            delete([screw_cut])

        activate([holder])
        bpy.ops.transform.translate(value=self.holder_xyz)

        if shield:
            self.add_shield(holder, num_shield=2)

        return holder

    def cap(self, shield=False, name='cap'):
        # This makes the head cap that is permanently cemented to the skull
        cap_location = [0, 0, self.cap_size[2] / 2]
        cap = add_cube(self.cap_size, cap_location, name)

        # This bevels the back corners
        for side in [-1, 1]:
            select_verts(cap, [0, side * 100], [-100, 100], [-100, 0])
            bpy.ops.mesh.bevel(offset=self.cap_bottom_bevel, segments=1)
            select_verts(cap, [0, side * 100], [0, 100], [-100, 100])
            bpy.ops.mesh.bevel(offset=1, segments=1)

        select_verts(cap, [-100, 100], [0, 100], [-100, 0])
        bpy.ops.mesh.bevel(offset=1.5, segments=1)

        bpy.ops.object.mode_set(mode='OBJECT')

        # This makes the head fixation piece
        head_fix_size = self.head_fix_size
        head_fix_location = [0, 0, head_fix_size[2] / 2 + .001 + self.headfix_bar_z]
        head_fix = add_cube(head_fix_size, head_fix_location, 'head_fix')
        select_verts(head_fix, [-100, 100], [0, -100], [head_fix_location[2], 100])
        bpy.ops.mesh.bevel(offset=self.stereotax_bevel, affect='VERTICES')

        bpy.ops.object.mode_set(mode='OBJECT')

        # This makes the mid section cutout
        hole_size = list(map(lambda x: x + 2 * self.cap_clearance, self.holder_size))
        hole_size[2] += self.cap_top_extention

        hole_location = [0, 0, hole_size[2] / 2 + self.cap_size[2] - hole_size[2] + self.cap_clearance]
        hole = add_cube(hole_size, hole_location, 'hole')
        for x in [[0, 100], [-100, 0]]:
            select_verts(hole, x, [0, 100], [-100, 100])
            bpy.ops.mesh.bevel(offset=self.bevel_offset, segments=10)
        bpy.ops.object.mode_set(mode='OBJECT')

        clear_size = list(map(lambda x: x - 2 * self.cap_bottom_lip, self.holder_size))
        clear_location = [0, 0, clear_size[2] / 2 + self.cap_bottom_thickness]
        clear = add_cube(clear_size, clear_location, 'clear')

        # This makes the cylinders
        bpy.ops.mesh.primitive_cylinder_add(radius=self.lip_outer_radius, depth=self.lip_height,
                                            location=(self.PIXEL_X_OFFSET, 0, -self.lip_height / 2 + .001))
        outer_lip = bpy.context.active_object
        oval_amount = .3
        resize([1 + oval_amount * self.lip_inner_radius / self.lip_outer_radius, 1, 1])
        bpy.ops.mesh.primitive_cylinder_add(radius=self.lip_inner_radius, depth=15,
                                            location=(self.PIXEL_X_OFFSET, 0, 0))
        inner_lip = bpy.context.active_object
        resize([1 + oval_amount, 1, 1])

        # This makes the cap dovetail
        dove2_size = [self.dove2_width - 2 * self.cap_clearance, self.dove2_depth - self.cap_clearance,
                      self.holder_size[2]]
        dove2_location = [0, self.holder_size[1] - dove2_size[1] / 2 + .001,
                          self.holder_size[2] / 2 - self.holder_wall_thickness]
        dove2_location = [x + y for x, y in zip(dove2_location, self.holder_xyz)]
        cap_dovetail = add_cube(dove2_size, dove2_location, 'cap_dovetail')
        select_verts(cap_dovetail, [-dove2_size[0] / 2, dove2_size[0] / 2], [0, dove2_location[1]], [-100, 100])
        ratio = 1 + 2 * dove2_size[1] / sqrt(3) / dove2_size[0]
        bpy.ops.transform.resize(value=(ratio, 1, 1))
        bpy.ops.mesh.bevel(offset=self.dove_bevel, segments=1)
        select_verts(cap_dovetail, [-100, 100], [dove2_location[1], 100], [-100, 100])
        bpy.ops.mesh.extrude_context_move(TRANSFORM_OT_translate={"value": (0, self.cap_wall_thickness, 0)})
        ratio = 1 + 2 * self.cap_wall_thickness / sqrt(3) / dove2_size[0]
        bpy.ops.transform.resize(value=(ratio, 1, 1))
        select_verts(cap_dovetail, [-dove2_size[0] / 2, dove2_size[0] / 2], [0, dove2_location[1]], [-100, 100])

        bpy.ops.object.mode_set(mode='OBJECT')

        # This makes the cut away window rectangle
        window_size = [self.cap_window_width,
                       self.cap_wall_thickness + self.cap_bottom_lip + self.cap_clearance + .2,
                       self.cap_size[2]]
        window_location = [self.PIXEL_X_OFFSET, -self.cap_size[1] / 2 + window_size[1] / 2 - .001,
                           self.cap_size[2] / 2 + self.cap_window_base_thickness]
        window = add_cube(window_size, window_location, 'window')

        # This makes the cutout for the securing hex screw
        oval_amount = 1.1
        bpy.ops.mesh.primitive_cylinder_add(radius=self.screw_divot_radius, depth=self.screw_divot_depth + .001,
                                            location=(0, 0, 0), rotation=(0, pi / 2, 0))
        divot_cut1 = bpy.context.active_object
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        select_verts(divot_cut1, [-100, 0], [-100, 100], [-100, 100])
        bpy.ops.transform.resize(value=(1, .8, .8))
        bpy.ops.object.mode_set(mode='OBJECT')
        resize((1, 1, oval_amount))
        bpy.ops.transform.translate(value=(self.cap_size[0] / 2 - self.screw_divot_depth / 2, 0, 0))
        bpy.ops.transform.translate(value=(self.hex_location))

        bpy.ops.mesh.primitive_cylinder_add(radius=self.screw_divot_radius, depth=self.screw_divot_depth + .001,
                                            location=(0, 0, 0), rotation=(0, pi / 2, 0))
        divot_cut2 = bpy.context.active_object
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        select_verts(divot_cut2, [0, 100], [-100, 100], [-100, 100])
        bpy.ops.transform.resize(value=(1, .8, .8))
        bpy.ops.object.mode_set(mode='OBJECT')
        resize((1, 1, oval_amount))
        bpy.ops.transform.translate(value=(-self.cap_size[0] / 2 + self.screw_divot_depth / 2, 0, 0))
        bpy.ops.transform.translate(value=(self.hex_location))

        # This makes the cutaway for the back where the holder hex sinks in
        handle_size = [self.handle_size[0] + self.cap_clearance * 4, 2 * self.handle_size[1],
                       self.handle_size[2] + self.cap_clearance * 2 + self.cap_top_extention]
        handle_location = [0, handle_size[1] / 2, self.cap_size[2] - handle_size[2] / 2 + self.cap_clearance]
        handle_cut = add_cube(handle_size, handle_location, 'handle_cut')

        loc = [0, self.screw_y, self.cover_size[2] / 2 + self.cover_move_z - self.SCREW_LENGTH / 2]
        bpy.ops.mesh.primitive_cylinder_add(radius=self.SCREW_THREAD_RADIUS + .1, depth=self.SCREW_LENGTH,
                                            location=loc, rotation=(0, 0, 0))
        screw_cut = bpy.context.active_object

        # # This makes the cut out for the screws to secure the cover
        # cover_screw = add_cylinder(self.SCREW_THREAD_RADIUS, self.cap_size[0] * 1.1, 100, 'cover_screw')
        # rotate(pi / 2, 'Y')
        # translate(self.hex_location)

        # This makes the cut out for the screws to secure the cover
        depth = self.cover_size[0] + self.hex_depth * 2
        bpy.ops.mesh.primitive_cylinder_add(radius=self.SCREW_THREAD_RADIUS,  # * 1.3,
                                            depth=depth,
                                            location=self.hex_location, rotation=(0, pi / 2, 0))
        hex_screw = bpy.context.active_object

        # This applies boolean modifiers, deletes, and translates
        boolean_modifier(cap, head_fix, modifier='UNION')
        boolean_modifier(cap, hole)
        boolean_modifier(cap, clear)
        boolean_modifier(cap, window)

        bpy.ops.transform.translate(value=(0, hole_size[1] / 2 + self.holder_xyz[1] - self.cap_clearance, 0))

        boolean_modifier(cap, outer_lip, modifier='UNION')
        boolean_modifier(cap, inner_lip)
        boolean_modifier(cap, cap_dovetail, modifier='UNION')

        boolean_modifier(cap, handle_cut)
        boolean_modifier(cap, screw_cut)
        # boolean_modifier(cap, ground)
        offset = self.cap_size[1] / 6
        for side in [1, -2]:
            activate([hex_screw])
            translate([side * depth / 2, side * offset, 0])
            boolean_modifier(cap, hex_screw)

        delete([head_fix, hole, clear, outer_lip, inner_lip, screw_cut, hex_screw,
                cap_dovetail, window, divot_cut1, divot_cut2, handle_cut])

        if shield:
            self.add_shield(cap, num_shield=2)

        return cap

    def cover(self, shield=False, name='cover'):
        # This makes the piece that holds the headstage and goes around the head cap
        cover = add_cube(self.cover_size, [0, 0, 0], name)

        # This adds thickness to the walls for the affixing screws so they don't go in to far
        depth = self.cover_size[0] / 2 + self.extra_side_screw
        size = [depth, 4, self.cover_size[2] - 1]
        screw_thickness = add_cube(size, (0, self.hex_location[1] - self.cover_xyz[1], 0), 'screw_thickness')
        offset = self.cap_size[1] / 6
        for side in [1, -2]:
            activate([screw_thickness])
            translate([side * depth / 2, side * offset, 0])
            boolean_modifier(cover, screw_thickness, modifier='UNION')
        delete([screw_thickness])

        # This makes the midsection cutter
        midsection_size = [self.handle_size[0] + 2 * self.cover_clearance, self.cover_size[1], self.cover_size[2]]
        midsection_location = [0, self.cover_thickness, -self.cover_thickness - .001]
        midsection = add_cube(midsection_size, midsection_location, 'midsection')
        boolean_modifier(cover, midsection)
        delete([midsection])

        # This makes the cap cutter
        size = list(map(lambda x: x + 2 * self.cover_clearance, self.cap_size))
        cap_cutter_location = [0, self.cover_size[1] / 2 - size[1] / 2 - self.cover_thickness,
                               self.cover_size[2] / 2 - size[
                                   2] / 2 - self.cover_thickness - self.cover_holder_space]
        cap_cutter = add_cube(size, cap_cutter_location, 'cap_cutter')

        boolean_modifier(cover, cap_cutter)
        delete([cap_cutter])

        # This makes the holder cutter
        size = list(map(lambda x: x + 2 * self.cover_clearance, self.holder_size))
        holder_cutter_location = [0, cap_cutter_location[1],
                                  self.cover_size[2] / 2 - size[2] / 2 - self.cover_thickness]
        holder_cutter = add_cube(size, holder_cutter_location, 'holder_cutter')
        for x in [[0, 100], [-100, 0]]:
            select_verts(holder_cutter, x, [cap_cutter_location[1], 100], [-100, 100])
            bpy.ops.mesh.bevel(offset=self.bevel_offset, segments=10)
        bpy.ops.object.mode_set(mode='OBJECT')

        boolean_modifier(cover, holder_cutter)
        delete([holder_cutter])

        # This makes the cut away blocks
        cut = [(self.cover_size[0] - self.holder_size[0]) / 2 - self.cover_thickness,
               self.cover_size[1] - 2 * self.cover_thickness - self.headstage_size[1],
               self.cover_holder_space]
        r1_location = list(map(lambda x, y: x - y, self.cover_size, cut))
        r1_location[1] = 0
        r1_size = [self.cover_size[0], self.cover_size[1] + 1, self.cover_size[2]]
        cut_away_r1 = add_cube(r1_size, (0, 0, 0), 'cut_away_r1')
        translate(r1_location)
        select_verts(cut_away_r1, INF, INF, INF_NEG)
        extrude_move([0, 0, -self.cover_size[0] / 2])
        resize([.01, 1, 1])

        # select_verts(cut_away_r1, [-100, r1_location[0]], [-100, 100], [-100, r1_location[2]])
        # offset = (self.cap_size[0] - self.holder_size[0]) / 2 + .1
        # bpy.ops.mesh.bevel(offset=offset)
        # select_verts(cut_away_r1, [r1_location[0], 100], [-100, 100], [-100, r1_location[2]])
        # bpy.ops.mesh.bevel(offset=offset)

        boolean_modifier(cover, cut_away_r1)
        activate([cut_away_r1])
        bpy.ops.transform.translate(value=(-2 * r1_location[0], .001, 0))
        boolean_modifier(cover, cut_away_r1)
        delete([cut_away_r1])

        # This makes the bottom bevel
        activate([cover])
        select_verts(cover,
                     [-self.cap_size[0] / 2 - self.cover_clearance, self.cap_size[0] / 2 + self.cover_clearance],
                     [-self.cover_size[1] / 2 + self.cover_thickness / 2,
                      self.cover_size[1] / 2 - self.cover_thickness / 2],
                     [-100, -self.cover_size[2] / 2])
        bpy.ops.mesh.bevel(offset=self.base_bevel, segments=1)
        bpy.ops.object.mode_set(mode='OBJECT')

        # This makes the headstage mount
        z_separation = 1
        y_separation = 1
        mount_size = [self.holder_size[0] + self.cover_thickness * 2, self.cover_thickness, self.headstage_size[2]]
        mount_location = [0, -self.cover_size[1] / 2 - mount_size[1] / 2 + self.cover_thickness - y_separation,
                          self.cover_size[2] / 2 + mount_size[2] / 2 + z_separation - .001]
        mount = add_cube(mount_size, (0, 0, 0), 'mount')
        translate(mount_location)
        select_verts(mount, [-100, 100], [-100, 100], [-100, 0])
        extrude_move((0, y_separation, -z_separation))
        resize((1, (self.cover_thickness + z_separation) / self.cover_thickness, 1))
        translate((0, z_separation / 2, 0))
        select_verts(mount, INF, [-100, -mount_size[1] / 2 + y_separation], [-100, -mount_size[2] / 2 - z_separation])
        translate([0, 0, -5])
        boolean_modifier(cover, mount, modifier='UNION')
        delete([mount])

        # # This makes the headstage mount
        # mount_z_separation = 1
        # mount_y_separation = -1
        # mount_size = [self.holder_size[0] + self.cover_thickness * 2 - .002, self.cover_thickness,
        #               self.headstage_size[2]]
        # mount_location = [0, -self.cover_size[1] / 2 - mount_size[1] / 2 - mount_y_separation + .001,
        #                   self.cover_size[2] / 2 + mount_size[2] / 2 + mount_z_separation - .001]
        # mount = add_cube(mount_size, (0, 0, 0), 'mount')
        # translate(mount_location)
        # select_verts(mount, [-100, 100], [-100, 100], [-100, 0])
        # extrude_move((0, (mount_y_separation + self.cover_thickness) / 2, -mount_z_separation))
        # resize((1, (mount_size[1] + mount_y_separation + self.cover_thickness) / mount_size[1], 1))
        # extrude_move((0, 0, -1))
        # extrude_move((0, (mount_y_separation + mount_size[1]) / 2, -2))
        # resize((1, self.cover_thickness / (mount_size[1] + mount_y_separation + self.cover_thickness), 1))
        # boolean_modifier(cover, mount, modifier='UNION')
        # delete([mount])

        activate([cover])
        bpy.ops.transform.translate(value=self.cover_xyz)

        # This makes the back cutter
        size = [self.PIXEL_TOP[0] - .7,
                self.cover_clearance + self.PIXEL_TOP[1] + self.holder_y_extension + self.cap_clearance +
                self.cap_wall_thickness + self.cover_clearance + self.cover_thickness,
                self.cover_size[2]]
        location = [0, -size[1] / 2 - self.PIXEL_PROBE_Y,
                    self.cover_xyz[2] + self.cover_thickness + .02 + 1]
        back_cutter = add_cube(size, location, 'pixel_cutter')
        boolean_modifier(cover, back_cutter)
        delete([back_cutter])

        # This makes the pixel cutter
        size = [self.PIXEL_TOP[0] + 2 * self.cover_clearance,
                2 * self.cover_clearance + self.PIXEL_TOP[1],
                self.cover_size[2]]
        location = [0, -size[1] / 2 + self.PIXEL_TOP[1] - self.PIXEL_PROBE_Y + self.cover_clearance,
                    self.cover_xyz[2] + self.cover_thickness + .02 + 1]
        pixel_cutter = add_cube(size, location, 'pixel_cutter')
        boolean_modifier(cover, pixel_cutter)
        delete([pixel_cutter])
        front_section_y = self.cover_size[1] / 2 + self.cover_xyz[1] - (size[1] / 2 + location[1])

        # This makes the cut out for the screws to secure the cover
        depth = self.cover_size[0] + self.hex_depth * 2
        bpy.ops.mesh.primitive_cylinder_add(radius=self.SCREW_THREAD_RADIUS,  # * 1.3,
                                            depth=depth,
                                            location=self.hex_location, rotation=(0, pi / 2, 0))
        hex_screw = bpy.context.active_object
        offset = self.cap_size[1] / 6
        for side in [1, -2]:
            activate([hex_screw])
            translate([side * depth / 2, side * offset, 0])
            boolean_modifier(cover, hex_screw)
        delete([hex_screw])

        # This adds the cover for the screw
        added_thickness = self.cover_thickness
        size = [self.SCREWHEAD_UPPER_RADIUS * 2 + 2 * self.cover_thickness, front_section_y - .02, added_thickness]
        loc = [0, self.cover_xyz[1] + self.cover_size[1] / 2 - size[1] / 2 - .01,
               self.cover_xyz[2] + self.cover_size[2] / 2 + size[2] / 2 - .001]
        screw_cover = add_cube(size, loc, 'screw_cover')

        bpy.ops.mesh.primitive_cylinder_add(radius=self.DRIVER_WIDTH / 2, depth=self.SCREW_LENGTH,
                                            location=[0, self.screw_y,
                                                      self.cover_xyz[2] + self.cover_size[
                                                          2] / 2 - self.SCREWHEAD_DEPTH / 2],
                                            rotation=(0, 0, 0))
        screw = bpy.context.active_object
        boolean_modifier(screw_cover, screw)
        boolean_modifier(cover, screw_cover, 'UNION')
        delete([screw])
        delete([screw_cover])

        # This makes the cutout for the screw head
        loc = [0, self.screw_y, self.cover_xyz[2] + self.cover_size[2] / 2 - self.SCREWHEAD_DEPTH / 2]
        bpy.ops.mesh.primitive_cylinder_add(radius=self.SCREWHEAD_UPPER_RADIUS, depth=self.SCREWHEAD_DEPTH + .001,
                                            vertices=32,
                                            location=loc, rotation=(0, 0, 0))
        screwhead_cut = bpy.context.active_object
        select_verts(screwhead_cut, [-100, 100], [-100, 100], [-100, 0])
        ratio = self.SCREWHEAD_LOWER_RADIUS / self.SCREWHEAD_UPPER_RADIUS
        bpy.ops.transform.resize(value=(ratio, ratio, 1))
        select_verts(screwhead_cut, [-100, 100], [-100, 100], [-100, 0])
        bpy.ops.mesh.extrude_context_move(TRANSFORM_OT_translate={"value": (0, 0, -5)})
        select_verts(screwhead_cut, [-100, 100], [-100, 100], [100, 0])
        bpy.ops.mesh.extrude_context_move(TRANSFORM_OT_translate={"value": (0, 0, self.screwhead_top)})
        select_verts(screwhead_cut, [-100, 100], [self.SCREWHEAD_UPPER_RADIUS * .2, 100], [-100, 100])
        extrude_move((0, 5, 0))
        boolean_modifier(cover, screwhead_cut)
        delete([screwhead_cut])

        # This adds a cutout for the pixel dovetail to come through
        size = [self.DOVE_OUTER_WIDTH + .5, self.DOVE_DEPTH, 4]
        loc = [0, self.PIXEL_BOTTOM[1] - self.PIXEL_PROBE_Y + size[1] / 2,
               self.cover_xyz[2] + self.cover_size[2] / 2]
        dove_space_cut = add_cube(size, loc, 'dove_space_cut')
        boolean_modifier(cover, dove_space_cut)
        delete([dove_space_cut])

        do_screw_test = False
        if do_screw_test:
            screw_test = add_cube(self.cover_size, [0, 0, 0], 'screw_test')
            bpy.ops.transform.translate(value=self.cover_xyz)
            bpy.ops.transform.translate(
                value=(
                    0, self.cover_size[1] - front_section_y + .002, self.cover_size[2] - self.SCREWHEAD_DEPTH - 1))
            boolean_modifier(screw_test, cover, modifier='INTERSECT')
            activate([cover])
            bpy.ops.object.delete(use_global=False)

        if shield:
            self.add_shield(cover, num_shield=2)
        return cover

    def stopper(self, shield=False):
        # This makes the piece that permanently attaches to the pixel
        holder_location = [0, self.holder_size[1] / 2, self.holder_size[2] / 2]
        stopper = add_cube(self.holder_size, holder_location, 'stopper')
        for x in [[0, 100], [-100, 0]]:
            select_verts(stopper, x, [self.holder_size[1], 100], [-100, 100])
            bpy.ops.mesh.bevel(offset=self.bevel_offset, segments=10)
        bpy.ops.object.mode_set(mode='OBJECT')

        # This makes the square that inserts into the bottom section
        clear_size = list(map(lambda x: x - 4 * self.cap_bottom_lip, self.holder_size))
        clear_size[2] = self.holder_size[2] / 3
        clear_location = [0, .6, clear_size[2] / 2 + self.cap_bottom_thickness + self.cap_clearance]
        clear = add_cube(clear_size, clear_location, 'clear')

        # This makes the cap dovetail
        dove2_size = [self.dove2_width, self.dove2_depth, self.holder_size[2] + 5]
        dove2_location = [0, self.holder_size[1] - dove2_size[1] / 2 + .001,
                          self.holder_size[2] / 2 - self.holder_wall_thickness]
        cap_dovetail = add_cube(dove2_size, dove2_location, 'cap_dovetail')
        select_verts(cap_dovetail, [-dove2_size[0] / 2, dove2_size[0] / 2], [0, dove2_location[1]], [-100, 100])
        ratio = 1 + 2 * dove2_size[1] / sqrt(3) / dove2_size[0]
        bpy.ops.transform.resize(value=(ratio, 1, 1))
        boolean_modifier(stopper, cap_dovetail)
        select_verts(stopper, [-self.dove2_width / 2, self.dove2_width / 2], [self.holder_size[1], 100],
                     [-100, 100])
        bpy.ops.mesh.bevel(offset=self.dove_bevel, segments=1)
        mode(('OBJECT'))

        # This makes the cutout for the securing hex nut
        embed_depth = self.holder_size[2] / 2
        bpy.ops.mesh.primitive_cylinder_add(radius=self.hex_radius, depth=self.hex_depth, vertices=6,
                                            location=(0, 0, self.holder_size[2] - embed_depth))
        hex_cut = bpy.context.active_object
        bpy.ops.transform.rotate(value=pi / 6, orient_axis='Z')
        hex_y = (self.holder_size[1] - self.dove2_depth) / 2
        bpy.ops.transform.translate(value=(0, hex_y, 0))
        select_verts(hex_cut, [-100, 100], [-100, -self.hex_radius], [-100, 100])
        translate((-self.hex_radius, 0, 0))
        mode('OBJECT')

        # This makes the cutout for the screw to come through
        loc = (0, hex_y, self.SCREW_LENGTH / 2 + self.holder_size[2] - embed_depth)
        bpy.ops.mesh.primitive_cylinder_add(radius=self.SCREW_THREAD_RADIUS, depth=self.SCREW_LENGTH, location=loc)
        screw_cut = bpy.context.active_object

        # This applies boolean modifiers, deletes, and translates
        boolean_modifier(stopper, hex_cut)
        boolean_modifier(stopper, screw_cut)

        for obj in [cap_dovetail, hex_cut, screw_cut]:
            activate([obj])
            bpy.ops.object.delete(use_global=False)

        activate([stopper])
        select_verts(stopper, [-ratio * dove2_size[0] / 2, ratio * dove2_size[0] / 2],
                     [self.holder_size[1] - dove2_size[1], 100], [-100, 0])
        bpy.ops.mesh.bevel(offset=self.base_bevel, segments=1)

        activate([stopper])
        bpy.ops.transform.translate(value=self.holder_xyz)
        boolean_modifier(stopper, clear, modifier='UNION')
        activate([clear])
        bpy.ops.object.delete(use_global=False)

        if shield:
            self.add_shield(stopper, shield_height=self.holder_size[2] + 1, radius=self.holder_size[0] / 2 + 2,
                            location=(0, 1, self.holder_size[2] / 2 + 3))

        return stopper

    def stabber(self, shield=False):
        # This makes the piece that permanently attaches to the pixel
        stabber_location = [0, self.holder_size[1] / 2, self.holder_size[2] / 2]
        stabber = add_cube(self.holder_size, stabber_location, 'stabber')
        for x in [[0, 100], [-100, 0]]:
            select_verts(stabber, x, [self.holder_size[1], 100], [-100, 100])
            bpy.ops.mesh.bevel(offset=self.bevel_offset, segments=10)
        bpy.ops.object.mode_set(mode='OBJECT')

        # This makes the dovetail cutout
        cutter_size = [self.PIXEL_BOTTOM[0] + 2 * self.holder_clearance,
                       self.PIXEL_BOTTOM[1] + self.holder_y_extension,
                       20]
        dovetail = [self.DOVE_INNER_WIDTH, self.DOVE_DEPTH, 10]
        xyz_location = [0, cutter_size[1] / 2 - .001,
                        dovetail[2] / 2 + self.holder_space_below_dove - self.holder_clearance]
        cutter = add_cube(cutter_size, xyz_location, 'cutter')
        select_verts(cutter, [-100, 100], [0, 100], [-100, 100])
        bpy.ops.mesh.extrude_region()
        ratio = list(map(lambda x, y: x / y, dovetail, cutter_size))
        bpy.ops.transform.resize(value=(ratio[0], 1, ratio[2]))
        bpy.ops.mesh.extrude_context_move(TRANSFORM_OT_translate={"value": (0, dovetail[1], 0)})
        bpy.ops.transform.resize(value=(self.DOVE_OUTER_WIDTH / self.DOVE_INNER_WIDTH, 1, 1))
        for side in [1, -1]:
            select_verts(cutter, [side * dovetail[0] / 2, 0], [0, 100], [-100, 100])
            bpy.ops.mesh.bevel(offset=self.pixel_dove_bevel, segments=1)

        bpy.ops.object.mode_set(mode='OBJECT')

        # This makes the needle cut pieces
        cut_size = [self.holder_size[0] - 2, 3, self.holder_size[2] + 1]
        cut_location = [0, -cut_size[1] / 2 - self.holder_xyz[1], self.holder_size[2] / 2]
        cut = add_cube(cut_size, cut_location, 'cut')
        boolean_modifier(stabber, cut)

        needle_size = [self.needle_diameter, self.needle_diameter, self.holder_size[2] + 1]
        needle_location = [0, 0, self.holder_size[2] / 2]
        needle = add_cube(needle_size, needle_location, 'needle')
        bpy.ops.transform.rotate(value=pi / 4, orient_axis='Z')
        bpy.ops.transform.translate(value=[0, -self.holder_xyz[1] + .001, 0])
        boolean_modifier(stabber, needle)

        delete([cut, needle])

        # This makes the cap dovetail
        dove2_size = [self.dove2_width, self.dove2_depth, self.holder_size[2] + 5]
        dove2_location = [0, self.holder_size[1] - dove2_size[1] / 2 + .001,
                          self.holder_size[2] / 2 - self.holder_wall_thickness]
        cap_dovetail = add_cube(dove2_size, dove2_location, 'cap_dovetail')
        select_verts(cap_dovetail, [-dove2_size[0] / 2, dove2_size[0] / 2], [0, dove2_location[1]], [-100, 100])
        ratio = 1 + 2 * dove2_size[1] / sqrt(3) / dove2_size[0]
        bpy.ops.transform.resize(value=(ratio, 1, 1))
        boolean_modifier(stabber, cap_dovetail)
        select_verts(stabber, [-self.dove2_width / 2, self.dove2_width / 2], [self.holder_size[1], 100],
                     [-100, 100])
        bpy.ops.mesh.bevel(offset=self.dove_bevel, segments=1)
        mode(('OBJECT'))

        # This makes the handle piece
        handle_location = [0, self.handle_size[1] / 2 + cutter_size[1] + dovetail[1] + .001,
                           self.holder_size[2] - self.handle_size[2] / 2 - .001]
        handle = add_cube(self.handle_size, (0, 0, 0), 'handle')
        for side in [1, -1]:
            select_verts(handle, [side * 100, 0], [0, 100], [-100, 100])
            bpy.ops.mesh.bevel(offset=1.3, segments=1)

        mode(('OBJECT'))
        translate(handle_location)
        boolean_modifier(stabber, handle, modifier='UNION')

        # This makes the cutout for the securing hex nut
        hex_location = [0, 5 / 2 + cutter_size[1] + dovetail[1] + .001,
                        self.holder_size[2] - self.handle_size[2] / 2 - .001]
        # hex_location = [0, self.screw_y-self.holder_xyz[1],
        #                 self.holder_size[2] - handle_size[2] / 2 - .001]
        bpy.ops.mesh.primitive_cylinder_add(radius=self.hex_radius, depth=self.hex_depth, vertices=6,
                                            location=hex_location)
        hex_cut = bpy.context.active_object
        bpy.ops.transform.rotate(value=pi / 6, orient_axis='Z')
        select_verts(hex_cut, [-100, 100], [-100, -self.hex_radius], [-100, 100])
        translate((-self.hex_radius, 0, 0))
        mode('OBJECT')
        bpy.ops.transform.rotate(value=pi, orient_axis='Z')
        mode('OBJECT')

        # This makes the cutout for the screw to come through
        bpy.ops.mesh.primitive_cylinder_add(radius=self.SCREW_THREAD_RADIUS, depth=self.SCREW_LENGTH,
                                            location=hex_location)
        screw_cut = bpy.context.active_object

        # This applies boolean modifiers, deletes, and translates
        boolean_modifier(stabber, hex_cut)
        boolean_modifier(stabber, screw_cut)

        for obj in [cutter, handle, cap_dovetail, hex_cut, screw_cut]:
            activate([obj])
            bpy.ops.object.delete(use_global=False)

        activate([stabber])
        select_verts(stabber, [-ratio * dove2_size[0] / 2, ratio * dove2_size[0] / 2],
                     [self.holder_size[1] - dove2_size[1], 100], [-100, 0])
        bpy.ops.mesh.bevel(offset=self.base_bevel, segments=1)

        activate([stabber])
        bpy.ops.transform.translate(value=self.holder_xyz)
        if shield:
            self.add_shield(stabber, shield_height=self.holder_size[2] + 1, radius=self.holder_size[0] / 2 + 2,
                            location=(0, 2, self.holder_size[2] / 2 + 3))

    def surgery(self, shield=False):
        # This makes the piece that permanently attaches to the pixel
        holder_location = [0, self.holder_size[1] / 2, self.holder_size[2] / 2]
        surgery = add_cube(self.holder_size, holder_location, 'surgery')
        for x in [[0, 100], [-100, 0]]:
            select_verts(surgery, x, [self.holder_size[1], 100], [-100, 100])
            bpy.ops.mesh.bevel(offset=self.bevel_offset, segments=10)
        bpy.ops.object.mode_set(mode='OBJECT')

        # This makes the cap dovetail
        dove2_size = [self.dove2_width, self.dove2_depth, self.holder_size[2] + 5]
        dove2_location = [0, self.holder_size[1] - dove2_size[1] / 2 + .001,
                          self.holder_size[2] / 2 - self.holder_wall_thickness]
        cap_dovetail = add_cube(dove2_size, dove2_location, 'cap_dovetail')
        select_verts(cap_dovetail, [-dove2_size[0] / 2, dove2_size[0] / 2], [0, dove2_location[1]], [-100, 100])
        ratio = 1 + 2 * dove2_size[1] / sqrt(3) / dove2_size[0]
        bpy.ops.transform.resize(value=(ratio, 1, 1))
        boolean_modifier(surgery, cap_dovetail)
        select_verts(surgery, [-self.dove2_width / 2, self.dove2_width / 2], [self.holder_size[1], 100],
                     [-100, 100])
        bpy.ops.mesh.bevel(offset=self.dove_bevel, segments=1)
        mode(('OBJECT'))

        # This makes the needle cut pieces
        cut_size = [self.holder_size[0] + 1, self.holder_xyz[1] * 2, self.holder_size[2] + 1]
        cut_location = [0, 0, self.holder_size[2] / 2]
        cut = add_cube(cut_size, cut_location, 'cut')

        post_size = [self.post_diameter, self.post_diameter, self.holder_size[2] + 1]
        post_location = [0, 0, self.holder_size[2] / 2]
        post = add_cube(post_size, post_location, 'post')
        bpy.ops.transform.rotate(value=pi / 4, orient_axis='Z')
        bpy.ops.transform.translate(value=[self.surgery_post_separation / 2, -self.holder_xyz[1] + .001, 0])
        boolean_modifier(surgery, post)
        activate([post])
        bpy.ops.transform.translate(value=[-self.surgery_post_separation, 0, 0])
        boolean_modifier(surgery, post)

        needle_size = [self.needle_diameter, self.needle_diameter, self.holder_size[2] + 1]
        needle_location = [0, 0, self.holder_size[2] / 2]
        needle = add_cube(needle_size, needle_location, 'needle')
        bpy.ops.transform.rotate(value=pi / 4, orient_axis='Z')
        bpy.ops.transform.translate(value=[0, -self.holder_xyz[1] + .001, 0])
        boolean_modifier(surgery, needle)

        # This applies boolean modifiers, deletes, and translates
        boolean_modifier(surgery, cut)

        for obj in [cap_dovetail, cut, post, needle]:
            activate([obj])
            bpy.ops.object.delete(use_global=False)

        activate([surgery])
        select_verts(surgery, [-ratio * dove2_size[0] / 2, ratio * dove2_size[0] / 2],
                     [self.holder_size[1] - dove2_size[1], 100], [-100, 0])
        bpy.ops.mesh.bevel(offset=self.base_bevel, segments=1)

        activate([surgery])

        height = self.holder_size[2] + 1
        radius = self.holder_size[0] / 2 + 1

        activate([surgery])
        bpy.ops.transform.translate(value=self.holder_xyz)
        if shield:
            self.add_shield(surgery, shield_height=self.holder_size[2] + 1, radius=self.holder_size[0] / 2 + 2,
                            location=(0, 1, self.holder_size[2] / 2 + 3))

        return surgery

    def add_shield(self, obj, num_shield=1):
        apply_all(obj)
        vert_coords = np.array([list(v.co) for v in obj.data.vertices])
        bbox = np.stack([np.min(vert_coords, axis=0), np.max(vert_coords, axis=0)])
        shield_loc = np.mean(bbox, axis=0)
        square_distances = (vert_coords[:, 0] - shield_loc[0]) ** 2 + (vert_coords[:, 1] - shield_loc[1]) ** 2
        shield_radius = max(np.sqrt(square_distances)) + 1
        shield_height = abs(bbox[0][2] - bbox[1][2])

        for i in range(num_shield):
            radius = shield_radius + 2 * i
            shield = add_cylinder(radius + self.shield_thickness, shield_height, 32, 'shield')
            shield_cut = add_cylinder(radius, shield_height + 1, 32, 'shield_cut')
            boolean_modifier(shield, shield_cut)
            activate([shield])
            translate(shield_loc)
            boolean_modifier(obj, shield, 'UNION')
            delete([shield_cut, shield])

    def tube(self, play=False):
        radius = 18
        length = 100
        thickness = 2
        ceiling_thickness = 2
        base_thickness = 2
        vertices = 100
        front_distance = 10
        slit_width = self.cap_size[0] + 2
        top_angle = 2 / 180 * pi
        ceiling = 2 * radius * .8
        slant_angle = 5 / 180 * pi
        slant_length = 20
        slant_height = 7.2
        front_bevel = .5
        headfix_internal_x_angle = 10 / 180 * pi

        # This makes the tube
        tube = add_cylinder(radius + thickness, length, vertices, 'tube')
        tube_cut = add_cylinder(radius + thickness, length, vertices, 'tube_cut')
        activate([tube, tube_cut])
        rotate(pi / 2, 'X')
        mode(('OBJECT'))

        # This makes the base
        base = add_cube([2 * radius, length - .1, base_thickness], [0, 0, 0], 'base')
        translate((0, 0, -radius - thickness + base_thickness / 2 - .1))

        # This makes the center cut
        center = add_cylinder(radius, length + thickness, vertices, 'center')
        rotate(pi / 2, 'X')
        mode('OBJECT')

        # This add the slit cutter
        slit = add_cube([slit_width, length + .01, radius], [0, 0, 0], 'slit')
        translate((0, 0, radius / 2))
        mode('OBJECT')

        # This makes the inner slant shape for the headfix
        slant_size = [(radius + thickness) * 2, slant_length, radius]
        slant_y = length / 2 - slant_length / 2 - 1
        slant_z = slant_size[2] / 2 - radius + ceiling - 1
        slant = add_cube(slant_size, (0, 0, 0), 'slant')
        translate([0, slant_y, slant_z])
        translate([0, 0, -slant_height])
        select_verts(slant, INF, INF_POS, INF_NEG)
        translate((0, 0, slant_size[1] * tan(slant_angle)))
        select_verts(slant, INF, INF_NEG, INF_NEG)
        bevel(front_bevel)
        boolean_modifier(slant, tube, 'INTERSECT')
        resize((.99, 1, 1))
        mode(('OBJECT'))

        # This flattens the tube and center
        z_depth = radius + thickness
        flatten = add_cube([(radius + thickness) * 2, length + 1, z_depth], [0, 0, 0], 'flatten')
        translate(
            (
                0, 0,
                z_depth / 2 - radius - 2.9))  # Need to adjust the number everytime, doing the math will take too long
        mode(('OBJECT'))
        translate((0, 0, ceiling))
        boolean_modifier(center, flatten)
        activate([flatten])
        translate((0, 0, ceiling_thickness))
        boolean_modifier(tube, flatten)
        activate([flatten])
        translate((0, 0, -.01))
        boolean_modifier(slant, flatten)

        # This applies the booleans
        boolean_modifier(tube, base, 'UNION')
        boolean_modifier(tube, center)
        if not play:
            boolean_modifier(tube, slant, 'UNION')
        boolean_modifier(tube, slit)
        delete([base, flatten, slant, center])

        # This moves the tube to position
        activate([tube, tube_cut])
        translate((0, -length / 2 + front_distance, radius - ceiling + (length - front_distance) * tan(top_angle)))
        translate((0, 0, self.head_fix_dims[2] + self.headfix_bar_z))

        if not play:
            # This cuts out the headfix piece
            headfix_cut_size = [self.cap_size[0] + 2 * (self.head_fix_dims[0] + self.headfix_clearance),
                                self.head_fix_dims[1] + self.headfix_clearance + .02,
                                self.head_fix_dims[2] + 1.8 * self.headfix_clearance]
            headfix_cut_location = [0, self.holder_size[1] / 2 + self.holder_xyz[1] + self.headfix_clearance / 2,
                                    self.head_fix_dims[2] / 2 + self.headfix_bar_z]
            headfix_cut = add_cube(headfix_cut_size, [0, 0, 0], 'headfix_cut')
            translate(headfix_cut_location)
            select_verts(headfix_cut, INF, INF_NEG, INF)
            factor = 1 + 2 * headfix_cut_size[1] * tan(headfix_internal_x_angle) / headfix_cut_size[0]
            resize((factor, 1, 1))
            extention = 25
            extrude_move((0, -extention, 0))
            factor = 1 + 2 * extention * tan(headfix_internal_x_angle) / (factor * headfix_cut_size[0])
            resize((factor, 1, 1))
            select_verts(headfix_cut, INF, [-100, -extention], INF_NEG)
            translate((0, 0, -extention * tan(slant_angle)))
            select_verts(headfix_cut, INF, INF_POS, INF)
            extrude_move((0, 25, 0))
            boolean_modifier(tube, headfix_cut)
            delete([headfix_cut])

            # This cuts holes for the backer
            backer_clearance = .15
            backer_size = [radius * 3, headfix_cut_size[2], headfix_cut_size[2]]
            backer_cut = add_cube([x + 2 * backer_clearance for x in backer_size], (0, 0, 0), 'backer_cut')
            backer = add_cube(backer_size, (0, 0, 0), 'backer')
            activate((backer, backer_cut))
            translate(headfix_cut_location)
            translate((0, backer_size[1] / 2 + headfix_cut_size[1] / 2, 0))
            select_verts(backer_cut, INF, INF_NEG, INF)
            extrude_move((0, -headfix_cut_size[2] / 2, 0))
            resize((1, 1, .01))
            select_verts(backer_cut, INF, INF_POS, INF)
            extrude_move((0, headfix_cut_size[2] / 2, 0))
            resize((1, 1, .01))

            boolean_modifier(tube, backer_cut)
            delete([backer_cut])

            boolean_modifier(backer, slit)
            delete([slit])
            activate([backer])
            select_verts(backer, INF_POS, INF, INF)
            bpy.ops.mesh.delete(type='VERT')
            mode(('OBJECT'))

            block_size = 6
            end_block = add_cube([block_size, block_size, block_size], [0, 0, 0], 'end_block')
            translate(headfix_cut_location)
            translate((-radius - block_size / 2 + 1, backer_size[1] / 2 + headfix_cut_size[1] / 2, 0))
            boolean_modifier(end_block, tube_cut)
            boolean_modifier(backer, end_block, 'UNION')
            delete([tube_cut, end_block])

            # this cuts out the hex and screw holes
            headfix_translate = (0, self.holder_size[1] / 2 + self.holder_xyz[1],
                                 (self.head_fix_dims[
                                      2] + 2 * self.headfix_thickness) / 2 - self.headfix_thickness + self.headfix_bar_z)
            for side in [1, -1]:
                distance = 2.3
                hex_location = [side * (self.cap_size[0] / 2 + self.head_fix_dims[0] + distance),
                                -self.head_fix_dims[1] / 2 - distance + self.headfix_clearance,
                                self.head_fix_dims[2] / 2 + distance]
                hex_cut = add_cylinder(self.hex_radius, self.hex_depth, 6, 'hex_cut')
                mode('OBJECT')
                screw_cut = add_cylinder(self.headfix_screw_radius, distance * 5, 32, 'screw_cut')
                activate([hex_cut, screw_cut])
                rotate(pi / 6, 'Z')
                bpy.ops.transform.rotate(value=pi / 4, orient_axis='Y',
                                         orient_matrix=(
                                             (side * 1.0, -1.0, 0.0), (1.0, side * 1.0, 0.0), (0.0, 0.0, 1.0)))
                bpy.ops.transform.translate(value=hex_location)
                bpy.ops.transform.translate(value=headfix_translate)

                # This cuts holes for the clicks
                click_hole = add_cube([1.5, 2, thickness + 1], (0, 0, 0), 'click_hole')
                bpy.ops.transform.translate(value=hex_location)
                bpy.ops.transform.translate(value=headfix_translate)
                translate((-side * 4, 0, -thickness / 2))
                select_verts(click_hole, INF, INF_NEG, INF_POS)
                translate((0, -1.5, 0))
                select_verts(click_hole, INF, INF_POS, INF_NEG)
                translate((0, 1.5, 0))
                mode('OBJECT')

                click_radius = .5
                click_clearance = .1
                click_holder_thickness = .4
                length = 80
                click_holder_cut = add_cylinder(radius=click_radius + click_clearance, depth=length,
                                                vertices=32, name='click_holder')
                click_holder = add_cylinder(radius=click_radius + click_clearance + click_holder_thickness,
                                            depth=30,
                                            vertices=32, name='click_holder')
                activate([click_holder, click_holder_cut])
                rotate(pi / 2, 'X')
                bpy.ops.transform.translate(value=hex_location)
                bpy.ops.transform.translate(value=headfix_translate)
                translate((-side * 4, -length / 2, .3))

                boolean_modifier(tube, hex_cut)
                boolean_modifier(tube, screw_cut)
                boolean_modifier(tube, click_hole)
                boolean_modifier(tube, click_holder, modifier='UNION')
                boolean_modifier(tube, click_holder_cut)

                # This deletes the cutters
                delete([hex_cut, screw_cut, click_hole, click_holder, click_holder_cut])

            # This cuts out a faster print
            trim = add_cube([3 * radius, 60, radius], (0, 0, 0), 'trim')
            translate((0, -12, 7))
            boolean_modifier(trim, tube, 'INTERSECT')

        return tube

    def stand(self, test=False):
        # This makes the stand
        stand = add_cube(self.stand_size, (0, self.cover_thickness / 2 - self.stand_front / 2, 0), 'stand')

        # This makes the mid section cutout
        hole_size = [self.cover_size[0] + 2 * self.stand_clearance,
                     self.cover_size[1] + 2 * self.stand_clearance,
                     self.stand_cover_depth + self.stand_clearance]
        hole_location = [0, 0, self.stand_size[2] / 2 - hole_size[2] / 2 + .001]
        hole = add_cube(hole_size, (0, 0, 0), 'hole')
        select_verts(hole, INF, INF, INF_NEG)
        ratio_x = (hole_size[0] - self.stand_clearance) / hole_size[0]
        ratio_y = (hole_size[1] - self.stand_clearance) / hole_size[1]
        resize([ratio_x, ratio_y, 1])
        mode('OBJECT')
        translate(hole_location)
        boolean_modifier(stand, hole)

        clear_size = [self.cover_size[0] - 2 * self.stand_ridge,
                      self.cover_size[1] - 2 * self.stand_ridge + 2 * self.stand_front,
                      self.stand_size[2] + 1]
        clear_location = [0, -self.stand_front, 0]
        clear = add_cube(clear_size, clear_location, 'clear')
        select_verts(clear, [-100, 100], [-100, 0], [-100, 100])
        extrude_move((0, -5, 0))
        boolean_modifier(stand, clear)

        # This makes the base of the stand
        wall_depth = 5
        base_location = [0, 0, -self.stand_size[2] / 2 - self.stand_base_size[2] / 2 + .001]
        base = add_cube(self.stand_base_size, (0, 0, 0), 'base')
        select_verts(base, INF, INF, INF_POS)
        translate([0, 0, wall_depth])
        mode('OBJECT')
        inner_size = [self.stand_lid_size[0] + .4, self.stand_lid_size[1] + .4, wall_depth + .01]
        inner_cut = add_cube(inner_size, (0, 0, 0), 'inner_cut')
        translate([0, 0, inner_size[2] / 2 + self.stand_base_size[2] / 2])
        boolean_modifier(base, inner_cut)
        delete([inner_cut])
        activate([base])
        translate(base_location)
        boolean_modifier(stand, base, 'UNION')

        # This moves the stand into position
        activate([stand])
        bpy.ops.transform.translate(value=self.cover_xyz)
        translate([0, 0, -self.cap_top_extention])
        bpy.ops.transform.translate(
            value=[0, 0, -self.stand_size[2] / 2 - self.cover_size[2] / 2 + self.stand_cover_depth])

        # This makes the cut outs for the screws that afix the cover
        depth = self.stand_size[0] + 1
        size = [depth, 5, self.stand_cover_depth + 1]
        loc = [0, self.hex_location[1],
               self.cover_xyz[2] - self.cover_size[2] / 2 + size[2] / 2 - self.cap_top_extention]
        screw_clear = add_cube(size, loc, 'screw_clear')
        offset = self.cap_size[1] / 6
        for side in [1, -2]:
            activate([screw_clear])
            translate([side * depth / 2, side * offset, 0])
            boolean_modifier(stand, screw_clear)

        # This makes the cut out for the cleaner piece
        size = [self.cover_size[0] - 2 * self.stand_ridge + 2 * self.inset, self.stand_size[1],
                self.cleaner_thickness + self.cleaner_clearance * 2]
        loc = [0, self.cover_xyz[1] - self.stand_thickness - self.stand_ridge - .01,
               size[2] / 2 - self.added_cleaner_space - self.stand_extra_lower_distance]
        clean_cut = add_cube(size, (0, 0, 0), 'clean_cut')
        translate(loc)
        select_verts(clean_cut, [-100, 100], [-100, 0], [-100, 100])
        increase = 1
        resize((1, 1, increase))
        translate((0, 0, size[2] * (increase - 1) / 2))
        boolean_modifier(stand, clean_cut)

        # This makes the cap dovetail
        clearance = self.cap_clearance - .02
        dove2_size = [self.dove2_width - 2 * clearance, self.dove2_depth - clearance, self.holder_size[2]]
        dove2_location = [0, self.holder_size[1] - dove2_size[1] / 2 + .001,
                          self.holder_size[2] / 2 - self.stand_extra_lower_distance]
        dove2_location = [x + y for x, y in zip(dove2_location, self.holder_xyz)]
        cap_dovetail = add_cube(dove2_size, dove2_location, 'cap_dovetail')
        select_verts(cap_dovetail, [-dove2_size[0] / 2, dove2_size[0] / 2], [0, dove2_location[1]], [-100, 100])
        ratio = 1 + 2 * dove2_size[1] / sqrt(3) / dove2_size[0]
        bpy.ops.transform.resize(value=(ratio, 1, 1))
        bpy.ops.mesh.bevel(offset=self.dove_bevel, segments=1)
        select_verts(cap_dovetail, [-100, 100], [dove2_location[1], 100], [-100, 100])
        bpy.ops.mesh.extrude_context_move(TRANSFORM_OT_translate={"value": (0, self.stand_clearance, 0)})
        ratio = 1 - 2 * self.stand_clearance / sqrt(3) / dove2_size[0]
        bpy.ops.transform.resize(value=(ratio, 1, 1))
        extrude_move((
            0, self.cap_wall_thickness + self.stand_thickness - self.stand_ridge - self.stand_clearance / 2 + 1,
            0))
        boolean_modifier(stand, cap_dovetail, 'UNION')

        # This cuts out space for the holder to lower in the back
        handle_size = [self.handle_size[0] + self.stand_clearance * 2, self.handle_size[1] * 4,
                       self.handle_size[
                           2] + self.stand_clearance * 2 + self.stand_cover_depth + self.stand_extra_lower_distance]
        handle_location = [0, handle_size[1] / 2,
                           self.cap_size[2] - handle_size[
                               2] / 2 + self.stand_clearance + self.stand_cover_depth - self.cap_top_extention]
        handle_cut = add_cube(handle_size, handle_location, 'handle_cut')
        boolean_modifier(stand, handle_cut)

        # This cuts out a spot for the screw to fit
        loc = [0, self.screw_y,
               self.cover_size[2] / 2 + self.cover_move_z - self.SCREW_LENGTH / 2 - self.cap_top_extention]
        bpy.ops.mesh.primitive_cylinder_add(radius=self.SCREW_THREAD_RADIUS + .1, depth=self.SCREW_LENGTH,
                                            location=loc, rotation=(0, 0, 0))
        screw_cut = bpy.context.active_object
        boolean_modifier(stand, screw_cut)

        delete([hole, clear, base, clean_cut, handle_cut, cap_dovetail, screw_clear, screw_cut])

        activate([stand])
        # translate([0, 0, self.cap_top_extention])

        if test:
            stand_test_size = [self.stand_size[0] + 1, self.stand_size[1] + 1, self.stand_size[2] + 1]
            stand_test = add_cube(stand_test_size, (0, self.cover_thickness / 2 - self.stand_front / 2, 0),
                                  'stand_test')
            translate(
                (self.cover_xyz[0], self.cover_xyz[1], stand_test_size[2] / 2 - self.stand_extra_lower_distance - 3))
            boolean_modifier(stand_test, stand, 'INTERSECT')
            return stand_test
        else:
            return stand

    def cleaner(self):
        # This makes the piece that holds the eppendorf tube and mates with the stand
        cleaner_size = [self.cover_size[0] - 2 * self.stand_ridge - 2 * self.stand_clearance + 2 * self.inset,
                        self.stand_size[1] + 5, self.cleaner_thickness]
        cleaner_loc = [0, -cleaner_size[1] / 2 + self.cap_size[1] / 2 - self.stand_clearance + self.cover_xyz[1],
                       cleaner_size[
                           2] / 2 + self.stand_clearance - self.added_cleaner_space - self.stand_extra_lower_distance]
        cleaner = add_cube(cleaner_size, cleaner_loc, 'cleaner')

        # This makes the cylinder
        radius = self.eppendorf_tube_diameter / 2
        bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=10, location=(0, -1, 0))
        tube_hole = bpy.context.active_object
        #
        # # This cuts away the interlocking pieces
        # cut_size = [self.stand_size[0] + 2 * self.stand_clearance, self.stand_size[1], self.stand_size[2]]
        # cut_location = [0, self.cover_xyz[1] + self.stand_size[1] / 3, 0]
        # cut = add_cube(cut_size, cut_location, 'cut')
        # inner_cut_size = [self.cover_size[0] - 2 * (self.stand_ridge + self.stand_clearance), self.stand_size[1], self.stand_size[2] + 2]
        # inner_cut = add_cube(inner_cut_size, cut_location, 'inner_cut')
        # translate((0, -1, 0))
        # boolean_modifier(cut, inner_cut)
        #
        # This applies boolean modifiers, deletes, and translates
        boolean_modifier(cleaner, tube_hole)

        for obj in [tube_hole]:
            activate([obj])
            bpy.ops.object.delete(use_global=False)

        return cleaner

    def headfix(self):
        headfix_size = [self.bridge_width + 2 * self.bridge_thickness,
                        self.head_fix_dims[1] + 2 * self.headfix_thickness,
                        self.head_fix_dims[2] + 2 * self.headfix_thickness]
        headfix_location = [0, 0, 0]
        headfix = add_cube(headfix_size, headfix_location, 'headfix')

        # This protrudes the brdige section
        select_verts(headfix, [-100, 100], [0, 100], [-100, 100])
        bpy.ops.mesh.extrude_context_move(TRANSFORM_OT_translate={"value": (0, self.bridge_y, 0)})

        # This makes the two side bars
        for sign in [1, -1]:
            select_verts(headfix, [0, sign * 100], [-headfix_size[1] / 2, headfix_size[1] / 2], [-100, 100])
            bpy.ops.mesh.extrude_context_move(
                TRANSFORM_OT_translate={"value": (sign * (self.stereotax_width - headfix_size[0])
                                                  / 2, 0, 0)})
            bpy.ops.mesh.extrude_region()
            bpy.ops.transform.resize(value=(1, self.stereotax_bar_thickness / headfix_size[1],
                                            self.stereotax_bar_thickness / headfix_size[2]))
            bpy.ops.mesh.extrude_context_move(
                TRANSFORM_OT_translate={"value": (sign * self.stereotax_bar_length, 0, 0)})
        bpy.ops.object.mode_set(mode='OBJECT')

        # This makes the pieces to cut out the middle
        cut1_size = [self.bridge_width, headfix_size[1] + 2 * (self.bridge_y - self.bridge_thickness), 20]
        cut1 = add_cube(cut1_size, (0, 0, 0), 'cut1')

        cut2_size = [self.cap_size[0] + 2 * (self.head_fix_dims[0] + self.headfix_clearance),
                     self.head_fix_dims[1] + self.headfix_thickness + self.headfix_clearance + .002,
                     self.head_fix_dims[2] + 2 * self.headfix_clearance]
        cut2_location = [0, -cut2_size[1] / 2, 0]
        cut2 = add_cube(cut2_size, cut2_location, 'cut2')
        bpy.ops.transform.translate(value=(0, self.head_fix_dims[1] / 2 + self.headfix_clearance, 0))
        select_verts(cut2, [-100, 100], [-100, -cut2_size[1]], [100, 0])
        bpy.ops.transform.translate(value=(0, 0, cut2_size[1] * tan(self.headfix_bar_slant * pi / 180)))

        for side in [1, -1]:
            select_verts(cut2, [side * 100, 0], [-100, -cut2_size[1]], [-100, 100])
            bpy.ops.transform.translate(value=(side * cut2_size[1] * tan(self.headfix_bar_slant * pi / 180), 0, 0))

        bpy.ops.object.mode_set(mode='OBJECT')

        cut3_size = [self.stereotax_width + .002, self.bridge_y + headfix_size[1] + .004, 5]
        cut3_location = [0, -cut3_size[1] / 2 + self.bridge_y + headfix_size[1] / 2 + .002,
                         -cut3_size[2] / 2 - headfix_size[2] / 2 + .5]
        cut3 = add_cube(cut3_size, [0, 0, 0], 'cut3')
        bpy.ops.transform.translate(value=cut3_location)
        select_verts(cut3, [-100, 100], [100, 0], [100, 0])
        bpy.ops.transform.translate(value=(0, 0, cut3_size[1] * tan(self.headfix_bar_slant * pi / 180)))

        bottom_thickness = 1
        amount_to_cut = self.headfix_thickness - self.headfix_clearance - bottom_thickness
        bpy.ops.object.mode_set(mode='OBJECT')
        cut4_size = [self.stereotax_width + .002, self.bridge_y + headfix_size[1] + .004, 5]
        cut4_location = [0, -cut4_size[1] / 2 + self.bridge_y + headfix_size[1] / 2 + .002,
                         -cut4_size[2] / 2 - headfix_size[2] / 2 + amount_to_cut]
        cut4 = add_cube(cut4_size, [0, 0, 0], 'cut4')
        bpy.ops.transform.translate(value=cut4_location)

        # This deletes the cutters
        for obj in [cut1, cut2, cut3, cut4]:
            boolean_modifier(headfix, obj)
            activate([obj])
            bpy.ops.object.delete(use_global=False)

        # This adds the bevels
        activate([headfix])
        for sign in [1, -1]:
            select_verts(headfix, [0, sign * cut1_size[0] / 2], [headfix_size[1], 100], [-100, 100])
            bpy.ops.mesh.bevel(offset=self.headfix_inner_bevel)
            select_verts(headfix, [sign * 100, sign * self.stereotax_width / 2],
                         [0, -self.stereotax_bar_thickness / 2],
                         [0, self.stereotax_bar_thickness / 2])
            bpy.ops.mesh.bevel(offset=self.stereotax_bevel)
            select_verts(headfix, [0, sign * cut1_size[0] / 2], [-100, headfix_size[1] / 2],
                         [-100, -cut2_size[2] / 2 - bottom_thickness])
            bpy.ops.mesh.bevel(offset=0.6)

        bpy.ops.object.mode_set(mode='OBJECT')

        # this cuts out the hex and screw holes
        for side in [1, -1]:
            distance = 2.7
            hex_location = [side * (self.cap_size[0] / 2 + self.head_fix_dims[0] + distance),
                            -self.head_fix_dims[1] / 2 - distance + self.headfix_clearance,
                            self.head_fix_dims[2] / 2 + distance]
            bpy.ops.mesh.primitive_cylinder_add(radius=self.hex_radius, depth=self.hex_depth, vertices=6,
                                                location=(0, 0, 0), rotation=(0, 0, 0))
            hex_cut = bpy.context.active_object
            bpy.ops.mesh.primitive_cylinder_add(radius=self.headfix_screw_radius, depth=distance * 4,
                                                location=(0, 0, 0), rotation=(0, 0, 0))
            screw_cut = bpy.context.active_object
            activate([hex_cut, screw_cut])
            bpy.ops.transform.rotate(value=pi / 4, orient_axis='Y',
                                     orient_matrix=(
                                         (side * 1.0, -1.0, 0.0), (1.0, side * 1.0, 0.0), (0.0, 0.0, 1.0)))
            bpy.ops.transform.translate(value=hex_location)

            boolean_modifier(headfix, hex_cut)
            boolean_modifier(headfix, screw_cut)

            # This deletes the cutters
            for obj in [hex_cut, screw_cut]:
                activate([obj])
                bpy.ops.object.delete(use_global=False)

        activate([headfix])
        bpy.ops.transform.translate(value=(0, self.holder_size[1] / 2 + self.holder_xyz[1],
                                           headfix_size[2] / 2 - self.headfix_thickness + self.headfix_bar_z))


class HeadMount:
    def __init__(self):
        self.objects = []
        # clearance for cap should .11
        # clearance for cover should be .15
        self.cap_clearance = .13  # should be .11
        self.cover_clearance = .16

        self.protrusion = 5

        self.lip_height = 1
        self.lip_outer_radius = .8
        self.lip_inner_radius = .45

        self.squeezer_bump_size = .8
        self.squeezer_z_shape = [1, 1.2, 1.2, 5]
        self.squeezer_width = 5
        self.squeezer_thickness = 1
        # self.squeezer_clearance = clearance
        self.squeezer_handle_gap = 1
        self.squeezer_handle_thickness = 2
        self.squeezer_handle_length = 14
        self.squeezer_bottom_thickness = 2
        self.squeezer_rotate_center = 7
        self.squeeze_length = 15

        self.squeezer_handle_size = [self.squeezer_width, 100, self.squeezer_width]

        self.dove_clearance = .1
        self.DOVE_OUTER_WIDTH = 4.86165
        self.DOVE_DEPTH = .5588
        self.DOVE_INNER_WIDTH = self.DOVE_OUTER_WIDTH - 2 * self.DOVE_DEPTH / sqrt(3)
        self.DOVE_Z_SPACER = 1
        self.DOVE_HEIGHT = 7.3 - 1

        self.PIXEL_TOP = [7.2, 1.2, 12.2]
        self.PIXEL_BOTTOM = [6.2, 1.2, 10.7]
        self.PIXEL_PROBE = [.07, .024, 10]
        self.PIXEL_PROBE_Y = .5
        # self.PIXEL_PROBE_Y = .9

        # holder settings
        self.holder_height = 10
        self.holder_space_below_dove = 2
        self.holder_y_extension = 1
        self.holder_wall_thickness = 1
        holder_x = self.PIXEL_BOTTOM[0] + 2 * self.holder_wall_thickness + 2 * self.dove_clearance
        # holder_x = self.squeezer_width + 2 * self.squeezer_bump_size + 2 * self.squeezer_clearance + self.holder_wall_thickness
        holder_y = self.holder_y_extension + self.PIXEL_BOTTOM[1] + self.DOVE_DEPTH + \
                   self.holder_wall_thickness + self.squeezer_thickness
        self.holder_size = [holder_x, holder_y, self.holder_height]

        self.pixel_xyz = [0, 0, self.PIXEL_PROBE[2] - self.protrusion - self.lip_height]
        self.holder_xyz = [0, -self.PIXEL_PROBE_Y + self.dove_clearance - self.holder_y_extension,
                           self.pixel_xyz[2] + self.DOVE_Z_SPACER - self.holder_space_below_dove]

        self.handle_width = 5.9
        self.handle_thickness = 3
        self.handle_length = 4.5

        # cap settings
        self.cap_wall_thickness = .8
        self.cap_size = list(
            map(lambda x: x + 2 * (self.cap_wall_thickness + self.cap_clearance), self.holder_size))
        self.cap_size[2] = self.holder_xyz[2] + self.holder_size[2]
        self.cap_bottom_thickness = 1.5
        self.cap_bottom_lip = .7
        self.cap_window_width = 1
        self.cap_window_base_thickness = self.cap_bottom_thickness + .001
        self.dove2_width = 2.95
        self.dove2_depth = 1
        self.dove2_clearance = .13  # should be .13

        self.head_fix_dims = [4, 2, 2]
        self.head_fix_cylinder_radius = .7
        self.headfix_bar_z = 1.5

        self.cap_bottom_bevel = 2
        self.ground_wire_depth = .5
        self.ground_wire_x = self.cap_size[0] / 2 - 3
        self.wire_location = [-self.ground_wire_x, -self.cap_size[1] / 2 + .01, self.cap_size[2] / 2]
        self.plug_width = 1
        self.plug_depth = 2
        self.plug_wall = .5

        # cover settings
        self.headstage_size = [17, 3, 14]
        self.cover_thickness = 1.3
        self.cover_squeezer_clearance = .7
        self.cover_holder_space = self.holder_size[2]
        self.cover_lip_depth = 1.5
        self.screw_hole_radius = .6  # for self-tapping
        self.screw_hole_x_offset = 6.7
        self.screw_hole_z_offset = 7.5
        self.flex_space = 2
        self.cover_midsection_x = self.handle_width + 2 * self.cover_squeezer_clearance

        self.hex_radius = 2.4
        self.hex_location = [0, self.holder_size[1] / 2 + self.holder_xyz[1], self.cap_size[2] - self.hex_radius]
        self.screw_divot_depth = .5
        self.screw_divot_radius = 1.1
        self.base_bevel = .5

        self.cover_size = [self.cap_size[0] + 2 * self.cover_thickness,
                           self.cap_size[1] + 2 * self.cover_thickness,
                           self.cover_thickness + self.holder_size[
                               2] + self.hex_radius * 2 + self.cover_clearance + 1]
        self.cover_move_z = self.cover_thickness - self.cover_size[2] / 2 + self.cover_holder_space + \
                            self.cap_size[2] + self.cover_clearance
        self.cover_xyz = [0, self.holder_size[1] / 2 + self.cover_clearance + self.holder_xyz[1],
                          -self.cover_size[2] / 2 + self.cover_thickness + 2 * self.holder_size[2] +
                          self.cover_clearance + self.holder_xyz[2]]

        self.tracking_cylinder_radius = 2
        self.bevel_offset = self.holder_size[0] / 2 - self.tracking_cylinder_radius - 1
        self.screwhead_top = .35

        # headfix paramaters
        self.bridge_thickness = 5
        self.bridge_y = 10
        self.headfix_clearance = .4
        self.bridge_width = self.cap_size[0] + 3 * self.headfix_clearance
        self.headfix_thickness = 3
        self.headfix_inner_bevel = 2
        self.headfix_outer_bevel = sqrt(3 ** 2 / 2)
        self.stereotax_bevel = 2 * sqrt(1 ** 2 / 2)
        self.headfix_screw_radius = 1.1
        self.stereotax_width = 44
        self.stereotax_bar_thickness = 4.3
        self.stereotax_bar_length = 20

        self.headfix_bar_slant = 10  # degrees

        self.screw_y = 5 / 2 + self.DOVE_DEPTH + self.PIXEL_BOTTOM[1] - \
                       self.PIXEL_PROBE_Y + self.dove_clearance
        self.SCREWHEAD_LOWER_RADIUS = 1.15
        self.SCREWHEAD_DEPTH = 1
        self.SCREWHEAD_UPPER_RADIUS = self.SCREWHEAD_DEPTH + self.SCREWHEAD_LOWER_RADIUS + .1
        self.SCREW_THREAD_RADIUS = 1.05
        self.DRIVER_WIDTH = 3
        self.SCREW_LENGTH = 16.5

        self.screw_cover_size = [self.cover_midsection_x + self.cover_thickness, self.SCREWHEAD_UPPER_RADIUS + 2.5,
                                 1]
        self.screw_cover_location = [0, self.screw_y,
                                     self.screw_cover_size[2] / 2 + self.cover_thickness + self.cover_holder_space +
                                     self.cap_size[2] + self.cover_clearance + self.cover_clearance]

        self.surgery_post_separation = 4
        self.post_diameter = .82  # 21 gauge
        self.needle_diameter = .45  # 26 gauge

        # This defines everything for the stand
        self.stand_thickness = 2
        self.inset = 1
        self.stand_ridge = .6

        self.eppendorf_height = 30
        self.stand_cover_depth = 10
        self.stand_front = 3
        self.stand_size = [self.cover_size[0] + self.stand_thickness * 2,
                           self.cover_size[1] + self.stand_thickness * 2 + self.cover_thickness + self.stand_front,
                           self.eppendorf_height + self.stand_cover_depth + 10]
        self.stand_clearance = .3
        self.cleaner_clearance = .35
        self.base_width = 30
        self.base_thickness = 3
        self.stand_base_size = [self.stand_size[0] + 2 * self.base_width,
                                self.stand_size[1] + 2 * self.base_width - self.stand_front, self.base_thickness]
        self.stand_lid_size = [self.stand_base_size[0] - 2 * self.base_thickness,
                               self.stand_base_size[1] - 2 * self.base_thickness,
                               self.stand_size[2] + 2 * self.cover_size[2]]
        self.stand_lid_thickness = 1

        self.cleaner_thickness = 1.5
        self.eppendorf_tube_diameter = 8
        self.hex_depth = 2
        self.added_cleaner_space = 1

        self.dove_bevel = .2
        self.pixel_dove_bevel = .1

        self.shield_thickness = .7

        self.ground_pin_loc = [-2.5, -4.3, 0]
        self.ground_inner_radius = .5
        self.ground_outer_radius = .6
        self.ground_cap_radius = .9

    def pixel(self):
        first_block = self.PIXEL_TOP
        second_block = self.PIXEL_BOTTOM
        probe = self.PIXEL_PROBE
        probe_location = self.PIXEL_PROBE_Y
        dovetail = [self.DOVE_INNER_WIDTH, self.DOVE_DEPTH, self.DOVE_HEIGHT]

        # This makes the object
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, location=(0, 0, 0))
        bpy.ops.transform.resize(value=(first_block[0], first_block[1], first_block[2]))
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        pixel = bpy.context.active_object
        bpy.context.active_object.name = 'pixel'
        select_verts(pixel, [-100, 100], [-100, 100], [-100, 0])
        bpy.ops.mesh.extrude_region()
        ratio = list(map(lambda x, y: x / y, second_block, first_block))
        bpy.ops.transform.resize(value=(ratio[0], .999 * ratio[1], 1))
        bpy.ops.mesh.extrude_context_move(TRANSFORM_OT_translate={"value": (0, 0, -second_block[2])})
        bpy.ops.mesh.extrude_region()
        ratio = list(map(lambda x, y: x / y, probe, second_block))
        bpy.ops.transform.resize(value=(ratio[0], ratio[1], 1))
        bpy.ops.transform.translate(value=(0, probe_location - second_block[1] / 2, 0))
        bpy.ops.mesh.extrude_context_move(TRANSFORM_OT_translate={"value": (0, 0, -probe[2])})

        select_verts(pixel, [-second_block[0] / 2, second_block[0] / 2], [second_block[1] / 2, 100],
                     [-(first_block[2] / 2 + second_block[2]), 0])
        bpy.ops.mesh.extrude_region()
        ratio = list(map(lambda x, y: x / y, dovetail, second_block))
        bpy.ops.transform.resize(value=(ratio[0], 1, ratio[2]))
        bpy.ops.transform.translate(value=(0, 0, self.DOVE_Z_SPACER - (second_block[2] - dovetail[2]) / 2))

        bpy.ops.mesh.extrude_context_move(TRANSFORM_OT_translate={"value": (0, dovetail[1], 0)})
        bpy.ops.transform.resize(value=(self.DOVE_OUTER_WIDTH / self.DOVE_INNER_WIDTH, 1, 1))

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.translate(
            value=(0, second_block[1] / 2 - probe_location, first_block[2] / 2 + second_block[2]))
        bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.transform.translate(value=self.pixel_xyz)
        return pixel

    def holder(self, shield=False):
        # This makes the piece that permanently attaches to the pixel
        holder_location = [0, self.holder_size[1] / 2, self.holder_size[2] / 2]
        holder = add_cube(self.holder_size, holder_location, 'holder')
        for x in [[0, 100], [-100, 0]]:
            select_verts(holder, x, [self.holder_size[1], 100], [-100, 100])
            bpy.ops.mesh.bevel(offset=self.bevel_offset, segments=10)
        bpy.ops.object.mode_set(mode='OBJECT')

        # This makes the dovetail cutout
        cutter_size = [self.PIXEL_BOTTOM[0] + 2 * self.dove_clearance,
                       self.PIXEL_BOTTOM[1] + self.holder_y_extension,
                       20]
        dovetail = [self.DOVE_INNER_WIDTH + 2 * self.dove_clearance, self.DOVE_DEPTH, 10]
        xyz_location = [0, cutter_size[1] / 2 - .001,
                        dovetail[2] / 2 + self.holder_space_below_dove - self.dove_clearance]
        cutter = add_cube(cutter_size, xyz_location, 'cutter')
        select_verts(cutter, [-100, 100], [0, 100], [-100, 100])
        bpy.ops.mesh.extrude_region()
        ratio = list(map(lambda x, y: x / y, dovetail, cutter_size))
        bpy.ops.transform.resize(value=(ratio[0], 1, ratio[2]))
        bpy.ops.mesh.extrude_context_move(TRANSFORM_OT_translate={"value": (0, dovetail[1], 0)})
        bpy.ops.transform.resize(value=(self.DOVE_OUTER_WIDTH / self.DOVE_INNER_WIDTH, 1, 1))
        for side in [1, -1]:
            select_verts(cutter, [side * dovetail[0] / 2, 0], [0, 100], [-100, 100])
            bpy.ops.mesh.bevel(offset=self.pixel_dove_bevel, segments=1)

        bpy.ops.object.mode_set(mode='OBJECT')

        # This makes the cap dovetail
        dove2_size = [self.dove2_width, self.dove2_depth, self.holder_size[2] + 5]
        dove2_location = [0, self.holder_size[1] - dove2_size[1] / 2 + .001,
                          self.holder_size[2] / 2 - self.holder_wall_thickness]
        cap_dovetail = add_cube(dove2_size, dove2_location, 'cap_dovetail')
        select_verts(cap_dovetail, [-dove2_size[0] / 2, dove2_size[0] / 2], [0, dove2_location[1]], [-100, 100])
        ratio = 1 + 2 * dove2_size[1] / sqrt(3) / dove2_size[0]
        bpy.ops.transform.resize(value=(ratio, 1, 1))
        boolean_modifier(holder, cap_dovetail)
        select_verts(holder, [-self.dove2_width / 2, self.dove2_width / 2], [self.holder_size[1], 100], [-100, 100])
        bpy.ops.mesh.bevel(offset=self.dove_bevel, segments=1)
        mode(('OBJECT'))

        # This makes the handle piece
        handle_size = [self.handle_width, self.handle_length, self.handle_thickness]
        handle_location = [0, handle_size[1] / 2 + cutter_size[1] + dovetail[1] + .001,
                           self.holder_size[2] - handle_size[2] / 2 - .001]
        handle = add_cube(handle_size, (0, 0, 0), 'handle')
        for side in [1, -1]:
            select_verts(handle, [side * 100, 0], [0, 100], [-100, 100])
            bpy.ops.mesh.bevel(offset=1.3, segments=1)

        mode(('OBJECT'))
        translate(handle_location)
        boolean_modifier(holder, handle, modifier='UNION')

        # # This makes the cutout for the securing hex nut
        # bpy.ops.mesh.primitive_cylinder_add(radius=self.hex_radius, depth=handle_size[2] + .005, vertices=6,
        #                                     location=handle_location, rotation=(0, 0, 0))
        # hex_cut = bpy.context.active_object
        # bpy.ops.transform.rotate(value=pi / 6, orient_axis='Z')

        # This makes the cutout for the securing hex nut
        hex_location = [0, 5 / 2 + cutter_size[1] + dovetail[1] + .001,
                        self.holder_size[2] - handle_size[2] / 2 - .001]
        # hex_location = [0, self.screw_y-self.holder_xyz[1],
        #                 self.holder_size[2] - handle_size[2] / 2 - .001]
        bpy.ops.mesh.primitive_cylinder_add(radius=self.hex_radius, depth=self.hex_depth, vertices=6,
                                            location=hex_location)
        hex_cut = bpy.context.active_object
        bpy.ops.transform.rotate(value=pi / 6, orient_axis='Z')
        select_verts(hex_cut, [-100, 100], [-100, -self.hex_radius], [-100, 100])
        translate((-self.hex_radius, 0, 0))
        mode('OBJECT')
        bpy.ops.transform.rotate(value=pi, orient_axis='Z')
        mode('OBJECT')

        # This makes the cutout for the screw to come through
        bpy.ops.mesh.primitive_cylinder_add(radius=self.SCREW_THREAD_RADIUS, depth=self.SCREW_LENGTH,
                                            location=hex_location)
        screw_cut = bpy.context.active_object

        # This applies boolean modifiers, deletes, and translates
        boolean_modifier(holder, cutter)
        boolean_modifier(holder, hex_cut)
        boolean_modifier(holder, screw_cut)

        for obj in [cutter, handle, cap_dovetail, hex_cut, screw_cut]:
            activate([obj])
            bpy.ops.object.delete(use_global=False)

        activate([holder])
        select_verts(holder, [-ratio * dove2_size[0] / 2, ratio * dove2_size[0] / 2],
                     [self.holder_size[1] - dove2_size[1], 100], [-100, 0])
        bpy.ops.mesh.bevel(offset=self.base_bevel, segments=1)

        activate([holder])
        bpy.ops.transform.translate(value=self.holder_xyz)
        if shield:
            self.add_shield(holder, shield_height=self.holder_size[2] + 1, radius=self.holder_size[0] / 2 + 2,
                            location=(0, 1, self.holder_size[2] / 2 + 3))

        return holder

    def cap(self, shield=False):
        # This makes the head cap that is permanently cemented to the skull
        cap_location = [0, 0, self.cap_size[2] / 2]
        cap = add_cube(self.cap_size, cap_location, 'cap')

        # This bevels the back corners
        for side in [-1, 1]:
            select_verts(cap, [0, side * 100], [-100, 100], [-100, 0])
            bpy.ops.mesh.bevel(offset=self.cap_bottom_bevel, segments=1)
            select_verts(cap, [0, side * 100], [0, 100], [-100, 100])
            bpy.ops.mesh.bevel(offset=1, segments=1)

        select_verts(cap, [-100, 100], [0, 100], [-100, 0])
        bpy.ops.mesh.bevel(offset=1.5, segments=1)

        bpy.ops.object.mode_set(mode='OBJECT')

        # This makes the head fixation piece
        head_fix_size = [x for x in self.head_fix_dims]
        head_fix_size[0] = self.cap_size[0] + 2 * head_fix_size[0]
        head_fix_location = [0, 0, head_fix_size[2] / 2 + .001 + self.headfix_bar_z]
        head_fix = add_cube(head_fix_size, head_fix_location, 'head_fix')
        select_verts(head_fix, [-100, 100], [0, -100], [head_fix_location[2], 100])
        bpy.ops.mesh.bevel(offset=self.stereotax_bevel, affect='VERTICES')

        bpy.ops.object.mode_set(mode='OBJECT')

        # This makes the mid section cutout
        hole_size = list(map(lambda x: x + 2 * self.cap_clearance, self.holder_size))
        hole_location = [0, 0, hole_size[2] / 2 + self.cap_size[2] - hole_size[2] + self.cap_clearance]
        hole = add_cube(hole_size, hole_location, 'hole')
        for x in [[0, 100], [-100, 0]]:
            select_verts(hole, x, [0, 100], [-100, 100])
            bpy.ops.mesh.bevel(offset=self.bevel_offset, segments=10)
        bpy.ops.object.mode_set(mode='OBJECT')

        clear_size = list(map(lambda x: x - 2 * self.cap_bottom_lip, self.holder_size))
        clear_location = [0, 0, clear_size[2] / 2 + self.cap_bottom_thickness]
        clear = add_cube(clear_size, clear_location, 'clear')

        # This makes the cylinders
        bpy.ops.mesh.primitive_cylinder_add(radius=self.lip_outer_radius, depth=self.lip_height,
                                            location=(0, 0, -self.lip_height / 2 + .001))
        outer_lip = bpy.context.active_object
        bpy.ops.mesh.primitive_cylinder_add(radius=self.lip_inner_radius, depth=15, location=(0, 0, 0))
        inner_lip = bpy.context.active_object

        # This makes the cap dovetail
        dove2_size = [self.dove2_width - 2 * self.dove2_clearance, self.dove2_depth - self.dove2_clearance,
                      self.holder_size[2]]
        dove2_location = [0, self.holder_size[1] - dove2_size[1] / 2 + .001,
                          self.holder_size[2] / 2 - self.holder_wall_thickness]
        dove2_location = [x + y for x, y in zip(dove2_location, self.holder_xyz)]
        cap_dovetail = add_cube(dove2_size, dove2_location, 'cap_dovetail')
        select_verts(cap_dovetail, [-dove2_size[0] / 2, dove2_size[0] / 2], [0, dove2_location[1]], [-100, 100])
        ratio = 1 + 2 * dove2_size[1] / sqrt(3) / dove2_size[0]
        bpy.ops.transform.resize(value=(ratio, 1, 1))
        bpy.ops.mesh.bevel(offset=self.dove_bevel, segments=1)
        select_verts(cap_dovetail, [-100, 100], [dove2_location[1], 100], [-100, 100])
        bpy.ops.mesh.extrude_context_move(TRANSFORM_OT_translate={"value": (0, self.cap_wall_thickness, 0)})
        ratio = 1 - 2 * self.cap_wall_thickness / sqrt(3) / dove2_size[0]
        bpy.ops.transform.resize(value=(ratio, 1, 1))
        select_verts(cap_dovetail, [-dove2_size[0] / 2, dove2_size[0] / 2], [0, dove2_location[1]], [-100, 100])

        bpy.ops.object.mode_set(mode='OBJECT')

        # This makes the cut away window rectangle
        window_size = [self.cap_window_width,
                       self.cap_wall_thickness + self.cap_bottom_lip + self.cap_clearance + .2,
                       self.cap_size[2]]
        window_location = [0, -self.cap_size[1] / 2 + window_size[1] / 2 - .001,
                           self.cap_size[2] / 2 + self.cap_window_base_thickness]
        window = add_cube(window_size, window_location, 'window')

        # This makes the cutout for the securing hex screw
        oval_amount = 1.1
        bpy.ops.mesh.primitive_cylinder_add(radius=self.screw_divot_radius, depth=self.screw_divot_depth + .001,
                                            location=(0, 0, 0), rotation=(0, pi / 2, 0))
        divot_cut1 = bpy.context.active_object
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        select_verts(divot_cut1, [-100, 0], [-100, 100], [-100, 100])
        bpy.ops.transform.resize(value=(1, .8, .8))
        bpy.ops.object.mode_set(mode='OBJECT')
        resize((1, 1, oval_amount))
        bpy.ops.transform.translate(value=(self.cap_size[0] / 2 - self.screw_divot_depth / 2, 0, 0))
        bpy.ops.transform.translate(value=(self.hex_location))

        bpy.ops.mesh.primitive_cylinder_add(radius=self.screw_divot_radius, depth=self.screw_divot_depth + .001,
                                            location=(0, 0, 0), rotation=(0, pi / 2, 0))
        divot_cut2 = bpy.context.active_object
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        select_verts(divot_cut2, [0, 100], [-100, 100], [-100, 100])
        bpy.ops.transform.resize(value=(1, .8, .8))
        bpy.ops.object.mode_set(mode='OBJECT')
        resize((1, 1, oval_amount))
        bpy.ops.transform.translate(value=(-self.cap_size[0] / 2 + self.screw_divot_depth / 2, 0, 0))
        bpy.ops.transform.translate(value=(self.hex_location))

        # This makes the cutaway for the back where the holder hex sinks in
        handle_size = [self.handle_width + self.cap_clearance * 4, self.handle_length,
                       self.handle_thickness + self.cap_clearance * 2]
        handle_location = [0, handle_size[1] / 2, self.cap_size[2] - handle_size[2] / 2 + self.cap_clearance]
        handle_cut = add_cube(handle_size, handle_location, 'handle_cut')

        loc = [0, self.screw_y, self.cover_size[2] / 2 + self.cover_move_z - self.SCREW_LENGTH / 2]
        bpy.ops.mesh.primitive_cylinder_add(radius=self.SCREW_THREAD_RADIUS, depth=self.SCREW_LENGTH,
                                            location=loc, rotation=(0, 0, 0))
        screw_cut = bpy.context.active_object

        # # This adds a square spot for the ground to plug into
        # plug_inner_size = [self.plug_width, self.plug_width, self.plug_depth]
        # plug_outer_size = [plug_inner_size[0] + 2 * self.plug_wall, plug_inner_size[1] + 2 * self.plug_wall,
        #                    plug_inner_size[2] + self.plug_wall]
        # inner_plug = add_cube(plug_inner_size, (0, 0, 0), 'inner_plug')
        # outer_plug = add_cube(plug_outer_size, (0, 0, 0), 'outer_plug')
        # activate([inner_plug, outer_plug])
        # plug_location = [self.wire_location[0], self.wire_location[1], self.cap_size[2] - plug_outer_size[2] / 2 + .01]
        # translate(plug_location)
        # activate([inner_plug])
        # translate((0, 0, self.plug_wall / 2 + .01))
        #
        # boolean_modifier(cap, outer_plug, 'UNION')
        # boolean_modifier(cap, inner_plug)

        # # This cuts a line along the front for the ground wire to be glued into
        # wire_size = [self.ground_wire_depth, self.ground_wire_depth, self.cap_size[2] * 2]
        # wire = add_cube(wire_size, (0, 0, 0), 'wire')
        # rotate(pi / 4, 'Z')
        # translate(self.wire_location)
        # boolean_modifier(cap, wire)

        # This makes a model for the gold ground
        height = self.cap_size[2] + 2
        ground = add_cylinder(self.ground_cap_radius, height, 32, 'ground')
        translate(self.ground_pin_loc)
        translate([0, 0, height / 2 - 1])

        # This makes the cut out for the screws to secure the cover
        cover_screw = add_cylinder(self.SCREW_THREAD_RADIUS, self.cap_size[0] * 1.1, 100, 'cover_screw')
        rotate(pi / 2, 'Y')
        translate(self.hex_location)

        # This applies boolean modifiers, deletes, and translates
        boolean_modifier(cap, head_fix, modifier='UNION')
        boolean_modifier(cap, hole)
        boolean_modifier(cap, clear)
        boolean_modifier(cap, window)

        bpy.ops.transform.translate(value=(0, hole_size[1] / 2 + self.holder_xyz[1] - self.cap_clearance, 0))

        boolean_modifier(cap, outer_lip, modifier='UNION')
        boolean_modifier(cap, inner_lip)
        boolean_modifier(cap, cap_dovetail, modifier='UNION')
        # boolean_modifier(cap, divot_cut1)
        # boolean_modifier(cap, divot_cut2)
        boolean_modifier(cap, handle_cut)
        boolean_modifier(cap, screw_cut)
        boolean_modifier(cap, ground)
        boolean_modifier(cap, cover_screw)

        delete([head_fix, hole, clear, outer_lip, inner_lip, screw_cut, cover_screw,
                cap_dovetail, window, divot_cut1, divot_cut2, handle_cut, ground])

        if shield:
            height = self.cap_size[2] + self.lip_height + 1
            self.add_shield(cap, shield_height=height, radius=head_fix_size[0] / 2 + 1,
                            location=[0, 0, height / 2 - self.lip_height])

        return cap

    def cover(self, shield=False):
        # This makes the piece that holds the headstage and goes around the head cap
        cover = add_cube(self.cover_size, [0, 0, 0], 'cover')

        # This makes the stability bar
        bar_size = [self.cover_size[0] - self.cover_thickness, self.cover_thickness / 2, self.cover_thickness]
        bar_location = [0, -self.cover_size[1] / 2 - bar_size[1] / 2 + .01,
                        -self.cover_size[2] / 2 + bar_size[2] / 2 + .02]
        bar = add_cube(bar_size, bar_location, 'bar')
        for side in [1, -1]:
            select_verts(bar, [side * 100, 0], [bar_location[1], -100], [-100, 100])
            bpy.ops.mesh.bevel(offset=self.cover_thickness * .8, segments=1)
        # boolean_modifier(cover, bar, 'UNION')
        mode('OBJECT')

        # This makes the midsection cutter
        midsection_size = [self.cover_midsection_x, self.cover_size[1], self.cover_size[2]]
        midsection_location = [0, self.cover_thickness, -self.cover_thickness - .001]
        midsection = add_cube(midsection_size, midsection_location, 'midsection')
        # for side in [1, -1]:
        #     select_verts(midsection, [side * 100, 0], [midsection_location[1], -100], [-100, 100])
        #     bpy.ops.mesh.bevel(offset=self.cover_clearance + .5, segments=1)
        boolean_modifier(cover, midsection)

        # This makes the cap cutter
        size = list(map(lambda x: x + 2 * self.cover_clearance, self.cap_size))
        cap_cutter_location = [0, self.cover_size[1] / 2 - size[1] / 2 - self.cover_thickness,
                               self.cover_size[2] / 2 - size[
                                   2] / 2 - self.cover_thickness - self.cover_holder_space]
        cap_cutter = add_cube(size, cap_cutter_location, 'cap_cutter')

        boolean_modifier(cover, cap_cutter)

        # This makes the holder cutter
        size = list(map(lambda x: x + 2 * self.cover_clearance, self.holder_size))
        holder_cutter_location = [0, cap_cutter_location[1],
                                  self.cover_size[2] / 2 - size[2] / 2 - self.cover_thickness]
        holder_cutter = add_cube(size, holder_cutter_location, 'holder_cutter')
        for x in [[0, 100], [-100, 0]]:
            select_verts(holder_cutter, x, [cap_cutter_location[1], 100], [-100, 100])
            bpy.ops.mesh.bevel(offset=self.bevel_offset, segments=10)
        bpy.ops.object.mode_set(mode='OBJECT')

        boolean_modifier(cover, holder_cutter)

        # This makes the cut away blocks
        cut = [(self.cover_size[0] - self.holder_size[0]) / 2 - self.cover_thickness,
               self.cover_size[1] - 2 * self.cover_thickness - self.headstage_size[1],
               self.cover_holder_space]
        r1_location = list(map(lambda x, y: x - y, self.cover_size, cut))
        r1_location[1] = 0
        r1_size = [self.cover_size[0], self.cover_size[1] + 1, self.cover_size[2]]
        cut_away_r1 = add_cube(r1_size, r1_location, 'cut_away_r1')
        select_verts(cut_away_r1, [-100, r1_location[0]], [-100, 100], [-100, r1_location[2]])
        offset = (self.cap_size[0] - self.holder_size[0]) / 2 + .1
        bpy.ops.mesh.bevel(offset=offset)
        select_verts(cut_away_r1, [r1_location[0], 100], [-100, 100], [-100, r1_location[2]])
        bpy.ops.mesh.bevel(offset=offset)

        boolean_modifier(cover, cut_away_r1)
        activate([cut_away_r1])
        bpy.ops.transform.translate(value=(-2 * r1_location[0], .001, 0))
        boolean_modifier(cover, cut_away_r1)

        # This makes the bottom bevel
        select_verts(cover,
                     [-self.cap_size[0] / 2 - self.cover_clearance, self.cap_size[0] / 2 + self.cover_clearance],
                     [-self.cover_size[1] / 2 + self.cover_thickness / 2,
                      self.cover_size[1] / 2 - self.cover_thickness / 2],
                     [-100, -self.cover_size[2] / 2])
        bpy.ops.mesh.bevel(offset=self.base_bevel, segments=1)
        # select_verts(cover, [-self.cap_size[0] / 2 - self.cover_clearance, 0],
        #              [-self.cover_size[1] / 2 + self.cover_thickness / 2, self.cover_size[1] / 2 - self.cover_thickness / 2],
        #              [-100, -self.cover_size[2] / 2])
        # bpy.ops.mesh.bevel(offset=self.base_bevel, segments=1)

        # This makes the headstage mount
        bpy.ops.object.mode_set(mode='OBJECT')
        mount_z_separation = 1
        mount_y_separation = 1
        mount_wing_height = 3
        mount_wing_depth = 2.5
        mount_wing_x = [.1, .2, 2]
        mount_size = [self.holder_size[0] + self.cover_thickness * 2 - .002, self.cover_thickness,
                      self.headstage_size[2]]
        mount_location = [0, -self.cover_size[1] / 2 - mount_size[1] / 2 - mount_y_separation + .001,
                          self.cover_size[2] / 2 + mount_size[2] / 2 + mount_z_separation - .001]
        mount = add_cube(mount_size, (0, 0, 0), 'mount')
        translate(mount_location)
        for side in [1, -1]:
            select_verts(mount, [side * 100, 0], [-100, 100], [-100, 100])
            extrude_move((side * mount_wing_x[0], 0, mount_size[2] / 2 - mount_wing_height / 2))
            resize((1, 1, mount_wing_height / mount_size[2]))
            extrude_move((side * mount_wing_x[1], 0, 0))
            extrude_move((side * mount_wing_x[2], 0, 0))
            select_verts(mount, [side * 100, side * (mount_size[0] / 2 + mount_wing_x[0] + mount_wing_x[1])],
                         [-100, 0],
                         [0, 100])
            translate((0, -mount_wing_depth, 0))

        select_verts(mount, [-100, 100], [-100, -mount_wing_depth], [0, mount_size[2] / 2 - mount_wing_height])
        bpy.ops.mesh.bevel(offset=mount_wing_depth / 3, segments=1)

        select_verts(mount, [-100, 100], [-100, 100], [-100, 0])
        extrude_move((0, (mount_y_separation + self.cover_thickness) / 2, -mount_z_separation))
        resize((1, (mount_size[1] + mount_y_separation + self.cover_thickness) / mount_size[1], 1))
        extrude_move((0, 0, -1))
        extrude_move((0, (mount_y_separation + mount_size[1]) / 2, -2))
        resize((1, self.cover_thickness / (mount_size[1] + mount_y_separation + self.cover_thickness), 1))
        boolean_modifier(cover, mount, modifier='UNION')

        # This makes the screw holes
        bpy.ops.mesh.primitive_cylinder_add(radius=self.screw_hole_radius, depth=15,
                                            location=(
                                                self.screw_hole_x_offset, -self.cover_size[1] / 2,
                                                self.screw_hole_z_offset))
        bpy.ops.transform.rotate(value=pi / 2, orient_axis='X')
        translate((0, 0, mount_z_separation + mount_size[2]))
        screw_hole = bpy.context.active_object
        boolean_modifier(cover, screw_hole)
        activate([screw_hole])
        bpy.ops.transform.translate(value=(-2 * self.screw_hole_x_offset, 0, 0))
        boolean_modifier(cover, screw_hole)

        activate([cover])
        bpy.ops.transform.translate(value=self.cover_xyz)

        # This makes the pixel cutter
        y_fine_tune = .6
        size = [self.PIXEL_TOP[0] + 2 * self.cover_clearance,
                self.cover_clearance + self.PIXEL_TOP[1] + self.holder_y_extension +
                self.cap_wall_thickness + self.cover_thickness + self.cap_clearance + y_fine_tune,
                self.cover_size[2]]
        location = [0, -self.PIXEL_TOP[1] / 2 + 1.1 - self.PIXEL_PROBE_Y - size[
            1] / 2 + self.cover_clearance + y_fine_tune,
                    self.cover_xyz[2] + self.cover_thickness + .02 + 1]
        pixel_cutter = add_cube(size, location, 'pixel_cutter')
        boolean_modifier(cover, pixel_cutter)
        front_section_y = self.cover_size[1] / 2 + self.cover_xyz[1] - (size[1] / 2 + location[1])

        # This makes the covers for the hexes
        size = [self.cover_thickness, self.hex_radius * 2 + 1, self.hex_radius * 2 + 2]
        for side in [1, -1]:
            loc = [side * (self.cover_size[0] / 2 + self.cover_thickness / 2 - .01), self.hex_location[1],
                   self.hex_location[2] + .5]
            hex_cover = add_cube(size, (0, 0, 0), 'hex_cover')
            translate(loc)
            select_verts(hex_cover, [0, side * 100], [-100, 100], [0, 100])
            translate((0, 0, -self.cover_thickness))
            # boolean_modifier(cover, hex_cover, 'UNION')
            delete([hex_cover])

        # This makes the cutout for the securing hex nut
        bpy.ops.mesh.primitive_cylinder_add(radius=self.hex_radius,
                                            depth=self.cover_size[
                                                      0] - self.cover_thickness * 2 + self.hex_depth * 2,
                                            vertices=6,
                                            location=self.hex_location, rotation=(0, pi / 2, 0))
        hex_cut = bpy.context.active_object
        bpy.ops.transform.rotate(value=pi / 6, orient_axis='X')
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        resize((1, 1, 5 / 4.8))
        # boolean_modifier(cover, hex_cut)

        # This makes the cut out for the screws to secure the cover
        bpy.ops.mesh.primitive_cylinder_add(radius=self.SCREW_THREAD_RADIUS,  # * 1.3,
                                            depth=self.cover_size[0] + self.hex_depth * 2,
                                            location=self.hex_location, rotation=(0, pi / 2, 0))
        hex_screw = bpy.context.active_object
        boolean_modifier(cover, hex_screw)

        # This adds the cover for the screw
        added_thickness = self.cover_thickness
        size = [self.SCREWHEAD_UPPER_RADIUS * 2 + 2 * self.cover_thickness, front_section_y - .02, added_thickness]
        loc = [0, self.cover_xyz[1] + self.cover_size[1] / 2 - size[1] / 2 - .01,
               self.cover_xyz[2] + self.cover_size[2] / 2 + size[2] / 2 - .001]
        screw_cover = add_cube(size, loc, 'screw_cover')

        bpy.ops.mesh.primitive_cylinder_add(radius=self.DRIVER_WIDTH / 2, depth=self.SCREW_LENGTH,
                                            location=[0, self.screw_y,
                                                      self.cover_xyz[2] + self.cover_size[
                                                          2] / 2 - self.SCREWHEAD_DEPTH / 2],
                                            rotation=(0, 0, 0))
        screw = bpy.context.active_object
        boolean_modifier(screw_cover, screw)
        boolean_modifier(cover, screw_cover, 'UNION')

        # This makes the cutout for the screw head
        loc = [0, self.screw_y, self.cover_xyz[2] + self.cover_size[2] / 2 - self.SCREWHEAD_DEPTH / 2]
        bpy.ops.mesh.primitive_cylinder_add(radius=self.SCREWHEAD_UPPER_RADIUS, depth=self.SCREWHEAD_DEPTH + .001,
                                            vertices=32,
                                            location=loc, rotation=(0, 0, 0))
        screwhead_cut = bpy.context.active_object
        select_verts(screwhead_cut, [-100, 100], [-100, 100], [-100, 0])
        ratio = self.SCREWHEAD_LOWER_RADIUS / self.SCREWHEAD_UPPER_RADIUS
        bpy.ops.transform.resize(value=(ratio, ratio, 1))
        select_verts(screwhead_cut, [-100, 100], [-100, 100], [-100, 0])
        bpy.ops.mesh.extrude_context_move(TRANSFORM_OT_translate={"value": (0, 0, -5)})
        select_verts(screwhead_cut, [-100, 100], [-100, 100], [100, 0])
        bpy.ops.mesh.extrude_context_move(TRANSFORM_OT_translate={"value": (0, 0, self.screwhead_top)})
        select_verts(screwhead_cut, [-100, 100], [0, 100], [-100, 100])
        extrude_move((0, 5, 0))
        boolean_modifier(cover, screwhead_cut)

        # This cuts out the space for the ground pin
        pin = add_cylinder(self.ground_outer_radius, 3, 32, 'pin')
        inner_pin = add_cylinder(self.ground_inner_radius, 5, 32, 'outer_pin')
        boolean_modifier(pin, inner_pin, 'UNION')
        translate(self.ground_pin_loc)
        translate([0, 0, 9])
        # boolean_modifier(cover, pin)

        delete([bar, midsection, cap_cutter, holder_cutter, cut_away_r1, mount, screw_hole, screwhead_cut,
                pixel_cutter,
                screw_cover, screw, hex_screw, hex_cut, inner_pin, pin])

        # screw_test = add_cube(self.cover_size, [0, 0, 0], 'screw_test')
        # bpy.ops.transform.translate(value=self.cover_xyz)
        # bpy.ops.transform.translate(
        #     value=(0, self.cover_size[1] - front_section_y + .002, self.cover_size[2] - self.SCREWHEAD_DEPTH - 1))
        # boolean_modifier(screw_test, cover, modifier='INTERSECT')
        # activate([cover])
        # bpy.ops.object.delete(use_global=False)

        if shield:
            self.add_shield(cover, shield_height=self.cover_size[2] + 2, radius=self.cover_size[0] / 2 + 2 + 1.5,
                            location=self.cover_xyz)
        return cover

    def stopper(self, shield=False):
        # This makes the piece that permanently attaches to the pixel
        holder_location = [0, self.holder_size[1] / 2, self.holder_size[2] / 2]
        stopper = add_cube(self.holder_size, holder_location, 'stopper')
        for x in [[0, 100], [-100, 0]]:
            select_verts(stopper, x, [self.holder_size[1], 100], [-100, 100])
            bpy.ops.mesh.bevel(offset=self.bevel_offset, segments=10)
        bpy.ops.object.mode_set(mode='OBJECT')

        # This makes the square that inserts into the bottom section
        clear_size = list(map(lambda x: x - 4 * self.cap_bottom_lip, self.holder_size))
        clear_size[2] = self.holder_size[2] / 3
        clear_location = [0, .6, clear_size[2] / 2 + self.cap_bottom_thickness + self.cap_clearance]
        clear = add_cube(clear_size, clear_location, 'clear')

        # This makes the cap dovetail
        dove2_size = [self.dove2_width, self.dove2_depth, self.holder_size[2] + 5]
        dove2_location = [0, self.holder_size[1] - dove2_size[1] / 2 + .001,
                          self.holder_size[2] / 2 - self.holder_wall_thickness]
        cap_dovetail = add_cube(dove2_size, dove2_location, 'cap_dovetail')
        select_verts(cap_dovetail, [-dove2_size[0] / 2, dove2_size[0] / 2], [0, dove2_location[1]], [-100, 100])
        ratio = 1 + 2 * dove2_size[1] / sqrt(3) / dove2_size[0]
        bpy.ops.transform.resize(value=(ratio, 1, 1))
        boolean_modifier(stopper, cap_dovetail)
        select_verts(stopper, [-self.dove2_width / 2, self.dove2_width / 2], [self.holder_size[1], 100],
                     [-100, 100])
        bpy.ops.mesh.bevel(offset=self.dove_bevel, segments=1)
        mode(('OBJECT'))

        # This makes the cutout for the securing hex nut
        embed_depth = self.holder_size[2] / 2
        bpy.ops.mesh.primitive_cylinder_add(radius=self.hex_radius, depth=self.hex_depth, vertices=6,
                                            location=(0, 0, self.holder_size[2] - embed_depth))
        hex_cut = bpy.context.active_object
        bpy.ops.transform.rotate(value=pi / 6, orient_axis='Z')
        hex_y = (self.holder_size[1] - self.dove2_depth) / 2
        bpy.ops.transform.translate(value=(0, hex_y, 0))
        select_verts(hex_cut, [-100, 100], [-100, -self.hex_radius], [-100, 100])
        translate((-self.hex_radius, 0, 0))
        mode('OBJECT')

        # This makes the cutout for the screw to come through
        loc = (0, hex_y, self.SCREW_LENGTH / 2 + self.holder_size[2] - embed_depth)
        bpy.ops.mesh.primitive_cylinder_add(radius=self.SCREW_THREAD_RADIUS, depth=self.SCREW_LENGTH, location=loc)
        screw_cut = bpy.context.active_object

        # This applies boolean modifiers, deletes, and translates
        boolean_modifier(stopper, hex_cut)
        boolean_modifier(stopper, screw_cut)

        for obj in [cap_dovetail, hex_cut, screw_cut]:
            activate([obj])
            bpy.ops.object.delete(use_global=False)

        activate([stopper])
        select_verts(stopper, [-ratio * dove2_size[0] / 2, ratio * dove2_size[0] / 2],
                     [self.holder_size[1] - dove2_size[1], 100], [-100, 0])
        bpy.ops.mesh.bevel(offset=self.base_bevel, segments=1)

        activate([stopper])
        bpy.ops.transform.translate(value=self.holder_xyz)
        boolean_modifier(stopper, clear, modifier='UNION')
        activate([clear])
        bpy.ops.object.delete(use_global=False)

        if shield:
            self.add_shield(stopper, shield_height=self.holder_size[2] + 1, radius=self.holder_size[0] / 2 + 2,
                            location=(0, 1, self.holder_size[2] / 2 + 3))

        return stopper

    def stabber(self, shield=False):
        # This makes the piece that permanently attaches to the pixel
        stabber_location = [0, self.holder_size[1] / 2, self.holder_size[2] / 2]
        stabber = add_cube(self.holder_size, stabber_location, 'stabber')
        for x in [[0, 100], [-100, 0]]:
            select_verts(stabber, x, [self.holder_size[1], 100], [-100, 100])
            bpy.ops.mesh.bevel(offset=self.bevel_offset, segments=10)
        bpy.ops.object.mode_set(mode='OBJECT')

        # This makes the dovetail cutout
        cutter_size = [self.PIXEL_BOTTOM[0] + 2 * self.dove_clearance,
                       self.PIXEL_BOTTOM[1] + self.holder_y_extension,
                       20]
        dovetail = [self.DOVE_INNER_WIDTH + 2 * self.dove_clearance, self.DOVE_DEPTH, 10]
        xyz_location = [0, cutter_size[1] / 2 - .001,
                        dovetail[2] / 2 + self.holder_space_below_dove - self.dove_clearance]
        cutter = add_cube(cutter_size, xyz_location, 'cutter')
        select_verts(cutter, [-100, 100], [0, 100], [-100, 100])
        bpy.ops.mesh.extrude_region()
        ratio = list(map(lambda x, y: x / y, dovetail, cutter_size))
        bpy.ops.transform.resize(value=(ratio[0], 1, ratio[2]))
        bpy.ops.mesh.extrude_context_move(TRANSFORM_OT_translate={"value": (0, dovetail[1], 0)})
        bpy.ops.transform.resize(value=(self.DOVE_OUTER_WIDTH / self.DOVE_INNER_WIDTH, 1, 1))
        for side in [1, -1]:
            select_verts(cutter, [side * dovetail[0] / 2, 0], [0, 100], [-100, 100])
            bpy.ops.mesh.bevel(offset=self.pixel_dove_bevel, segments=1)

        bpy.ops.object.mode_set(mode='OBJECT')

        # This makes the needle cut pieces
        cut_size = [self.holder_size[0] - 2, 3, self.holder_size[2] + 1]
        cut_location = [0, -cut_size[1] / 2 - self.holder_xyz[1], self.holder_size[2] / 2]
        cut = add_cube(cut_size, cut_location, 'cut')
        boolean_modifier(stabber, cut)

        needle_size = [self.needle_diameter, self.needle_diameter, self.holder_size[2] + 1]
        needle_location = [0, 0, self.holder_size[2] / 2]
        needle = add_cube(needle_size, needle_location, 'needle')
        bpy.ops.transform.rotate(value=pi / 4, orient_axis='Z')
        bpy.ops.transform.translate(value=[0, -self.holder_xyz[1] + .001, 0])
        boolean_modifier(stabber, needle)

        delete([cut, needle])

        # This makes the cap dovetail
        dove2_size = [self.dove2_width, self.dove2_depth, self.holder_size[2] + 5]
        dove2_location = [0, self.holder_size[1] - dove2_size[1] / 2 + .001,
                          self.holder_size[2] / 2 - self.holder_wall_thickness]
        cap_dovetail = add_cube(dove2_size, dove2_location, 'cap_dovetail')
        select_verts(cap_dovetail, [-dove2_size[0] / 2, dove2_size[0] / 2], [0, dove2_location[1]], [-100, 100])
        ratio = 1 + 2 * dove2_size[1] / sqrt(3) / dove2_size[0]
        bpy.ops.transform.resize(value=(ratio, 1, 1))
        boolean_modifier(stabber, cap_dovetail)
        select_verts(stabber, [-self.dove2_width / 2, self.dove2_width / 2], [self.holder_size[1], 100],
                     [-100, 100])
        bpy.ops.mesh.bevel(offset=self.dove_bevel, segments=1)
        mode(('OBJECT'))

        # This makes the handle piece
        handle_size = [self.handle_width, self.handle_length, self.handle_thickness]
        handle_location = [0, handle_size[1] / 2 + cutter_size[1] + dovetail[1] + .001,
                           self.holder_size[2] - handle_size[2] / 2 - .001]
        handle = add_cube(handle_size, (0, 0, 0), 'handle')
        for side in [1, -1]:
            select_verts(handle, [side * 100, 0], [0, 100], [-100, 100])
            bpy.ops.mesh.bevel(offset=1.3, segments=1)

        mode(('OBJECT'))
        translate(handle_location)
        boolean_modifier(stabber, handle, modifier='UNION')

        # This makes the cutout for the securing hex nut
        hex_location = [0, 5 / 2 + cutter_size[1] + dovetail[1] + .001,
                        self.holder_size[2] - handle_size[2] / 2 - .001]
        # hex_location = [0, self.screw_y-self.holder_xyz[1],
        #                 self.holder_size[2] - handle_size[2] / 2 - .001]
        bpy.ops.mesh.primitive_cylinder_add(radius=self.hex_radius, depth=self.hex_depth, vertices=6,
                                            location=hex_location)
        hex_cut = bpy.context.active_object
        bpy.ops.transform.rotate(value=pi / 6, orient_axis='Z')
        select_verts(hex_cut, [-100, 100], [-100, -self.hex_radius], [-100, 100])
        translate((-self.hex_radius, 0, 0))
        mode('OBJECT')
        bpy.ops.transform.rotate(value=pi, orient_axis='Z')
        mode('OBJECT')

        # This makes the cutout for the screw to come through
        bpy.ops.mesh.primitive_cylinder_add(radius=self.SCREW_THREAD_RADIUS, depth=self.SCREW_LENGTH,
                                            location=hex_location)
        screw_cut = bpy.context.active_object

        # This applies boolean modifiers, deletes, and translates
        boolean_modifier(stabber, hex_cut)
        boolean_modifier(stabber, screw_cut)

        for obj in [cutter, handle, cap_dovetail, hex_cut, screw_cut]:
            activate([obj])
            bpy.ops.object.delete(use_global=False)

        activate([stabber])
        select_verts(stabber, [-ratio * dove2_size[0] / 2, ratio * dove2_size[0] / 2],
                     [self.holder_size[1] - dove2_size[1], 100], [-100, 0])
        bpy.ops.mesh.bevel(offset=self.base_bevel, segments=1)

        activate([stabber])
        bpy.ops.transform.translate(value=self.holder_xyz)
        if shield:
            self.add_shield(stabber, shield_height=self.holder_size[2] + 1, radius=self.holder_size[0] / 2 + 2,
                            location=(0, 2, self.holder_size[2] / 2 + 3))

    def surgery(self, shield=False):
        # This makes the piece that permanently attaches to the pixel
        holder_location = [0, self.holder_size[1] / 2, self.holder_size[2] / 2]
        surgery = add_cube(self.holder_size, holder_location, 'surgery')
        for x in [[0, 100], [-100, 0]]:
            select_verts(surgery, x, [self.holder_size[1], 100], [-100, 100])
            bpy.ops.mesh.bevel(offset=self.bevel_offset, segments=10)
        bpy.ops.object.mode_set(mode='OBJECT')

        # This makes the cap dovetail
        dove2_size = [self.dove2_width, self.dove2_depth, self.holder_size[2] + 5]
        dove2_location = [0, self.holder_size[1] - dove2_size[1] / 2 + .001,
                          self.holder_size[2] / 2 - self.holder_wall_thickness]
        cap_dovetail = add_cube(dove2_size, dove2_location, 'cap_dovetail')
        select_verts(cap_dovetail, [-dove2_size[0] / 2, dove2_size[0] / 2], [0, dove2_location[1]], [-100, 100])
        ratio = 1 + 2 * dove2_size[1] / sqrt(3) / dove2_size[0]
        bpy.ops.transform.resize(value=(ratio, 1, 1))
        boolean_modifier(surgery, cap_dovetail)
        select_verts(surgery, [-self.dove2_width / 2, self.dove2_width / 2], [self.holder_size[1], 100],
                     [-100, 100])
        bpy.ops.mesh.bevel(offset=self.dove_bevel, segments=1)
        mode(('OBJECT'))

        # This makes the needle cut pieces
        cut_size = [self.holder_size[0] + 1, self.holder_xyz[1] * 2, self.holder_size[2] + 1]
        cut_location = [0, 0, self.holder_size[2] / 2]
        cut = add_cube(cut_size, cut_location, 'cut')

        post_size = [self.post_diameter, self.post_diameter, self.holder_size[2] + 1]
        post_location = [0, 0, self.holder_size[2] / 2]
        post = add_cube(post_size, post_location, 'post')
        bpy.ops.transform.rotate(value=pi / 4, orient_axis='Z')
        bpy.ops.transform.translate(value=[self.surgery_post_separation / 2, -self.holder_xyz[1] + .001, 0])
        boolean_modifier(surgery, post)
        activate([post])
        bpy.ops.transform.translate(value=[-self.surgery_post_separation, 0, 0])
        boolean_modifier(surgery, post)

        needle_size = [self.needle_diameter, self.needle_diameter, self.holder_size[2] + 1]
        needle_location = [0, 0, self.holder_size[2] / 2]
        needle = add_cube(needle_size, needle_location, 'needle')
        bpy.ops.transform.rotate(value=pi / 4, orient_axis='Z')
        bpy.ops.transform.translate(value=[0, -self.holder_xyz[1] + .001, 0])
        boolean_modifier(surgery, needle)

        # This applies boolean modifiers, deletes, and translates
        boolean_modifier(surgery, cut)

        for obj in [cap_dovetail, cut, post, needle]:
            activate([obj])
            bpy.ops.object.delete(use_global=False)

        activate([surgery])
        select_verts(surgery, [-ratio * dove2_size[0] / 2, ratio * dove2_size[0] / 2],
                     [self.holder_size[1] - dove2_size[1], 100], [-100, 0])
        bpy.ops.mesh.bevel(offset=self.base_bevel, segments=1)

        activate([surgery])

        height = self.holder_size[2] + 1
        radius = self.holder_size[0] / 2 + 1

        activate([surgery])
        bpy.ops.transform.translate(value=self.holder_xyz)
        if shield:
            self.add_shield(surgery, shield_height=self.holder_size[2] + 1, radius=self.holder_size[0] / 2 + 2,
                            location=(0, 1, self.holder_size[2] / 2 + 3))

        return surgery

    def add_shield(self, obj, shield_height=1, radius=1, location=(0, 0, 0)):
        shield = add_cylinder(radius + self.shield_thickness, shield_height, 32, 'shield')
        shield_cut = add_cylinder(radius, shield_height + 1, 32, 'shield_cut')
        boolean_modifier(shield, shield_cut)
        activate([shield])
        translate(location)
        boolean_modifier(obj, shield, 'UNION')
        delete([shield_cut, shield])

    def tube(self, play=False):
        radius = 18
        length = 100
        thickness = 2
        ceiling_thickness = 2
        base_thickness = 2
        vertices = 100
        front_distance = 10
        slit_width = self.cap_size[0] + 2
        top_angle = 2 / 180 * pi
        ceiling = 2 * radius * .8
        slant_angle = 5 / 180 * pi
        slant_length = 20
        slant_height = 7.2
        front_bevel = .5
        headfix_internal_x_angle = 10 / 180 * pi

        # This makes the tube
        tube = add_cylinder(radius + thickness, length, vertices, 'tube')
        tube_cut = add_cylinder(radius + thickness, length, vertices, 'tube_cut')
        activate([tube, tube_cut])
        rotate(pi / 2, 'X')
        mode(('OBJECT'))

        # This makes the base
        base = add_cube([2 * radius, length - .1, base_thickness], [0, 0, 0], 'base')
        translate((0, 0, -radius - thickness + base_thickness / 2 - .1))

        # This makes the center cut
        center = add_cylinder(radius, length + thickness, vertices, 'center')
        rotate(pi / 2, 'X')
        mode('OBJECT')

        # This add the slit cutter
        slit = add_cube([slit_width, length + .01, radius], [0, 0, 0], 'slit')
        translate((0, 0, radius / 2))
        mode('OBJECT')

        # This makes the inner slant shape for the headfix
        slant_size = [(radius + thickness) * 2, slant_length, radius]
        slant_y = length / 2 - slant_length / 2 - 1
        slant_z = slant_size[2] / 2 - radius + ceiling - 1
        slant = add_cube(slant_size, (0, 0, 0), 'slant')
        translate([0, slant_y, slant_z])
        translate([0, 0, -slant_height])
        select_verts(slant, INF, INF_POS, INF_NEG)
        translate((0, 0, slant_size[1] * tan(slant_angle)))
        select_verts(slant, INF, INF_NEG, INF_NEG)
        bevel(front_bevel)
        boolean_modifier(slant, tube, 'INTERSECT')
        resize((.99, 1, 1))
        mode(('OBJECT'))

        # This flattens the tube and center
        z_depth = radius + thickness
        flatten = add_cube([(radius + thickness) * 2, length + 1, z_depth], [0, 0, 0], 'flatten')
        translate(
            (
                0, 0,
                z_depth / 2 - radius - 2.9))  # Need to adjust the number everytime, doing the math will take too long
        mode(('OBJECT'))
        translate((0, 0, ceiling))
        boolean_modifier(center, flatten)
        activate([flatten])
        translate((0, 0, ceiling_thickness))
        boolean_modifier(tube, flatten)
        activate([flatten])
        translate((0, 0, -.01))
        boolean_modifier(slant, flatten)

        # This applies the booleans
        boolean_modifier(tube, base, 'UNION')
        boolean_modifier(tube, center)
        if not play:
            boolean_modifier(tube, slant, 'UNION')
        boolean_modifier(tube, slit)
        delete([base, flatten, slant, center])

        # This moves the tube to position
        activate([tube, tube_cut])
        translate((0, -length / 2 + front_distance, radius - ceiling + (length - front_distance) * tan(top_angle)))
        translate((0, 0, self.head_fix_dims[2] + self.headfix_bar_z))

        if not play:
            # This cuts out the headfix piece
            headfix_cut_size = [self.cap_size[0] + 2 * (self.head_fix_dims[0] + self.headfix_clearance),
                                self.head_fix_dims[1] + self.headfix_clearance + .02,
                                self.head_fix_dims[2] + 1.8 * self.headfix_clearance]
            headfix_cut_location = [0, self.holder_size[1] / 2 + self.holder_xyz[1] + self.headfix_clearance / 2,
                                    self.head_fix_dims[2] / 2 + self.headfix_bar_z]
            headfix_cut = add_cube(headfix_cut_size, [0, 0, 0], 'headfix_cut')
            translate(headfix_cut_location)
            select_verts(headfix_cut, INF, INF_NEG, INF)
            factor = 1 + 2 * headfix_cut_size[1] * tan(headfix_internal_x_angle) / headfix_cut_size[0]
            resize((factor, 1, 1))
            extention = 25
            extrude_move((0, -extention, 0))
            factor = 1 + 2 * extention * tan(headfix_internal_x_angle) / (factor * headfix_cut_size[0])
            resize((factor, 1, 1))
            select_verts(headfix_cut, INF, [-100, -extention], INF_NEG)
            translate((0, 0, -extention * tan(slant_angle)))
            select_verts(headfix_cut, INF, INF_POS, INF)
            extrude_move((0, 25, 0))
            boolean_modifier(tube, headfix_cut)
            delete([headfix_cut])

            # This cuts holes for the backer
            backer_clearance = .15
            backer_size = [radius * 3, headfix_cut_size[2], headfix_cut_size[2]]
            backer_cut = add_cube([x + 2 * backer_clearance for x in backer_size], (0, 0, 0), 'backer_cut')
            backer = add_cube(backer_size, (0, 0, 0), 'backer')
            activate((backer, backer_cut))
            translate(headfix_cut_location)
            translate((0, backer_size[1] / 2 + headfix_cut_size[1] / 2, 0))
            select_verts(backer_cut, INF, INF_NEG, INF)
            extrude_move((0, -headfix_cut_size[2] / 2, 0))
            resize((1, 1, .01))
            select_verts(backer_cut, INF, INF_POS, INF)
            extrude_move((0, headfix_cut_size[2] / 2, 0))
            resize((1, 1, .01))

            boolean_modifier(tube, backer_cut)
            delete([backer_cut])

            boolean_modifier(backer, slit)
            delete([slit])
            activate([backer])
            select_verts(backer, INF_POS, INF, INF)
            bpy.ops.mesh.delete(type='VERT')
            mode(('OBJECT'))

            block_size = 6
            end_block = add_cube([block_size, block_size, block_size], [0, 0, 0], 'end_block')
            translate(headfix_cut_location)
            translate((-radius - block_size / 2 + 1, backer_size[1] / 2 + headfix_cut_size[1] / 2, 0))
            boolean_modifier(end_block, tube_cut)
            boolean_modifier(backer, end_block, 'UNION')
            delete([tube_cut, end_block])

            # this cuts out the hex and screw holes
            headfix_translate = (0, self.holder_size[1] / 2 + self.holder_xyz[1],
                                 (self.head_fix_dims[
                                      2] + 2 * self.headfix_thickness) / 2 - self.headfix_thickness + self.headfix_bar_z)
            for side in [1, -1]:
                distance = 2.3
                hex_location = [side * (self.cap_size[0] / 2 + self.head_fix_dims[0] + distance),
                                -self.head_fix_dims[1] / 2 - distance + self.headfix_clearance,
                                self.head_fix_dims[2] / 2 + distance]
                hex_cut = add_cylinder(self.hex_radius, self.hex_depth, 6, 'hex_cut')
                mode('OBJECT')
                screw_cut = add_cylinder(self.headfix_screw_radius, distance * 5, 32, 'screw_cut')
                activate([hex_cut, screw_cut])
                rotate(pi / 6, 'Z')
                bpy.ops.transform.rotate(value=pi / 4, orient_axis='Y',
                                         orient_matrix=(
                                             (side * 1.0, -1.0, 0.0), (1.0, side * 1.0, 0.0), (0.0, 0.0, 1.0)))
                bpy.ops.transform.translate(value=hex_location)
                bpy.ops.transform.translate(value=headfix_translate)

                # This cuts holes for the clicks
                click_hole = add_cube([1.5, 2, thickness + 1], (0, 0, 0), 'click_hole')
                bpy.ops.transform.translate(value=hex_location)
                bpy.ops.transform.translate(value=headfix_translate)
                translate((-side * 4, 0, -thickness / 2))
                select_verts(click_hole, INF, INF_NEG, INF_POS)
                translate((0, -1.5, 0))
                select_verts(click_hole, INF, INF_POS, INF_NEG)
                translate((0, 1.5, 0))
                mode('OBJECT')

                click_radius = .5
                click_clearance = .1
                click_holder_thickness = .4
                length = 80
                click_holder_cut = add_cylinder(radius=click_radius + click_clearance, depth=length,
                                                vertices=32, name='click_holder')
                click_holder = add_cylinder(radius=click_radius + click_clearance + click_holder_thickness,
                                            depth=30,
                                            vertices=32, name='click_holder')
                activate([click_holder, click_holder_cut])
                rotate(pi / 2, 'X')
                bpy.ops.transform.translate(value=hex_location)
                bpy.ops.transform.translate(value=headfix_translate)
                translate((-side * 4, -length / 2, .3))

                boolean_modifier(tube, hex_cut)
                boolean_modifier(tube, screw_cut)
                boolean_modifier(tube, click_hole)
                boolean_modifier(tube, click_holder, modifier='UNION')
                boolean_modifier(tube, click_holder_cut)

                # This deletes the cutters
                delete([hex_cut, screw_cut, click_hole, click_holder, click_holder_cut])

            # This cuts out a faster print
            trim = add_cube([3 * radius, 60, radius], (0, 0, 0), 'trim')
            translate((0, -12, 7))
            boolean_modifier(trim, tube, 'INTERSECT')

        return tube

    def stand(self):
        # This makes the stand
        stand = add_cube(self.stand_size, (0, self.cover_thickness / 2 - self.stand_front / 2, 0), 'stand')

        # This makes the mid section cutout
        hole_size = [self.cover_size[0] + 2 * self.stand_clearance,
                     self.cover_size[1] + 2 * self.stand_clearance,
                     self.stand_cover_depth + self.stand_clearance]
        hole_location = [0, 0, self.stand_size[2] / 2 - hole_size[2] / 2 + .001]
        hole = add_cube(hole_size, (0, 0, 0), 'hole')
        select_verts(hole, INF, INF, INF_NEG)
        ratio_x = (hole_size[0] - self.stand_clearance) / hole_size[0]
        ratio_y = (hole_size[1] - self.stand_clearance) / hole_size[1]
        resize([ratio_x, ratio_y, 1])
        mode('OBJECT')
        translate(hole_location)
        boolean_modifier(stand, hole)

        clear_size = [self.cover_size[0] - 2 * self.stand_ridge,
                      self.cover_size[1] - 2 * self.stand_ridge + 2 * self.stand_front,
                      self.stand_size[2] + 1]
        clear_location = [0, -self.stand_front, 0]
        clear = add_cube(clear_size, clear_location, 'clear')
        select_verts(clear, [-100, 100], [-100, 0], [-100, 100])
        extrude_move((0, -5, 0))
        boolean_modifier(stand, clear)

        # This cuts out securing screw holes for the lid
        wall_depth = 5
        lid_screw_cut = add_cylinder(self.screw_hole_radius, self.stand_base_size[0] + 5, 32, 'lid_screw_cut')
        rotate(pi / 2, 'Y')
        translate([0, 0, self.stand_base_size[2] / 2 + wall_depth / 2])

        # This makes the base of the stand
        base_location = [0, 0, -self.stand_size[2] / 2 - self.stand_base_size[2] / 2 + .001]
        base = add_cube(self.stand_base_size, (0, 0, 0), 'base')
        select_verts(base, INF, INF, INF_POS)
        translate([0, 0, wall_depth])
        mode('OBJECT')
        inner_size = [self.stand_lid_size[0] + .4, self.stand_lid_size[1] + .4, wall_depth + .01]
        inner_cut = add_cube(inner_size, (0, 0, 0), 'inner_cut')
        translate([0, 0, inner_size[2] / 2 + self.stand_base_size[2] / 2])
        boolean_modifier(base, inner_cut)
        boolean_modifier(base, lid_screw_cut)
        delete([inner_cut])
        activate([base, lid_screw_cut])
        translate(base_location)
        boolean_modifier(stand, base, 'UNION')

        # This makes the lid for the stand
        stand_lid = add_cube(self.stand_lid_size, (0, 0, 0), 'stand_lid')
        inner_size = [self.stand_lid_size[0] - 2 * self.stand_lid_thickness,
                      self.stand_lid_size[1] - 2 * self.stand_lid_thickness,
                      self.stand_lid_size[2]]
        inner_cut = add_cube(inner_size, (0, 0, -self.stand_lid_thickness), 'inner_cut')
        boolean_modifier(stand_lid, inner_cut)
        delete([inner_cut])
        activate([stand_lid])
        translate([0, 0, self.stand_lid_size[2] / 2 + base_location[2] + self.base_thickness / 2])
        boolean_modifier(stand_lid, lid_screw_cut)
        delete([lid_screw_cut])

        # This moves the cover to the right
        activate([stand, stand_lid])
        bpy.ops.transform.translate(value=self.cover_xyz)
        bpy.ops.transform.translate(
            value=[0, 0, -self.stand_size[2] / 2 - self.cover_size[2] / 2 + self.stand_cover_depth])

        # This makes the cut outs for the screws that afix the cover
        size = [self.stand_size[0] + 1, self.hex_radius * 2 + 1 + self.stand_clearance * 2,
                self.stand_cover_depth + 1]
        loc = [0, self.hex_location[1], self.cover_xyz[2] - self.cover_size[2] / 2 + size[2] / 2]
        screw_clear = add_cube(size, loc, 'screw_clear')
        boolean_modifier(stand, screw_clear)

        # This makes the cut out for the cleaner piece
        size = [self.cover_size[0] - 2 * self.stand_ridge + 2 * self.inset, self.stand_size[1],
                self.cleaner_thickness + self.cleaner_clearance * 2]
        loc = [0, self.cover_xyz[1] - self.stand_thickness - self.stand_ridge - .01,
               size[2] / 2 - self.added_cleaner_space]
        clean_cut = add_cube(size, (0, 0, 0), 'clean_cut')
        translate(loc)
        select_verts(clean_cut, [-100, 100], [-100, 0], [-100, 100])
        increase = 1
        resize((1, 1, increase))
        translate((0, 0, size[2] * (increase - 1) / 2))
        boolean_modifier(stand, clean_cut)

        # This makes the cap dovetail
        dove2_size = [self.dove2_width - 2 * self.dove2_clearance, self.dove2_depth - self.dove2_clearance,
                      self.holder_size[2] - 2]
        dove2_location = [0, self.holder_size[1] - dove2_size[1] / 2 + .001,
                          -dove2_size[2] / 2 + self.holder_size[2] - self.holder_wall_thickness]
        dove2_location = [x + y for x, y in zip(dove2_location, self.holder_xyz)]
        cap_dovetail = add_cube(dove2_size, dove2_location, 'cap_dovetail')
        select_verts(cap_dovetail, [-dove2_size[0] / 2, dove2_size[0] / 2], [0, dove2_location[1]], [-100, 100])
        ratio = 1 + 2 * dove2_size[1] / sqrt(3) / dove2_size[0]
        bpy.ops.transform.resize(value=(ratio, 1, 1))
        bpy.ops.mesh.bevel(offset=.05, segments=1)
        select_verts(cap_dovetail, [-100, 100], [dove2_location[1], 100], [-100, 100])
        bpy.ops.mesh.extrude_context_move(TRANSFORM_OT_translate={"value": (0, self.stand_clearance, 0)})
        ratio = 1 - 2 * self.stand_clearance / sqrt(3) / dove2_size[0]
        bpy.ops.transform.resize(value=(ratio, 1, 1))
        extrude_move(
            (
                0, self.cap_wall_thickness + self.stand_thickness - self.stand_ridge - self.stand_clearance / 2 + 1,
                0))
        boolean_modifier(stand, cap_dovetail, 'UNION')

        # This cuts out space for the holder to lower in the back
        handle_size = [self.handle_width + self.stand_clearance * 2, self.handle_length * 4,
                       self.handle_thickness + self.stand_clearance * 2 + self.stand_cover_depth]
        handle_location = [0, handle_size[1] / 2,
                           self.cap_size[2] - handle_size[2] / 2 + self.stand_clearance + self.stand_cover_depth]
        handle_cut = add_cube(handle_size, handle_location, 'handle_cut')
        boolean_modifier(stand, handle_cut)

        # This cuts out a spot for the screw to fit
        loc = [0, self.screw_y, self.cover_size[2] / 2 + self.cover_move_z - self.SCREW_LENGTH / 2]
        bpy.ops.mesh.primitive_cylinder_add(radius=self.SCREW_THREAD_RADIUS, depth=self.SCREW_LENGTH,
                                            location=loc, rotation=(0, 0, 0))
        screw_cut = bpy.context.active_object
        boolean_modifier(stand, screw_cut)

        for obj in [hole, clear, base, screw_clear, clean_cut, screw_cut, handle_cut, cap_dovetail]:
            activate([obj])
            bpy.ops.object.delete(use_global=False)

        stand_test_size = [self.stand_size[0] + 1, self.stand_size[1] + 1, self.stand_size[2] + 1]
        stand_test = add_cube(stand_test_size, (0, self.cover_thickness / 2 - self.stand_front / 2, 0),
                              'stand_test')
        translate((self.cover_xyz[0], self.cover_xyz[1], stand_test_size[2] / 2 - self.stand_thickness))
        boolean_modifier(stand_test, stand, 'INTERSECT')

        return stand

    def cleaner(self):
        # This makes the piece that holds the eppendorf tube and mates with the stand
        cleaner_size = [self.cover_size[0] - 2 * self.stand_ridge - 2 * self.stand_clearance + 2 * self.inset,
                        self.stand_size[1] + 5, self.cleaner_thickness]
        cleaner_loc = [0, -cleaner_size[1] / 2 + self.cap_size[1] / 2 - self.stand_clearance + self.cover_xyz[1],
                       cleaner_size[2] / 2 + self.stand_clearance - self.added_cleaner_space]
        cleaner = add_cube(cleaner_size, cleaner_loc, 'cleaner')

        # This makes the cylinder
        radius = self.eppendorf_tube_diameter / 2
        bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=10, location=(0, -1, 0))
        tube_hole = bpy.context.active_object
        #
        # # This cuts away the interlocking pieces
        # cut_size = [self.stand_size[0] + 2 * self.stand_clearance, self.stand_size[1], self.stand_size[2]]
        # cut_location = [0, self.cover_xyz[1] + self.stand_size[1] / 3, 0]
        # cut = add_cube(cut_size, cut_location, 'cut')
        # inner_cut_size = [self.cover_size[0] - 2 * (self.stand_ridge + self.stand_clearance), self.stand_size[1], self.stand_size[2] + 2]
        # inner_cut = add_cube(inner_cut_size, cut_location, 'inner_cut')
        # translate((0, -1, 0))
        # boolean_modifier(cut, inner_cut)
        #
        # This applies boolean modifiers, deletes, and translates
        boolean_modifier(cleaner, tube_hole)

        for obj in [tube_hole]:
            activate([obj])
            bpy.ops.object.delete(use_global=False)

        return cleaner

    def headfix(self):
        headfix_size = [self.bridge_width + 2 * self.bridge_thickness,
                        self.head_fix_dims[1] + 2 * self.headfix_thickness,
                        self.head_fix_dims[2] + 2 * self.headfix_thickness]
        headfix_location = [0, 0, 0]
        headfix = add_cube(headfix_size, headfix_location, 'headfix')

        # This protrudes the brdige section
        select_verts(headfix, [-100, 100], [0, 100], [-100, 100])
        bpy.ops.mesh.extrude_context_move(TRANSFORM_OT_translate={"value": (0, self.bridge_y, 0)})

        # This makes the two side bars
        for sign in [1, -1]:
            select_verts(headfix, [0, sign * 100], [-headfix_size[1] / 2, headfix_size[1] / 2], [-100, 100])
            bpy.ops.mesh.extrude_context_move(
                TRANSFORM_OT_translate={"value": (sign * (self.stereotax_width - headfix_size[0])
                                                  / 2, 0, 0)})
            bpy.ops.mesh.extrude_region()
            bpy.ops.transform.resize(value=(1, self.stereotax_bar_thickness / headfix_size[1],
                                            self.stereotax_bar_thickness / headfix_size[2]))
            bpy.ops.mesh.extrude_context_move(
                TRANSFORM_OT_translate={"value": (sign * self.stereotax_bar_length, 0, 0)})
        bpy.ops.object.mode_set(mode='OBJECT')

        # This makes the pieces to cut out the middle
        cut1_size = [self.bridge_width, headfix_size[1] + 2 * (self.bridge_y - self.bridge_thickness), 20]
        cut1 = add_cube(cut1_size, (0, 0, 0), 'cut1')

        cut2_size = [self.cap_size[0] + 2 * (self.head_fix_dims[0] + self.headfix_clearance),
                     self.head_fix_dims[1] + self.headfix_thickness + self.headfix_clearance + .002,
                     self.head_fix_dims[2] + 2 * self.headfix_clearance]
        cut2_location = [0, -cut2_size[1] / 2, 0]
        cut2 = add_cube(cut2_size, cut2_location, 'cut2')
        bpy.ops.transform.translate(value=(0, self.head_fix_dims[1] / 2 + self.headfix_clearance, 0))
        select_verts(cut2, [-100, 100], [-100, -cut2_size[1]], [100, 0])
        bpy.ops.transform.translate(value=(0, 0, cut2_size[1] * tan(self.headfix_bar_slant * pi / 180)))

        for side in [1, -1]:
            select_verts(cut2, [side * 100, 0], [-100, -cut2_size[1]], [-100, 100])
            bpy.ops.transform.translate(value=(side * cut2_size[1] * tan(self.headfix_bar_slant * pi / 180), 0, 0))

        bpy.ops.object.mode_set(mode='OBJECT')

        cut3_size = [self.stereotax_width + .002, self.bridge_y + headfix_size[1] + .004, 5]
        cut3_location = [0, -cut3_size[1] / 2 + self.bridge_y + headfix_size[1] / 2 + .002,
                         -cut3_size[2] / 2 - headfix_size[2] / 2 + .5]
        cut3 = add_cube(cut3_size, [0, 0, 0], 'cut3')
        bpy.ops.transform.translate(value=cut3_location)
        select_verts(cut3, [-100, 100], [100, 0], [100, 0])
        bpy.ops.transform.translate(value=(0, 0, cut3_size[1] * tan(self.headfix_bar_slant * pi / 180)))

        bottom_thickness = 1
        amount_to_cut = self.headfix_thickness - self.headfix_clearance - bottom_thickness
        bpy.ops.object.mode_set(mode='OBJECT')
        cut4_size = [self.stereotax_width + .002, self.bridge_y + headfix_size[1] + .004, 5]
        cut4_location = [0, -cut4_size[1] / 2 + self.bridge_y + headfix_size[1] / 2 + .002,
                         -cut4_size[2] / 2 - headfix_size[2] / 2 + amount_to_cut]
        cut4 = add_cube(cut4_size, [0, 0, 0], 'cut4')
        bpy.ops.transform.translate(value=cut4_location)

        # This deletes the cutters
        for obj in [cut1, cut2, cut3, cut4]:
            boolean_modifier(headfix, obj)
            activate([obj])
            bpy.ops.object.delete(use_global=False)

        # This adds the bevels
        activate([headfix])
        for sign in [1, -1]:
            select_verts(headfix, [0, sign * cut1_size[0] / 2], [headfix_size[1], 100], [-100, 100])
            bpy.ops.mesh.bevel(offset=self.headfix_inner_bevel)
            select_verts(headfix, [sign * 100, sign * self.stereotax_width / 2],
                         [0, -self.stereotax_bar_thickness / 2],
                         [0, self.stereotax_bar_thickness / 2])
            bpy.ops.mesh.bevel(offset=self.stereotax_bevel)
            select_verts(headfix, [0, sign * cut1_size[0] / 2], [-100, headfix_size[1] / 2],
                         [-100, -cut2_size[2] / 2 - bottom_thickness])
            bpy.ops.mesh.bevel(offset=0.6)

        bpy.ops.object.mode_set(mode='OBJECT')

        # this cuts out the hex and screw holes
        for side in [1, -1]:
            distance = 2.7
            hex_location = [side * (self.cap_size[0] / 2 + self.head_fix_dims[0] + distance),
                            -self.head_fix_dims[1] / 2 - distance + self.headfix_clearance,
                            self.head_fix_dims[2] / 2 + distance]
            bpy.ops.mesh.primitive_cylinder_add(radius=self.hex_radius, depth=self.hex_depth, vertices=6,
                                                location=(0, 0, 0), rotation=(0, 0, 0))
            hex_cut = bpy.context.active_object
            bpy.ops.mesh.primitive_cylinder_add(radius=self.headfix_screw_radius, depth=distance * 4,
                                                location=(0, 0, 0), rotation=(0, 0, 0))
            screw_cut = bpy.context.active_object
            activate([hex_cut, screw_cut])
            bpy.ops.transform.rotate(value=pi / 4, orient_axis='Y',
                                     orient_matrix=(
                                         (side * 1.0, -1.0, 0.0), (1.0, side * 1.0, 0.0), (0.0, 0.0, 1.0)))
            bpy.ops.transform.translate(value=hex_location)

            boolean_modifier(headfix, hex_cut)
            boolean_modifier(headfix, screw_cut)

            # This deletes the cutters
            for obj in [hex_cut, screw_cut]:
                activate([obj])
                bpy.ops.object.delete(use_global=False)

        activate([headfix])
        bpy.ops.transform.translate(value=(0, self.holder_size[1] / 2 + self.holder_xyz[1],
                                           headfix_size[2] / 2 - self.headfix_thickness + self.headfix_bar_z))


class Chamber:
    def __init__(self, overrider):
        self.overrider = overrider
        self.objects = []
        self.width_port = 2.5
        self.angle_port = 45 * pi / 180
        self.width_side = 5
        self.angle_side = 0.01 * pi / 180
        self.thickness = .7
        self.clearance_base = .03
        self.extra_back_clearance = .03
        # self.top_clearance = .1
        self.c_port = .03
        self.clearance_fastener = .023
        self.segments = 2
        self.h_top = 4
        self.h_locking = 3
        self.h_bottom = 4.5
        self.h_base = .5
        self.base_back_thickness = .451  # measured so i can make frame2
        self.width_fastener = .2 + .02
        self.h_fastener = 2 * .2 + .04
        self.handle_length = .15 * self.thickness
        self.fastener_multipliers = [1.3, .9, .5, .2]
        self.eye_separation = 1.2
        self.fastener_x = self.width_port / 4
        self.fastener_z = -self.h_locking / 4
        self.base_back_factor = 1.02
        self.heights = [self.h_base, self.h_bottom, self.h_locking, self.h_top]
        self.x_inner_shifts = [self.width_port / 2, self.width_port * cos(self.angle_port),
                               -self.angle_side * sin(self.angle_side)]
        self.y_inner_shifts = [0, -self.width_port * sin(self.angle_port), -self.width_side * cos(self.angle_side)]
        # self.x_inner_shifts, self.y_inner_shifts = generate_shifts(self.width_port, self.angle_port, self.width_side,
        #                                                            self.angle_side)
        [self.center, self.base_points, self.internal_points, self.external_points, self.factor] = \
            generate_points(self.x_inner_shifts, self.y_inner_shifts, self.thickness, self.clearance_base,
                            self.base_back_factor)
        self.cam_hole_diameter = 3.5
        self.cam_hole_location = [0, -.5 * (self.width_port / sqrt(2) + self.width_side), self.h_top]
        self.cam_attach_depth = .5
        self.cam_cover_diameter = 2.5
        self.cam_lip_diameter = 4

        self.cable_radius = .8
        self.cable_location = [0, -self.cable_radius * 2 / 3, self.h_top]

    def frame2(self):
        frame_size = [self.width_port + 2 * self.width_port * cos(self.angle_port) + 2 * self.thickness,
                      self.width_port * sin(self.angle_port) + self.width_side + 2 * self.thickness +
                      self.base_back_thickness,
                      sum(self.heights)]
        frame_location = [0, -frame_size[1] / 2 + self.thickness, -frame_size[2] / 2 + self.h_top]
        frame = add_cube(frame_size, frame_location, 'frame')

        for side in [INF_POS, INF_NEG]:
            select_verts(frame, side, INF_POS, INF)
            bevel((self.width_port + self.thickness * 2 * tan(pi / 8)) / sqrt(2))

        mode('OBJECT')

    def frame(self):
        x_inner_shifts = self.x_inner_shifts
        y_inner_shifts = self.y_inner_shifts
        bpy.ops.mesh.primitive_plane_add(size=2 * x_inner_shifts[0], enter_editmode=False,
                                         location=(0, 0, self.h_top / 2),
                                         rotation=(pi / 2, 0.0, 0.0))
        bpy.ops.transform.resize(value=(1, 1, self.h_top / 2 / x_inner_shifts[0]))

        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        obj_frame = bpy.context.active_object
        bpy.context.active_object.name = 'frame'

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        obj_frame.data.vertices[1].select = True
        obj_frame.data.vertices[3].select = True
        bpy.ops.object.mode_set(mode='EDIT')

        bpy.ops.mesh.extrude_context_move(
            TRANSFORM_OT_translate={"value": (x_inner_shifts[1], y_inner_shifts[1], 0)})
        bpy.ops.mesh.extrude_context_move(
            TRANSFORM_OT_translate={"value": (x_inner_shifts[2], y_inner_shifts[2], 0)})

        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        obj_frame.data.vertices[0].select = True
        obj_frame.data.vertices[2].select = True
        bpy.ops.object.mode_set(mode='EDIT')

        bpy.ops.mesh.extrude_context_move(
            TRANSFORM_OT_translate={"value": (-x_inner_shifts[1], y_inner_shifts[1], 0)})
        bpy.ops.mesh.extrude_context_move(
            TRANSFORM_OT_translate={"value": (-x_inner_shifts[2], y_inner_shifts[2], 0)})

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'

        f = self.factor / self.segments
        for i in range(self.segments):
            bpy.ops.mesh.extrude_region()
            bpy.ops.transform.resize(self.overrider, value=(1 + f, 1 + f, 1))
            f = f / (1 + f)

        middle = (self.internal_points[-1][1] + self.external_points[-1][1]) / 2
        select_verts(obj_frame, INF, [-100, middle], INF)
        resize((self.base_back_factor, self.base_back_factor, 1), overrider=self.overrider)
        extrude_move([0, -self.extra_back_clearance, 0])
        extrude()
        resize((.7, 1, 1))

        for face in obj_frame.data.polygons:
            face.select = any(i in verts for i in face.vertices) and facing_down(face.normal)

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, -self.h_locking)})

        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        verts = []
        for vert in obj_frame.data.vertices:
            if vert.co.z < -(self.h_locking - .1) and vert.co.y < sum(y_inner_shifts) - .1:
                verts.append(vert.index)

        select_verts(obj_frame, INF, [self.thickness / 2, -100], [0, 0])
        extrude_move((0, 0, -self.h_locking))
        select_verts(obj_frame, INF, [-self.width_port / 3, -100], [-self.h_locking, -self.h_locking])
        extrude_move((0, 0, -self.h_base - self.h_bottom))

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, -self.h_base - self.h_bottom)})

        bpy.ops.object.mode_set(mode='OBJECT')
        return obj_frame

    def base(self):
        coords = self.base_points
        width = 2 * coords[2][0]
        bpy.ops.mesh.primitive_plane_add(size=width,
                                         location=(
                                             0, coords[2][1],
                                             (self.h_top - self.h_base - self.h_bottom - self.h_locking) / 2),
                                         rotation=(pi / 2, 0.0, pi))
        bpy.ops.transform.resize(value=(1, 1, (self.h_bottom + self.h_locking + self.h_top - self.h_base) / width))

        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        obj_base = bpy.context.active_object
        bpy.context.active_object.name = 'plexiglass_base'

        # This makes the back piece
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        obj_base.data.vertices[0].select = True
        obj_base.data.vertices[1].select = True
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, -self.h_base)})

        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        obj_base.data.vertices[2].select = True
        obj_base.data.vertices[3].select = True
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, self.h_base)})

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, coords[3][1] - coords[2][1], 0)})
        bpy.ops.transform.resize(value=(coords[3][0] / coords[2][0], 1, 1))
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')

        # This makes the base section
        verts = [0, 1, 4, 5]
        for vert in verts:
            obj_base.data.vertices[vert].select = True
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, coords[1][1] - coords[2][1], 0)})
        bpy.ops.transform.resize(value=(coords[1][0] / coords[2][0], 1, 1))
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, coords[0][1] - coords[1][1], 0)})
        bpy.ops.transform.resize(value=(coords[0][0] / coords[1][0], 1, 1))
        bpy.context.active_object.name = 'base'
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')

        # This makes the top
        select_verts(obj_base, [-100, 100], [coords[2][1], coords[2][1]], [self.h_top - self.h_base, self.h_top])
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, coords[1][1] - coords[2][1], 0)})
        bpy.ops.transform.resize(value=(coords[1][0] / coords[2][0], 1, 1))
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, coords[0][1] - coords[1][1], 0)})
        bpy.ops.transform.resize(value=(coords[0][0] / coords[1][0], 1, 1))
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        select_verts(obj_base, [-100, 100], [coords[2][1], coords[3][1]], [self.h_top, self.h_top])
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, 5 * self.h_base)})
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.mesh.primitive_cube_add(size=1,
                                        location=(
                                            0, (coords[2][1] + coords[3][1]) / 2, self.h_top + 2.5 * self.h_base),
                                        rotation=(0, pi / 4, 0))

        # This cuts the handle
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        obj_handle = bpy.context.active_object
        activate([obj_base])
        bpy.ops.object.modifier_add(type='BOOLEAN')
        bpy.context.object.modifiers["Boolean"].operation = 'DIFFERENCE'
        bpy.context.object.modifiers["Boolean"].object = obj_handle
        bpy.ops.object.modifier_apply(modifier="Boolean")

        # This makes the whole for cables to run in
        # cable_port = add_cylinder(self.cable_radius, self.h_base * 3, 100, 'cable_port')
        cable_port = add_cube([self.width_port / 2, self.width_side, self.thickness * 2], [0, 0, 0], 'cable_port')
        translate(self.cable_location)
        boolean_modifier(obj_base, cable_port)
        delete([cable_port])

        # This makes the holes in the base
        bpy.ops.mesh.primitive_cube_add(size=1,
                                        location=(0, 0, -(self.h_base / 2 + self.h_bottom + self.h_locking)),
                                        rotation=(0, 0, pi / 4))
        bpy.ops.transform.resize(value=(.8, .8, 2))
        pee_hole = bpy.context.active_object
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        select_verts(pee_hole, [-100, 100], [-100, 100], [-100, 0])
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.merge()
        bpy.ops.object.mode_set(mode='OBJECT')
        boolean_modifier(obj_base, pee_hole)
        d = 1
        for j in range(5):
            for i in range(5):
                activate([pee_hole])
                bpy.ops.transform.translate(value=(-d, -d, 0))
                if pee_hole.location.y > -7:
                    boolean_modifier(obj_base, pee_hole)
            activate([pee_hole])
            bpy.ops.transform.translate(value=(6 * d, 4 * d, 0))
            boolean_modifier(obj_base, pee_hole)

        # This makes the hole for the ir light
        ir_wire_channel_width = .35
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, coords[2][1], self.h_top - self.h_base - .051))
        bpy.ops.transform.resize(value=(ir_wire_channel_width, 1, .1))
        obj_ir_wire = bpy.context.active_object
        boolean_modifier(obj_base, obj_ir_wire)

        # This makes the hole for the camera
        cam_cut = add_cylinder(self.cam_hole_diameter / 2 + self.clearance_base, self.thickness * 2, 100, 'cam_cut')
        translate(self.cam_hole_location)
        boolean_modifier(obj_base, cam_cut)

        delete([cam_cut, obj_handle, pee_hole, obj_ir_wire])

        return obj_base

    def port(self, blank=False):
        inside_point = self.internal_points[0]
        outside_point = self.external_points[0]

        # This sets the port dimensions
        window_width = 1.3  # cm, new 9/22/21
        # window_width = 1.5  # cm original
        lick_window_width = .7  # cm
        z_dims = [1.6, 2.3, 2.7]  # new 9/22/21
        z_extra = [2, 3.2]  # new 9/22/21
        # z_dims = [1.5, 2.3, 2.6]  # Original
        # z_extra = [1.9, 3.2]  # Original
        extended_back = 1

        LED_diameter = .55
        tube_diameter = .25
        port_ir_height = .4
        ir_y_depth = .17
        ir_y_depth_lick = .07
        ir_x_depth = .3

        # This calculates where everything goes
        offset = self.c_port / (2 * sin((pi - self.angle_port) / 2))
        x_coords = [lick_window_width / 2, window_width / 2, inside_point[0] - offset]
        thickness = abs(outside_point[1] - inside_point[1])
        expansion = outside_point[0] / inside_point[0]

        port_x = [-num for num in x_coords[::-1]] + x_coords
        port_y = [0, .5, 1.2, thickness + extended_back]
        port_z = [-self.h_base - self.h_bottom - self.h_locking] + \
                 [-self.h_bottom - self.h_locking + val for val in z_dims] + \
                 [-self.h_locking - self.c_port]

        [x_shifts, z_shifts] = [shifts(l) for l in [port_x, port_z]]
        if self.segments == 2:
            y_shifts = [thickness / 2 + self.c_port, thickness / 2 - self.c_port]
        elif self.segments == 3:
            y_shifts = [thickness / 3 + self.c_port, thickness / 3 - 2 * self.c_port, thickness / 3 + self.c_port]
        else:
            y_shifts = [thickness]

        x_adjustment = port_x[3] * (expansion - 1) / 2
        z_adjustment = (port_z[0] - (port_z[1] - z_shifts[0] / 2)) / 2

        # This builds the port
        obj_port = vertex_object('port', (port_x[0], port_y[0], port_z[0]))
        activate([obj_port])
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.mesh.select_all(action='SELECT')

        for shift in x_shifts:
            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (shift, 0, 0)})
        bpy.ops.mesh.select_all(action='SELECT')
        current_x = max(x_coords)
        for shift in y_shifts:
            f = 1 + shift / thickness * (outside_point[0] - inside_point[0]) / current_x
            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, shift, 0)})
            bpy.ops.transform.resize(value=(f, 1, 1))
            current_x = current_x * f
        bpy.ops.mesh.select_all(action='SELECT')
        for shift in z_shifts:
            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, shift)})

        commands = [
            {
                'select': ([-100, 100], [thickness, thickness], [port_z[0], port_z[4]]),
                'do': 'extrude_move',
                'value': (0, extended_back, 0)
            },
            {
                'select': (
                    [-100, 100], [thickness + extended_back, thickness + extended_back], [port_z[4], port_z[4]]),
                'do': 'translate',
                'value': (0, 0, -self.h_bottom + z_extra[1])
            },
            {
                'select': (
                    [-100, 100], [y_shifts[0], thickness], [port_z[-1], port_z[-1]]) if self.segments == 2 else (
                    [-100, 100], [y_shifts[0], sum(y_shifts[0:2])], [port_z[-1], port_z[-1]]),
                'do': 'extrude_move',
                'value': (0, 0, self.h_locking)
            }
        ]
        [manipulate(obj_port, command) for command in commands]

        if blank:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.active_object.name = 'blank'
            return obj_port

        y_shifts = shifts(port_y)

        commands = [
            {
                'select': ([port_x[2], port_x[3]], [port_y[0], port_y[0]], [port_z[3], port_z[3]]),
                'do': 'merge',
                'type': 'CENTER'
            },
            {
                'select': ([port_x[1], port_x[4]], [port_y[0], port_y[0]], [port_z[1], port_z[3]]),
                'do': 'extrude_move',
                'value': (0, y_shifts[0], 0)
            },
            {
                'select': ([port_x[1], port_x[4]], [port_y[1], port_y[1]], [port_z[2], port_z[3]]),
                'extra_select': [([port_x[2], port_x[3]], [port_y[1], port_y[1]], [port_z[1], port_z[3]])],
                'do': 'extrude_move',
                'value': (0, y_shifts[1], 0)
            },
            {
                'select': ([-.001, .001], [-100, 100], [port_z[3], port_z[3]]),
                'do': 'translate',
                'value': (0, 0, z_extra[1] - z_dims[2])
            },
            {
                'select': ([port_x[2], port_x[3]], [port_y[1], port_y[2]], [port_z[2], port_z[2]]),
                'do': 'translate',
                'value': (0, 0, z_extra[0] - z_dims[1])
            },
            {
                'select': ([port_x[2], port_x[3]], [port_y[1], port_y[2]], [port_z[1], port_z[1]]),
                'do': 'extrude_move',
                'value': (0, 0, -z_shifts[0] / 2)
            },
            {
                'select': (
                    [port_x[2], port_x[3]], [port_y[2], port_y[2]], [port_z[1] - z_shifts[0] / 2, port_z[1]]),
                'do': 'extrude_move',
                'value': (0, y_shifts[2], 0)
            },
            {
                'select': (
                    [port_x[2] * expansion, port_x[3] * expansion], [port_y[3], port_y[3]], [port_z[0], port_z[1]]),
                'do': 'delete',
                'type': 'ONLY_FACE',
                'limit': .01
            },
        ]

        [manipulate(obj_port, command) for command in commands]

        for i in [2, 3]:
            commands = [
                {
                    'select': ([port_x[i], port_x[i] * expansion], [port_y[3], port_y[3]], [port_z[1], port_z[1]]),
                    'limit': .01,
                    'do': 'merge',
                    'extra_do': ['translate'],
                    'value': ([-x_adjustment if i == 2 else x_adjustment][0], 0, 0)
                },
                {
                    'select': (
                        [port_x[i], port_x[i] * expansion], [port_y[3], port_y[3]],
                        [port_z[0], port_z[1] - z_shifts[0] / 2]),
                    'limit': .01,
                    'do': 'merge',
                    'extra_do': ['translate'],
                    'value': ([-x_adjustment if i == 2 else x_adjustment][0], 0, z_adjustment)
                },
                {
                    'select': ([port_x[i], port_x[i] * expansion], [port_y[2], port_y[3]], [port_z[1], port_z[1]]),
                    'limit': .01,
                    'do': 'bevel',
                    'offset': port_x[3],
                    'segments': 1,
                    'extra_do': ['quads_convert_to_tris'],
                },
                {
                    'select': (
                        [port_x[i], port_x[i]], [port_y[2] - port_x[3], port_y[2] - port_x[3]],
                        [port_z[1], port_z[1]]),
                    'limit': .01,
                    'do': 'translate',
                    'value': (0, port_x[3], 0),
                },
                {
                    'select': (
                        [port_x[i], port_x[i]], [port_y[2], port_y[2]],
                        [port_z[1] + port_x[3], port_z[1] + port_x[3]]),
                    'limit': .01,
                    'do': 'translate',
                    'value': (0, 0, -port_x[3]),
                },
                {
                    'select': ([port_x[i] * (expansion - 1), port_x[i] * (expansion - 1)], [port_y[3], port_y[3]],
                               [port_z[1], port_z[1]]),
                    'limit': .01,
                    'do': 'merge',
                },
            ]
            [manipulate(obj_port, command) for command in commands]

        commands = [
            {
                'select': (
                    [port_x[2] * expansion, port_x[3] * expansion], [port_y[2], port_y[3]],
                    [port_z[1], port_z[1] - port_x[3]]),
                'limit': .01,
                'do': 'translate',
                'value': (0, 0, -.1)
            },
        ]
        [manipulate(obj_port, command) for command in commands]

        # This was the divot at the front, but we are getting rid of it
        # select_verts(obj_port, [-lick_window_width / 2, lick_window_width / 2], [0, 0], [port_z[1], port_z[1]])
        # bevel(.3)

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles()
        bpy.ops.object.mode_set(mode='OBJECT')

        tube_height = port_z[1] + .2
        LED_z = tube_height + .7
        LED_length = 5 * thickness

        # This adds the IR cutters
        ir_pos = [(port_x[1] - ir_x_depth, ir_y_depth, port_z[1] + port_ir_height),
                  (port_x[2] - ir_x_depth, port_y[1] + ir_y_depth_lick, tube_height - .07),
                  (-port_x[1] + ir_x_depth, ir_y_depth, port_z[1] + port_ir_height),
                  (-port_x[2] + ir_x_depth, port_y[1] + ir_y_depth_lick, tube_height - .07)]
        ir1 = self.build_ir()
        bpy.ops.transform.translate(value=ir_pos[0])
        ir2 = self.build_ir(beam_diameter=.15)
        bpy.ops.transform.translate(value=ir_pos[1])
        ir3 = self.build_ir(side='left')
        bpy.ops.transform.translate(value=ir_pos[2])
        bpy.ops.transform.rotate(value=pi, orient_axis='Y')
        ir4 = self.build_ir(beam_diameter=.15, side='left')
        bpy.ops.transform.translate(value=ir_pos[3])
        bpy.ops.transform.rotate(value=pi, orient_axis='Y')
        [boolean_modifier(obj_port, cutter) for cutter in [ir1, ir2, ir3, ir4]]

        # This adds extra cutting for IR
        for pos in ir_pos:
            bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False,
                                            location=(pos[0], thickness + extended_back, pos[2]))
            bpy.ops.transform.resize(value=(.5, .2, .8))
            obj_knife = bpy.context.active_object
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

            commands = [
                {
                    'select': ([-100, 100], [0, thickness + extended_back], [-100, 100]),
                    'do': 'resize',
                    'value': (.3, 1, .5),
                },
            ]
            [manipulate(obj_knife, command) for command in commands]
            boolean_modifier(obj_port, obj_knife)
            activate([obj_knife])
            bpy.ops.object.delete(use_global=False)

        # This adds the LED cutters
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=LED_diameter / 2, depth=LED_length,
                                            enter_editmode=False, location=(0, 0, 0))
        bpy.ops.transform.rotate(value=pi / 2, orient_axis='X')
        bpy.ops.transform.translate(value=(self.eye_separation / 2, thickness / 2, LED_z))
        obj_LED = bpy.context.active_object
        boolean_modifier(obj_port, obj_LED)
        activate([obj_LED])
        bpy.ops.transform.translate(value=(-self.eye_separation, 0, 0))
        boolean_modifier(obj_port, obj_LED)

        # This adds the lick tube cutter

        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=tube_diameter / 2, depth=2,
                                            location=(0, port_y[2], 0))
        bpy.ops.transform.rotate(value=pi / 2, orient_axis='X')
        bpy.ops.transform.translate(value=(0, 0, tube_height))
        obj_tube = bpy.context.active_object
        boolean_modifier(obj_port, obj_tube)

        # This adds window cutter
        window_height = -self.h_bottom - self.h_locking + z_extra[0] + .251
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, y_shifts[0] + .5, window_height))
        bpy.ops.transform.resize(value=(.4, 1, .5))
        obj_window = bpy.context.active_object

        commands = [
            {
                'select': ([-100, 100], [-100, 0], [.5, .5]),
                'do': 'merge',
                'limit': .05
            },
            {
                'select': ([-100, 100], [0, 100], [.5, .5]),
                'do': 'merge',
                'limit': .05
            },
        ]
        [manipulate(obj_window, command) for command in commands]
        boolean_modifier(obj_port, obj_window)

        # This cuts out the bottom
        bpy.ops.mesh.primitive_cube_add(size=1,
                                        location=(0, y_shifts[0] + y_shifts[1], -self.h_bottom - self.h_locking))
        bpy.ops.transform.resize(value=(.45, 1.3, 2))
        obj_bottom_cut = bpy.context.active_object

        commands = [
            {
                'select': ([-100, 100], [-100, 100], [-.5, -.5]),
                'do': 'resize',
                'value': (5, 1, 1)
            },
        ]
        [manipulate(obj_bottom_cut, command) for command in commands]
        boolean_modifier(obj_port, obj_bottom_cut)

        for cutter in [ir1, ir2, ir3, ir4, obj_LED, obj_tube, obj_window, obj_bottom_cut]:
            activate([cutter])
            bpy.ops.object.delete(use_global=False)

        activate([obj_port])
        bpy.context.active_object.name = 'port'
        return obj_port

    def build_ir(self, beam_length=.3, y_dim=3, beam_diameter=.2, side='right'):
        x_dim = .23
        z_dim = .45
        rivet_diameter = .15
        beam_hole_from_end = .15
        rivet_length = y_dim
        bevel = 0.03

        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, location=(0, 0, 0))
        obj_detector = bpy.context.active_object
        bpy.ops.transform.resize(value=(x_dim / 2, y_dim, z_dim))
        bpy.ops.transform.translate(value=(x_dim / 4, y_dim / 2, 0))
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        select_verts(obj_detector, [0, 0], [-100, 100], [-100, 100])
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (-x_dim / 2, 0, 0)})
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        if side == 'right':
            select_verts(obj_detector, [0, 0], [-100, 100], [0, 100])
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.transform.translate(value=(0, 0, x_dim / 2))
            bpy.ops.object.mode_set(mode='OBJECT')
        if side == 'left':
            select_verts(obj_detector, [0, 0], [-100, 100], [-100, 0])
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.transform.translate(value=(0, 0, -x_dim / 2))
            bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.mesh.primitive_cylinder_add(radius=beam_diameter / 2, depth=beam_length, enter_editmode=False,
                                            location=(0, 0, 0))
        obj_post = bpy.context.active_object
        bpy.ops.transform.rotate(value=pi / 2, orient_axis='Y')
        bpy.ops.transform.translate(value=((x_dim + beam_length) / 2 - .01, beam_hole_from_end, 0))

        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=rivet_diameter / 2, depth=rivet_length,
                                            enter_editmode=False, location=(0, 0, 0))
        obj_rivet = bpy.context.active_object
        bpy.ops.transform.rotate(value=pi / 2, orient_axis='X')
        bpy.ops.transform.translate(value=(-.01 + x_dim / 2, beam_hole_from_end + rivet_length / 2, 0))

        boolean_modifier(obj_detector, obj_post, modifier='UNION')
        activate([obj_post])
        bpy.ops.object.delete(use_global=False)

        activate([obj_detector])
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        select_verts(obj_detector, [x_dim / 2, x_dim / 2],
                     [beam_hole_from_end + beam_diameter, beam_hole_from_end - beam_diameter],
                     [beam_diameter, -beam_diameter])
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.bevel(offset=bevel)

        boolean_modifier(obj_detector, obj_rivet, modifier='UNION')
        activate([obj_rivet])
        bpy.ops.object.delete(use_global=False)

        activate([obj_detector])
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles(threshold=0.003)

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        return obj_detector

    def fastener(self):
        widths = [self.width_fastener] + [val * self.width_fastener for val in self.fastener_multipliers]
        lengths = [self.handle_length] + [val * self.thickness for val in [1, 1.05, 1.1, 1.3, 1.6]]  # Original
        # lengths = [self.handle_length] + [self.thickness + val for val in [-.15, -.065, -.03, .11, .32]]  # Shapeways edit
        y_shifts = shifts(lengths)

        obj_fastener = vertex_object('fastener', (0, 0, 0))
        activate([obj_fastener])
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.mesh.select_all(action='SELECT')

        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (widths[0] - widths[4], 0, 0)})
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (2 * widths[4], 0, 0)})
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (widths[0] - widths[4], 0, 0)})

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, lengths[0], 0)})

        # Extrude each side
        for x_select in [[-100, widths[0]], [widths[0], 100]]:
            direction = x_select[0] / abs(x_select[0])
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')
            select_verts(obj_fastener, x_select, [lengths[0], lengths[0]], [-100, 100])
            bpy.ops.object.mode_set(mode='EDIT')

            [bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, shift, 0)}) for shift in
             y_shifts]
            for y_val in lengths[1:-1]:
                adjustment = (widths[3] - widths[4]) * (y_val - lengths[0]) / (lengths[-2] - lengths[0])
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='OBJECT')
                select_verts(obj_fastener,
                             [widths[0] + direction * widths[4], widths[0] + direction * widths[4]],
                             [y_val, y_val], [-100, 100])
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.transform.translate(value=(direction * adjustment, 0, 0))

            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')
            select_verts(obj_fastener, [widths[0] + direction * widths[4], widths[0] + direction * widths[4]],
                         [lengths[-1], lengths[-1]], [-100, 100])
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.transform.translate(value=(direction * (widths[3] - widths[4]), 0, 0))

            for i in range(len(lengths)):
                if direction == abs(direction):
                    x_val = 2 * widths[0]
                else:
                    x_val = 0
                adjustment = widths[floor(i / 2)] - widths[0]
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='OBJECT')
                select_verts(obj_fastener, [x_val, x_val], [lengths[i], lengths[i]], [-100, 100])
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.transform.translate(value=(direction * adjustment, 0, 0))

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, self.h_fastener)})

        handle_expansion = .5

        commands = [
            {
                'select': ([-100, 0], [-100, lengths[0]], [-100, 100]),
                'do': 'extrude_move',
                'value': (-widths[0] * handle_expansion, 0, 0)
            },
            {
                'select': ([2 * widths[0], 100], [-100, lengths[0]], [-100, 100]),
                'do': 'extrude_move',
                'value': (widths[0] * handle_expansion, 0, 0)
            },
            {
                'select': ([2 * widths[0], 2 * widths[0]], [lengths[0], lengths[0]], [-100, 100]),
                'do': 'bevel',
                'offset': handle_expansion / 2 * widths[0],
                'profile': .65,
                'segments': 5
            },
            {
                'select': ([0, 0], [lengths[0], lengths[0]], [-100, 100]),
                'do': 'bevel',
                'offset': handle_expansion / 2 * widths[0],
                'profile': .65,
                'segments': 5
            },
        ]
        [manipulate(obj_fastener, command) for command in commands]

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.translate(value=(-widths[0], 0, -self.h_fastener / 2))

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        return obj_fastener

    def place_fasteners(self):
        placements = [(0, 0, self.fastener_z), (self.fastener_x, 0, 3 * self.fastener_z),
                      (-self.fastener_x, 0, 3 * self.fastener_z)]
        fasteners = [self.fastener() for _ in range(len(placements))]
        self.objects.append(fasteners[0])
        for fastener, placement in zip(fasteners, placements):
            activate([fastener])
            bpy.ops.transform.translate(value=placement)
            bpy.ops.transform.rotate(value=pi / 4, orient_axis='Y')
        for i in [1, -1]:
            activate(fasteners)
            bpy.ops.object.duplicate()
            bpy.ops.transform.rotate(value=i * self.angle_port, orient_axis='Z',
                                     center_override=self.center + [0])

    def cut_fastener_holes(self, obj_list):
        width = self.width_fastener + self.clearance_fastener
        handle_length = self.handle_length + 3 * self.clearance_fastener
        height = self.h_fastener + 2 * self.clearance_fastener
        obj_fastener_cutout = vertex_object('fastener_cutout', (0, 0, 0))
        activate([obj_fastener_cutout])
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (2 * width, 0, 0)})

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, handle_length, 0)})
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 2 * self.thickness, 0)})

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, height)})

        handle_expansion = .5
        # beveled = handle_expansion / 2 * length

        # Extrude handle
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        select_verts(obj_fastener_cutout, [-100, 0], [-100, handle_length], [-100, 100])
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (-width * handle_expansion, 0, 0)})

        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        select_verts(obj_fastener_cutout, [2 * width, 100], [-100, handle_length], [-100, 100])
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (width * handle_expansion, 0, 0)})

        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        select_verts(obj_fastener_cutout, [0, 100], [-100, handle_length], [2 * width, 2 * width])
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, width * handle_expansion)})

        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        select_verts(obj_fastener_cutout, [0, 2 * width], [-100, handle_length], [0, 0])
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, -width * handle_expansion)})

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.translate(value=(-width, -self.clearance_fastener, -height / 2))
        bpy.ops.transform.rotate(value=pi / 4, orient_axis='Y')
        bpy.ops.transform.translate(value=(0, 0, self.fastener_z))

        bpy.ops.mesh.duplicate_move(TRANSFORM_OT_translate={"value": (self.fastener_x, 0, 2 * self.fastener_z)})
        bpy.ops.mesh.duplicate_move(TRANSFORM_OT_translate={"value": (-2 * self.fastener_x, 0, 0)})

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        for i in [0, 1, -2]:
            activate([obj_fastener_cutout])
            bpy.ops.transform.rotate(value=i * self.angle_port, orient_axis='Z', center_override=self.center + [0])
            [boolean_modifier(obj, obj_fastener_cutout) for obj in obj_list]
        activate([obj_fastener_cutout])
        bpy.ops.object.delete(use_global=False)

    def cut_screw_holes(self, obj_list):
        # port_screw_radius = .34 / 2  # First print used this
        port_screw_radius = .38 / 2
        screw_cut = add_cylinder(port_screw_radius, self.thickness * 1.2, 32, 'screw_cut')
        rotate(pi / 2, 'X')
        translate([0, self.thickness * 1.1 / 2, self.fastener_z])
        mode('EDIT')
        bpy.ops.mesh.duplicate_move(TRANSFORM_OT_translate={"value": (0, 0, 2 * self.fastener_z)})
        mode('OBJECT')
        for i in [0, 1, -2]:
            activate([screw_cut])
            bpy.ops.transform.rotate(value=i * self.angle_port, orient_axis='Z', center_override=self.center + [0])
            print(obj_list)
            [boolean_modifier(obj, screw_cut) for obj in obj_list]
        delete([screw_cut])

    def cam_attach(self):
        desired_depth = self.cam_attach_depth
        diameter = self.cam_hole_diameter
        lip_diameter = self.cam_lip_diameter
        clearance = .01
        major_diameter = 2.629 + clearance * 2
        minor_diameter = 2.568 + clearance * 2
        pitch = .0635
        major_edge = pitch / 8
        minor_edge = pitch / 4
        pitch_edge = .01
        segments = 100
        screw_revolutions = 16
        depth = pitch * (screw_revolutions + 1)

        screw_cut_size = major_diameter - minor_diameter
        screw_cut_location = [minor_diameter / 2 + screw_cut_size / 2, 0, 0]
        screw_cut = add_plane(screw_cut_size, [0, 0, 0], 'Y', 'screw_cut')
        select_verts(screw_cut, INF_POS, INF, INF)
        resize((0, 0, major_edge / screw_cut_size))
        select_verts(screw_cut, INF_NEG, INF, INF)
        resize((0, 0, (pitch - minor_edge) / screw_cut_size))
        select_verts(screw_cut, INF, INF, INF)
        translate(screw_cut_location)
        mode('OBJECT')
        bpy.ops.object.modifier_add(type='SCREW')
        bpy.context.object.modifiers["Screw"].steps = segments
        bpy.context.object.modifiers["Screw"].screw_offset = pitch
        bpy.context.object.modifiers["Screw"].iterations = screw_revolutions
        bpy.context.object.modifiers["Screw"].use_normal_flip = True
        bpy.ops.object.modifier_apply(modifier="Screw")

        select_verts(screw_cut, INF_POS, [0, 0], [-pitch / 2, pitch / 2])
        bpy.ops.mesh.edge_face_add()

        # bpy.ops.mesh.merge(type='CENTER')
        select_verts(screw_cut, INF_POS, [0, 0],
                     [-pitch / 2 + pitch * screw_revolutions, pitch / 2 + pitch * screw_revolutions])
        bpy.ops.mesh.edge_face_add()

        # bpy.ops.mesh.merge(type='CENTER')
        mode('OBJECT')
        translate([0, 0, -pitch * screw_revolutions / 2 + .01])
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        cam_attach = add_cylinder(diameter / 2, desired_depth, segments, 'cam_attach')
        lip = add_cylinder(lip_diameter / 2, desired_depth / 2, segments, 'lip')
        translate([0, 0, desired_depth / 4 + .01])
        boolean_modifier(cam_attach, lip, 'UNION')
        minor_radius = minor_diameter / 2 + .001
        minor_cut = add_cylinder(minor_radius, desired_depth + 1, segments, 'minor_cut')
        boolean_modifier(cam_attach, minor_cut)
        delete([minor_cut, lip])

        activate([cam_attach])
        select_verts_radius(cam_attach, INF, INF, [desired_depth / 2, 100], INF_POS, INF_POS, [0, minor_radius])
        bevel(.1)
        select_verts_radius(cam_attach, INF, INF, [-desired_depth / 2, -100], INF_POS, INF_POS, [0, minor_radius])
        bevel(.1)

        boolean_modifier(cam_attach, screw_cut)
        delete([screw_cut])

        activate([cam_attach])
        translate(self.cam_hole_location)

        return cam_attach

    def cam_cover(self):
        cam_cover = add_cylinder(self.cam_lip_diameter / 2, self.cam_attach_depth, 100, 'cam_cover')
        center = add_cylinder(self.cam_cover_diameter / 2, self.thickness, 100, 'center')
        translate([0, 0, -self.thickness / 2])
        boolean_modifier(cam_cover, center, 'UNION')
        delete([center])
        activate([cam_cover])
        translate([0, 0, self.cam_attach_depth + .05])
        translate(self.cam_hole_location)
        return cam_cover

    def cable_cover(self):
        # cable_cover = add_cylinder(self.cable_radius + .25, self.thickness / 2, 100, 'cable_cover')
        # center = add_cylinder(self.cable_radius - .02, self.thickness, 100, 'center')
        cable_cover = add_cube([.7 * self.width_port, self.width_port + .1, self.thickness / 2], [0, 0, 0],
                               'cable_cover')
        center = add_cube([self.width_port / 2 - .05, self.width_port, self.thickness], [0, 0, 0], 'center')
        translate([0, 0, -self.thickness / 2])
        activate([cable_cover, center])
        translate([0, 0, self.thickness / 4 + .05])
        translate(self.cable_location)
        upper_cyl_trim = add_cylinder(.05 + self.cam_lip_diameter / 2, self.thickness * 2, 100, 'upper_cyl_trim')
        translate([0, 0, self.thickness])
        lower_cyl_trim = add_cylinder(.05 + self.cam_hole_diameter / 2, self.thickness * 2, 100, 'lower_cyl_trim')
        activate([upper_cyl_trim, lower_cyl_trim])
        translate(self.cam_hole_location)
        boolean_modifier(center, lower_cyl_trim)
        boolean_modifier(cable_cover, center, 'UNION')
        boolean_modifier(cable_cover, upper_cyl_trim)
        trim = add_cube([self.cable_radius * 4, self.cable_radius * 2, self.thickness * 5], [0, 0, 0], 'trim')
        translate([0, self.cable_radius - self.clearance_base, self.h_top])
        boolean_modifier(cable_cover, trim)
        delete([center, trim, upper_cyl_trim, lower_cyl_trim])
        return cable_cover
