import bpy
from math import pi, sin, cos, sqrt
from mathutils import Vector
import os
from datetime import datetime


def facing_down(normal):
    return normal.dot(Vector((0.0, 0.0, 1.0))) > .9


def boolean_modifier(obj, cutter, modifier='DIFFERENCE'):
    activate([obj])
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.context.object.modifiers["Boolean"].operation = modifier
    bpy.context.object.modifiers["Boolean"].object = cutter
    bpy.ops.object.modifier_apply(modifier="Boolean")


def vertex_object(name, vertex):  # string, tuple
    mesh = bpy.data.meshes.new(name + '_mesh')
    obj = bpy.data.objects.new(name, mesh)
    obj.show_name = True
    bpy.context.collection.objects.link(obj)
    mesh.from_pydata([vertex], [], [])
    mesh.update()
    return obj


def select_verts(obj, x_range, y_range, z_range, limit=.001):
    if bpy.context.mode != 'EDIT':
        bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    for vert in obj.data.vertices:
        if min(x_range) - limit <= vert.co.x <= max(x_range) + limit \
                and min(y_range) - limit <= vert.co.y <= max(y_range) + limit \
                and min(z_range) - limit <= vert.co.z <= max(z_range) + limit:
            vert.select = True
    bpy.ops.object.mode_set(mode='EDIT')


def select_verts_radius(obj, x_range, y_range, z_range, x_radius, y_radius, z_radius, limit=.001):
    if bpy.context.mode != 'EDIT':
        bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    for vert in obj.data.vertices:
        if min(x_radius) - limit <= sqrt(vert.co.y ** 2 + vert.co.z ** 2) <= max(x_radius) + limit \
                and min(y_radius) - limit <= sqrt(vert.co.x ** 2 + vert.co.z ** 2) <= max(y_radius) + limit \
                and min(z_radius) - limit <= sqrt(vert.co.x ** 2 + vert.co.y ** 2) <= max(z_radius) + limit \
                and min(x_range) - limit <= vert.co.x <= max(x_range) + limit \
                and min(y_range) - limit <= vert.co.y <= max(y_range) + limit \
                and min(z_range) - limit <= vert.co.z <= max(z_range) + limit:
            vert.select = True
    bpy.ops.object.mode_set(mode='EDIT')


def shifts(values):
    return [values[i + 1] - values[i] for i in range(len(values) - 1)]


def center_point(point1, point2):  # [x1,y1],[x2,y2]
    return [(point1[i] + point2[i]) / 2 for i in range(len(point1))]


def slope(point1, point2):  # [x1,x2],[y1,y2]
    return (point1[1] - point2[1]) / (point1[0] - point2[0])


def shift_point(center, m, clearance):
    return [center[0] - clearance * abs(m) * (1 / (1 + m ** 2)) ** (1 / 2),
            center[1] - clearance * (1 / (1 + m ** 2)) ** (1 / 2)]


def intersection(line1, line2):
    [x1, y1, m1] = line1
    [x2, y2, m2] = line2
    x = (m1 * x1 - m2 * x2 + y2 - y1) / (m1 - m2)
    y = m1 * (x - x1) + y1
    return [x, y]


def circle_center(p1, p2, p3):
    [x1, y1] = p1
    [x2, y2] = p2
    [x3, y3] = p3
    k1 = (x1 ** 2 - x3 ** 2 + y1 ** 2 - y3 ** 2) * (2 * x2 - 2 * x3)
    k2 = (x2 ** 2 - x3 ** 2 + y2 ** 2 - y3 ** 2) * (2 * x1 - 2 * x3)
    k3 = (2 * y1 - 2 * y3) * (2 * x2 - 2 * x3) - (2 * y2 - 2 * y3) * (2 * x1 - 2 * x3)
    k = (k1 - k2) / k3
    h1 = x1 ** 2 - x3 ** 2 + y1 ** 2 - y3 ** 2 - (k * (2 * y1 - 2 * y3))
    h2 = (2 * x1 - 2 * x3)
    h = h1 / h2
    return [h, k]


def extrude_coord(pivot, coord, factor):
    [pivot_x, pivot_y] = pivot
    [inner_x, inner_y] = coord
    x1 = (inner_x - pivot_x) ** 2 + (inner_y - pivot_y) ** 2
    x2 = 1 + ((inner_y - pivot_y) / (inner_x - pivot_x)) ** 2
    x = factor * (x1 / x2) ** (1 / 2)
    y = x * (inner_y - pivot_y) / (inner_x - pivot_x)
    return [inner_x + x, inner_y + y]


