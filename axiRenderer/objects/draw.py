from math import cos, sin, pi
import numpy as np
from .components import Point, Path
import copy
outline_pen = ((80,80,80), 0.1)
detail_pen = ((80,80,80), 0.1)
roof_pen = ((11, 44, 154), 0.15)
water_pen = ((220, 137, 75), 0.1)

def move_point(point_, Dx, Dy):
    return Point(point_.coordinate[0]+Dx, point_.coordinate[1]+Dy)

def polar_to_descartes(center, radius, angle):
    return Point(center.coordinate[0]+radius*cos(angle), center.coordinate[1]+radius*sin(angle))

def draw_line(mesh, point_, Dx, Dy, pen):
    mesh.paths.append(Path([point_, move_point(point_, Dx, Dy)], pen))
    return mesh

def connect_points(mesh, point1, point2, pen):
    mesh.paths.append(Path([point1, point2], pen))
    return mesh

def draw_square(mesh, bottom_right, width, heigth, pen):
    top_right = move_point(bottom_right, 0, heigth)
    top_left = move_point(bottom_right, width, heigth)
    bottom_left = move_point(bottom_right, width, 0)

    mesh.paths.append(Path([bottom_right, top_right, top_left, bottom_left, copy.deepcopy(bottom_right)], pen))
    return mesh

def draw_arc(mesh, center, radius, pen, start_angle=0, end_angle=2*pi):
    unit_line_length = 0.1
    if(start_angle > end_angle):
        end_angle += 2*pi
    unit_angle = unit_line_length/radius

    path = [polar_to_descartes(center, radius, start_angle)]

    for angle in np.arange(start_angle+unit_angle, end_angle+unit_angle, unit_angle):
        path.append(polar_to_descartes(center, radius, angle))

    mesh.paths.append(Path(path, pen))
    return mesh


