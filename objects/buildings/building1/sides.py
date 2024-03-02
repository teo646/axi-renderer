from objects import display_mesh, Line_segment, Point, Polygon_mesh, move_point, draw_square, draw_line, draw_arc
from math import cos, tan, sin, pi

outline_pen = ((0,0,0), 0.3)
detail_pen = ((80,80,80), 0.2)
roof_pen = ((11, 44, 154), 0.3)

def draw_window(mesh, bottom_center):
    window_heigth = 7
    window_width = 2
    window_offset = 0.5
    bottom_left = move_point(bottom_center, -window_width/2-window_offset, 0)
    mesh = draw_square(mesh, move_point(bottom_center, -window_width/2-window_offset, 0), window_width + 2*window_offset, window_heigth+2*window_offset, detail_pen)
    mesh = draw_square(mesh, move_point(bottom_center, -window_width/2, window_offset), window_width, window_heigth, detail_pen)
    return mesh

#   _
#  / \
#  l l
#  l l
#draw something like this
def draw_door_edge(mesh, bottom_center, width, heigth):
    mesh = draw_line(mesh, move_point(bottom_center, -width/2,0), 0, heigth, detail_pen)
    mesh = draw_line(mesh, move_point(bottom_center, width/2,0), 0, heigth, detail_pen)
    mesh = draw_arc(mesh, move_point(bottom_center, 0, heigth), width/2, detail_pen, start_angle=0, end_angle=pi)
    return mesh

def draw_door(mesh, bottom_center):
    width = 5
    offset = 1
    heigth=12

    #draw door edges
    mesh = draw_door_edge(mesh, bottom_center, width, heigth)
    mesh = draw_door_edge(mesh, bottom_center, width+2*offset, heigth)

    #draw top deco
    mesh = draw_line(mesh, move_point(bottom_center, -width/2, heigth), width, 0, detail_pen)
    for index in range(1, 5):
        mesh = draw_line(mesh, move_point(bottom_center, 0, heigth), cos(pi/5*index)*width/2, sin(pi/5*index)*width/2, detail_pen)

    #draw chocolate on the door
    mesh = draw_square(mesh, move_point(bottom_center, -width/2 + 0.5, 0.5), 1.5, 4.5, detail_pen)
    mesh = draw_square(mesh, move_point(bottom_center, -width/2 + 0.5, 0.5+6.5), 1.5, 4.5, detail_pen)
    mesh = draw_square(mesh, move_point(bottom_center, width/2 - 0.5, 0.5), -1.5, 4.5, detail_pen)
    mesh = draw_square(mesh, move_point(bottom_center, width/2 - 0.5, 0.5+6.5), -1.5, 4.5, detail_pen)
    
    #draw handle
    mesh = draw_arc(mesh, move_point(bottom_center, width/2 - 1, 6), 0.3, detail_pen)
    mesh = draw_arc(mesh, move_point(bottom_center, width/2 - 1, 6), 0.15, detail_pen)

    return mesh



def draw_floors(mesh, bottom_left, num_room):
    mesh = draw_line(mesh, bottom_left, num_room*9, 0, detail_pen)
    for room in range(num_room):
        room_center = move_point(bottom_left, room*9 + 4.5, 0)
        mesh = draw_window(mesh, room_center)
    return mesh



def draw_first_floor(mesh, bottom_left, num_room):
    for room in range(num_room):
        room_center = move_point(bottom_left, room*9 + 4.5, 0)
        if(room == 3):
            mesh = draw_door(mesh, room_center)
        else:
            mesh = draw_window(mesh, move_point(room_center, 0, 6))
    return mesh


def get_front_mesh(num_floor, num_room):
    mesh = Polygon_mesh()
    mesh = draw_square(mesh, Point(0,0), num_room*9, num_floor*12+6, outline_pen)
    mesh.vertices_index = [0,1,2,3]

    mesh = draw_first_floor(mesh, Point(0,0), num_room)
    for floor in range(1, num_floor):
        floor_bottom_left = move_point(Point(0, 6), 0, floor*12)
        mesh = draw_floors(mesh, floor_bottom_left, num_room)

    return mesh

def get_side_mesh(num_floor, depth, roof_angle):
    mesh = Polygon_mesh()
    mesh.points += [Point(0,0),
                    Point(depth, 0),
                    Point(depth, num_floor*12+6+tan(roof_angle)*depth),
                    Point(0, num_floor*12+6)]
    mesh.line_segments += [Line_segment(0,1, outline_pen),
                          Line_segment(1,2, outline_pen),
                          Line_segment(2,3, outline_pen),
                          Line_segment(3,0, outline_pen)]
    mesh.vertices_index = [0,1,2,3]
    return mesh


def get_back_mesh(num_floor, num_room, depth, roof_angle):
    mesh = Polygon_mesh()
    mesh.points += [Point(0,0),
                    Point(num_room*9, 0),
                    Point(num_room*9, num_floor*12+6+tan(roof_angle)*depth),
                    Point(0, num_floor*12+6+tan(roof_angle)*depth)]
    mesh.line_segments += [Line_segment(0,1, outline_pen),
                          Line_segment(1,2, outline_pen),
                          Line_segment(2,3, outline_pen),
                          Line_segment(3,0, outline_pen)]
    mesh.vertices_index = [0,1,2,3]
    return mesh

def get_roof_mesh(num_room, depth, roof_angle, eave_length):
    mesh = Polygon_mesh()
    mesh = draw_square(mesh, Point(0,-eave_length), num_room*9, depth/cos(roof_angle)+eave_length, roof_pen)
    mesh.vertices_index = [0,1,2,3]

    for i in range(1,  num_room*9):
        mesh = draw_line(mesh, Point(i, -eave_length), 0, depth/cos(roof_angle)+eave_length, roof_pen)

    return mesh