def add_markers(points):
    for point in points:
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.5, enter_editmode=False, location=(point[0], point[1], 0))


def initialize_blender():
    if bpy.context.mode != 'OBJECT' and bpy.context.active_object:
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    override = bpy.context.copy()
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                override["area"] = area
                override["space_data"] = area.spaces.active
                override["screen"] = screen
                override["window"] = window
                override["region"] = area.regions[-1]
                return override


# def generate_shifts(port_width, port_angle, side_width, side_angle):
#     x_inner_shifts = [port_width / 2, port_width * cos(port_angle), -side_width * sin(side_angle)]
#     y_inner_shifts = [0, -port_width * sin(port_angle), -side_width * cos(side_angle)]
#     return x_inner_shifts, y_inner_shifts


def generate_points(x_inner_shifts, y_inner_shifts, thickness, base_clearance, base_back_factor):
    internal_points = [[sum(x_inner_shifts[0:i]), sum(y_inner_shifts[0:i])] for i in range(1, len(x_inner_shifts) + 1)]
    line_ends = [[[-num for num in internal_points[0]], internal_points[0]]] + [
        [internal_points[i], internal_points[i + 1]] for i in range(len(internal_points) - 1)]
    mid_points = [center_point(point1, point2) for [point1, point2] in line_ends]
    circle_points = [mid_points[0], mid_points[1], [-mid_points[1][0], mid_points[1][1]]]
    center = circle_center(*circle_points)
    factor = thickness / abs(center[1])
    external_points = [extrude_coord(center, point, factor) for point in internal_points]

    line_ends.append([internal_points[-1], external_points[-1]])
    lines = [shift_point(center_point(point1, point2), slope(point1, point2), base_clearance) + [slope(point1, point2)]
             for [point1, point2] in line_ends]
    print(internal_points[-1])
    print(external_points[-1])
    outer = [(e + i) / 2 for i, e in zip(internal_points[-1], external_points[-1])]
    [outer[0], outer[1]] = extrude_coord(center, [outer[0], outer[1]], base_back_factor - 1)
    outer[1] = outer[1] + base_clearance
    lines.append(outer + [0])
    base_points = [intersection(lines[i], lines[i + 1]) for i in range(len(lines) - 1)]
    return [center, base_points, internal_points, external_points, factor]


def place_cursor(overrider, loc):
    bpy.ops.view3d.snap_cursor_to_center(overrider)
    bpy.ops.transform.translate(value=tuple(loc), orient_type='GLOBAL',
                                orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
                                mirror=False,
                                use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1,
                                use_proportional_connected=False, use_proportional_projected=False,
                                cursor_transform=True,
                                release_confirm=False)


def add_plane(size, xyz_location, orthogonal, name):
    bpy.ops.mesh.primitive_plane_add(size=size, location=xyz_location)
    orthos = {
        'X': [pi / 2, 'Y'],
        'Y': [pi / 2, 'X'],
        'Z': [0, 'Z']
    }
    rotate(*orthos[orthogonal])
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    obj = bpy.context.active_object
    bpy.context.active_object.name = name
    return obj


def add_cube(xyz_size, xyz_location, name):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(xyz_location[0], xyz_location[1], xyz_location[2]))
    bpy.ops.transform.resize(value=(xyz_size[0], xyz_size[1], xyz_size[2]))
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    obj = bpy.context.active_object
    bpy.context.active_object.name = name
    return obj


def make_post(radius, height, post_shape, post_locations):
    if post_shape == 1:
        bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=height,
                                            location=(0, 0, 0))
        post = bpy.context.active_object
    else:
        bpy.ops.import_mesh.stl(
            filepath='/Users/elissasutlief/GoogleDrive/Code/Blender/Headcap/Torx_screw_cap-cache_vis_torx.stl',
            axis_forward='X', axis_up='Z')
        torx_radius = 3.91 / 2
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
        post = bpy.context.active_object
        sliver_thickness = .01
        sliver = add_cube([5, 5, sliver_thickness], [0, 0, 0], 'sliver')
        boolean_modifier(post, sliver, modifier='INTERSECT')
        bpy.ops.transform.resize(value=(radius / torx_radius, radius / torx_radius, height / sliver_thickness))
        activate([sliver])
        bpy.ops.object.delete(use_global=False)

    num_posts = 3
    posts = [post]
    for _ in range(num_posts - 1):
        activate([post])
        bpy.ops.object.duplicate(linked=0, mode='TRANSLATION')
        posts.append(bpy.context.active_object)

    for i in range(len(posts)):
        activate([posts[i]])
        bpy.ops.transform.translate(value=post_locations[i])

    activate([posts[1]])
    bpy.ops.transform.rotate(value=pi / 6, orient_axis='Z')

    return posts


