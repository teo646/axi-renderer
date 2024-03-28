from axiRenderer.objects.components import Point, Path, Mesh
from axiRenderer.objects.draw import move_point, draw_square, draw_line, draw_arc,\
                             outline_pen, detail_pen, roof_pen
from axiRenderer.objects.buildings import draw_simple_window, draw_arc_frame,\
                                          draw_simple_door 
from math import cos, tan
from copy import deepcopy

def draw_floors(mesh, bottom_left, num_room):
    mesh = draw_line(mesh, bottom_left, num_room*9, 0, detail_pen)
    for room in range(num_room):
        room_center = move_point(bottom_left, room*9 + 4.5, 0)
        mesh = draw_simple_window(mesh, room_center, 7, 2, 0.5)
    return mesh

def draw_first_floor(mesh, bottom_left, num_room):
    for room in range(num_room):
        room_center = move_point(bottom_left, room*9 + 4.5, 0)
        if(room == 3):
            mesh = draw_simple_door(mesh, room_center, 5, 12, 1)
        else:
            mesh = draw_simple_window(mesh, move_point(room_center, 0, 6), 7, 2, 0.5)
    return mesh


def get_front_mesh(num_floor, num_room):
    mesh = Mesh()
    mesh = draw_square(mesh, Point(0,0), num_room*9, num_floor*12+6, outline_pen)
    mesh.vertices = deepcopy(mesh.paths[0].points)

    mesh = draw_first_floor(mesh, Point(0,0), num_room)
    
    return mesh

def get_side_mesh(num_floor, depth, roof_angle):
    mesh = Mesh()
    p1 = Point(0,0)
    p2 = Point(depth, 0)
    p3 = Point(depth, num_floor*12+6+tan(roof_angle)*depth)
    p4 = Point(0, num_floor*12+6)

    mesh.paths.append(Path([p1,p2,p3,p4,deepcopy(p1)], outline_pen))
    mesh.vertices = deepcopy(mesh.paths[0].points)

    mesh = draw_simple_window(mesh, Point(depth/2-2, num_floor*8 + 4), 7, 2, 0.5)
    mesh = draw_simple_window(mesh, Point(depth/2+2, num_floor*8 + 4), 7, 2, 0.5)

    return mesh


def get_back_mesh(num_floor, num_room, depth, roof_angle):
    mesh = Mesh()
    p1 = Point(0,0)
    p2 = Point(num_room*9, 0)
    p3 = Point(num_room*9, num_floor*12+6+tan(roof_angle)*depth)
    p4 = Point(0, num_floor*12+6+tan(roof_angle)*depth)

    mesh.paths.append(Path([p1,p2,p3,p4,deepcopy(p1)], outline_pen))
    mesh.vertices = deepcopy(mesh.paths[0].points)
    mesh = draw_simple_window(mesh, Point(num_room*9/2-2, num_floor*8 + 4), 7, 2, 0.5)
    mesh = draw_simple_window(mesh, Point(num_room*9/2+2, num_floor*8 + 4), 7, 2, 0.5)
    return mesh

def get_corner_back_mesh(num_floor, num_room, depth, roof_angle):
    mesh = Mesh()
    p1 = Point(0,0)
    p2 = Point(num_room*9-depth, 0)
    p3 = Point(num_room*9-depth, num_floor*12+6+tan(roof_angle)*depth)
    p4 = Point(0, num_floor*12+6+tan(roof_angle)*depth)

    mesh.paths.append(Path([p1,p2,p3,p4,deepcopy(p1)], outline_pen))
    mesh.vertices = deepcopy(mesh.paths[0].points)

    mesh = draw_simple_window(mesh, Point((num_room*9-depth)/2, num_floor*8 + 4), 7, 2, 0.5)
    return mesh


def get_roof_mesh(num_room, depth, roof_angle, eave_length):
    mesh = Mesh()
    mesh = draw_square(mesh, Point(0,-eave_length), num_room*9, depth/cos(roof_angle)+eave_length, roof_pen)
    mesh.vertices = deepcopy(mesh.paths[0].points)

    for i in range(1,  num_room*9):
        mesh = draw_line(mesh, Point(i, -eave_length), 0, depth/cos(roof_angle)+eave_length, roof_pen)

    return mesh

def get_corner_roof_mesh(num_room, depth, roof_angle, eave_length):
    mesh = Mesh()
    p1 = Point(0,-eave_length)
    p2 = Point(num_room*9+eave_length, -eave_length)
    p3 = Point(num_room*9-depth, depth/cos(roof_angle))
    p4 = Point(0, depth/cos(roof_angle))

    mesh.paths.append(Path([p1,p2,p3,p4,deepcopy(p1)], outline_pen))
    mesh.vertices = deepcopy(mesh.paths[0].points)
    
    for i in range(1,  num_room*9-depth):
        mesh = draw_line(mesh, Point(i, -eave_length), 0, depth/cos(roof_angle)+eave_length, roof_pen)
    for i in range(depth+eave_length):
        ratio = (depth/cos(roof_angle)+eave_length)/(depth+eave_length)
        mesh = draw_line(mesh, Point(num_room*9-depth+i, -eave_length), 0, depth/cos(roof_angle)+eave_length-ratio*i, roof_pen)


    return mesh

