"""Legacy code for np1 headmount"""

import bpy
from math import tan, sqrt, floor
from helper_functions import *
import numpy as np
from itertools import product


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

        self.head_fix_size = [4, 2, 2]
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