def translate(val):
    bpy.ops.transform.translate(value=val)


def extrude_move(val):
    bpy.ops.mesh.extrude_context_move(TRANSFORM_OT_translate={"value": val})


def extrude():
    bpy.ops.mesh.extrude_region()


def resize(val, overrider=None):
    if overrider:
        bpy.ops.transform.resize(overrider, value=val)
    else:
        bpy.ops.transform.resize(value=val)


def mode(val):
    bpy.ops.object.mode_set(mode=val)


def rotate(val, axis):
    bpy.ops.transform.rotate(value=val, orient_axis=axis)


def bevel(val, segments=1):
    bpy.ops.mesh.bevel(offset=val, segments=segments)


def delete(parts):
    for obj in parts:
        activate([obj])
        bpy.ops.object.delete(use_global=False)


def add_cylinder(radius, depth, vertices, name):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=(0, 0, 0),
                                        vertices=vertices)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    obj = bpy.context.active_object
    bpy.context.active_object.name = name
    return obj


def activate(objects):
    if bpy.context.mode != 'OBJECT' and bpy.context.active_object:
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        bpy.context.view_layer.objects.active = obj
        obj.select_set(state=True)


def deactivate(objects):
    if bpy.context.mode != 'OBJECT' and bpy.context.active_object:
        bpy.ops.object.mode_set(mode='OBJECT')
    for obj in objects:
        bpy.context.view_layer.objects.active = obj
        obj.select_set(state=False)


def export_stl(p, scale=1):
    # This makes the directory for the exports
    path = bpy.path.abspath('//stlexports/' + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '/')
    if not os.path.exists(path):
        os.makedirs(path)

    # This writes the parameters file
    f = open(path + "params_used.txt", "w+")
    for param in [a for a in dir(p) if not a.startswith('__')]:
        f.write(param + f': {getattr(p, param)}\r\n')
    f.close()

    # This corrects Normals, Triangles, and Manifold Errors
    for obj in p.objects:
        activate([obj])
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_non_manifold()
        bpy.ops.object.mode_set(mode='OBJECT')
        for vert in obj.data.vertices:
            if vert.select:
                print(str(obj.name))
                print(vert.co.x)
                print(vert.co.y)
        # This exports the object
        file_path = path + obj.name + '.stl'
        bpy.ops.export_mesh.stl(filepath=file_path, use_selection=True, global_scale=scale)


def load_skull(pos=(0, 0, 0)):
    path = '/Users/elissasutlief/github/blender-creations/mouse_anatomy/'
    for name in ['Mouse_Brain.stl', 'Mouse_Skull.stl']:
        bpy.ops.import_mesh.stl(filepath=path + name, axis_forward='-Z', axis_up='-X')
        translate((-13.5, 15, .6))
        translate(pos)


def manipulate(obj, command):
    if bpy.context.mode != 'EDIT':
        bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    if 'limit' in command:
        limit = command['limit']
    else:
        limit = .001
    select_verts(obj, *command['select'], limit=limit)
    if 'extra_select' in command:
        [select_verts(obj, *s, limit=limit) for s in command['extra_select']]
    bpy.ops.object.mode_set(mode='EDIT')
    profile = .5
    to_do = [command['do']]
    if 'extra_do' in command:
        to_do = to_do + command['extra_do']
    for do in to_do:
        if do == 'extrude_move':
            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": command['value']})
        elif do == 'extrude':
            bpy.ops.mesh.extrude_region()
        elif do == 'translate':
            bpy.ops.transform.translate(value=command['value'])
        elif do == 'delete':
            bpy.ops.mesh.delete(type=command['type'])
        elif do == 'merge':
            bpy.ops.mesh.merge(type=command['type']) if 'type' in command else bpy.ops.mesh.merge()
        elif do == 'bevel':
            if 'profile' in command:
                profile = command['profile']
            bpy.ops.mesh.bevel(offset=command['offset'], segments=command['segments'], profile=profile)
        elif do == 'quads_convert_to_tris':
            bpy.ops.mesh.quads_convert_to_tris()
        elif do == 'resize':
            if 'overrider' in command:
                bpy.ops.transform.resize(command['overrider'], value=command['value'])
            else:
                bpy.ops.transform.resize(value=command['value'])
        else:
            print('nothing done to ' + obj.name)
