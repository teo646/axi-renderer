from math import cos, sin, pi
import numpy as np
from .components import Point, LineSegment

outline_pen = ((80,80,80), 0.1)
detail_pen = ((80,80,80), 0.1)
roof_pen = ((11, 44, 154), 0.15)


def move_point(point_, Dx, Dy):
    return Point(point_.coordinate[0]+Dx, point_.coordinate[1]+Dy)

def polar_to_descartes(center, radius, angle):
    return Point(center.coordinate[0]+radius*cos(angle), center.coordinate[1]+radius*sin(angle))

def draw_line(mesh, point_, Dx, Dy, pen):
    mesh.points += [point_,
                    move_point(point_, Dx, Dy)]
    arr_length = len(mesh.points)
    mesh.line_segments += [LineSegment(arr_length-2,arr_length-1, pen)]
    return mesh

def connect_points(mesh, point1, point2, pen):
    mesh.points += [point1, point2]
    arr_length = len(mesh.points)
    mesh.line_segments += [LineSegment(arr_length-2,arr_length-1, pen)]
    return mesh

def draw_square(mesh, bottom_right, width, heigth, pen):
    mesh.points += [bottom_right,
                    move_point(bottom_right, 0, heigth),
                    move_point(bottom_right, width, heigth),
                    move_point(bottom_right, width, 0)]
    arr_length = len(mesh.points)
    mesh.line_segments += [LineSegment(arr_length-4,arr_length-3, pen),
                          LineSegment(arr_length-3,arr_length-2, pen),
                          LineSegment(arr_length-2,arr_length-1, pen),
                          LineSegment(arr_length-1,arr_length-4, pen)]
    return mesh

def draw_arc(mesh, center, radius, pen, start_angle=0, end_angle=2*pi):
    unit_line_length = 0.05
    if(start_angle > end_angle):
        end_angle += 2*pi
    unit_angle = unit_line_length/radius
    mesh.points.append(polar_to_descartes(center, radius, start_angle))
    arr_length = len(mesh.points)

    for angle in np.arange(start_angle+unit_angle, end_angle+unit_angle, unit_angle):
        mesh.points.append(polar_to_descartes(center, radius, angle))
        mesh.line_segments.append(LineSegment(arr_length-1, arr_length, pen))
        arr_length += 1

    return mesh


