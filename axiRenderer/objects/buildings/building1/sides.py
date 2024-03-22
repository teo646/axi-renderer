from axiRenderer.objects.components import Point, LineSegment, Mesh
from axiRenderer.objects.draw import move_point, draw_square, draw_line, draw_arc,\
                             outline_pen, detail_pen, roof_pen
from axiRenderer.objects.buildings import draw_simple_window, draw_arc_frame,\
                                          draw_simple_door 
from math import cos, tan
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
    mesh.vertices_index = [0,1,2,3]

    mesh = draw_first_floor(mesh, Point(0,0), num_room)
    for floor in range(1, num_floor):
        floor_bottom_left = move_point(Point(0, 6), 0, floor*12)
        mesh = draw_floors(mesh, floor_bottom_left, num_room)

    return mesh

def get_side_mesh(num_floor, depth, roof_angle):
    mesh = Mesh()
    mesh.points += [Point(0,0),
                    Point(depth, 0),
                    Point(depth, num_floor*12+6+tan(roof_angle)*depth),
                    Point(0, num_floor*12+6)]
    mesh.line_segments += [LineSegment(0,1, outline_pen),
                          LineSegment(1,2, outline_pen),
                          LineSegment(2,3, outline_pen),
                          LineSegment(3,0, outline_pen)]
    mesh.vertices_index = [0,1,2,3]
    mesh = draw_simple_window(mesh, Point(depth/2-2, num_floor*8 + 4), 7, 2, 0.5)
    mesh = draw_simple_window(mesh, Point(depth/2+2, num_floor*8 + 4), 7, 2, 0.5)

    return mesh


def get_back_mesh(num_floor, num_room, depth, roof_angle):
    mesh = Mesh()
    mesh.points += [Point(0,0),
                    Point(num_room*9, 0),
                    Point(num_room*9, num_floor*12+6+tan(roof_angle)*depth),
                    Point(0, num_floor*12+6+tan(roof_angle)*depth)]
    mesh.line_segments += [LineSegment(0,1, outline_pen),
                          LineSegment(1,2, outline_pen),
                          LineSegment(2,3, outline_pen),
                          LineSegment(3,0, outline_pen)]
    mesh.vertices_index = [0,1,2,3]
    return mesh

def get_corner_back_mesh(num_floor, num_room, depth, roof_angle):
    mesh = Mesh()
    mesh.points += [Point(0,0),
                    Point(num_room*9-depth, 0),
                    Point(num_room*9-depth, num_floor*12+6+tan(roof_angle)*depth),
                    Point(0, num_floor*12+6+tan(roof_angle)*depth)]
    mesh.line_segments += [LineSegment(0,1, outline_pen),
                          LineSegment(1,2, outline_pen),
                          LineSegment(2,3, outline_pen),
                          LineSegment(3,0, outline_pen)]
    mesh.vertices_index = [0,1,2,3]
    return mesh


def get_roof_mesh(num_room, depth, roof_angle, eave_length):
    mesh = Mesh()
    mesh = draw_square(mesh, Point(0,-eave_length), num_room*9, depth/cos(roof_angle)+eave_length, roof_pen)
    mesh.vertices_index = [0,1,2,3]

    for i in range(1,  num_room*9):
        mesh = draw_line(mesh, Point(i, -eave_length), 0, depth/cos(roof_angle)+eave_length, roof_pen)

    return mesh

def get_corner_roof_mesh(num_room, depth, roof_angle, eave_length):
    mesh = Mesh()
    mesh.points += [Point(0,-eave_length),
                    Point(num_room*9+eave_length, -eave_length),
                    Point(num_room*9-depth, depth/cos(roof_angle)),
                    Point(0, depth/cos(roof_angle))]
    mesh.line_segments += [LineSegment(0,1, roof_pen),
                          LineSegment(1,2, roof_pen),
                          LineSegment(2,3, roof_pen),
                          LineSegment(3,0, roof_pen)]
    mesh.vertices_index = [0,1,2,3]


    
    for i in range(1,  num_room*9-depth):
        mesh = draw_line(mesh, Point(i, -eave_length), 0, depth/cos(roof_angle)+eave_length, roof_pen)
        ratio = (depth/cos(roof_angle)+eave_length)/(depth+eave_length)
    for i in range(depth+eave_length):
        mesh = draw_line(mesh, Point(num_room*9-depth+i, -eave_length), 0, depth/cos(roof_angle)+eave_length-ratio*i, roof_pen)


    return mesh

