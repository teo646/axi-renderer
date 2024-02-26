from math import cos, sin, pi
import numpy as np
import matplotlib.pyplot as plt
from .components import Point, Line_segment


def convert_rgb(rgb):
    return tuple(i/255 for i in rgb)[::-1] 

def move_point(point_, Dx, Dy):
    return Point(point_.coordinate[0]+Dx, point_.coordinate[1]+Dy)

def polar_to_descartes(center, radius, angle):
    return Point(center.coordinate[0]+radius*cos(angle), center.coordinate[1]+radius*sin(angle))

def draw_line(mesh, point_, Dx, Dy, pen):
    mesh.points += [point_,
                    move_point(point_, Dx, Dy)]
    arr_length = len(mesh.points)
    mesh.line_segments += [Line_segment(arr_length-2,arr_length-1, pen)]
    return mesh


def draw_square(mesh, bottom_right, width, heigth, pen):
    mesh.points += [bottom_right,
                    move_point(bottom_right, 0, heigth),
                    move_point(bottom_right, width, heigth),
                    move_point(bottom_right, width, 0)]
    arr_length = len(mesh.points)
    mesh.line_segments += [Line_segment(arr_length-4,arr_length-3, pen),
                          Line_segment(arr_length-3,arr_length-2, pen),
                          Line_segment(arr_length-2,arr_length-1, pen),
                          Line_segment(arr_length-1,arr_length-4, pen)]
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
        mesh.line_segments.append(Line_segment(arr_length-1, arr_length, pen))
        arr_length += 1

    return mesh


def display_mesh(mesh):
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection='3d', aspect='equal')
    plt.xlabel('x')
    plt.ylabel('y')
    for line_segment in mesh.line_segments:
        p1 = mesh.points[line_segment.point1_index]
        p2 = mesh.points[line_segment.point2_index]
        ax.plot([p1.coordinate[0], p2.coordinate[0]],
                [p1.coordinate[1], p2.coordinate[1]],
                zs=[p1.coordinate[2], p2.coordinate[2]], 
                color=convert_rgb(line_segment.color), 
                linewidth = line_segment.thickness)
    plt.show()

def display_object(object_):
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection='3d', aspect='equal')
    plt.xlabel('x')
    plt.ylabel('y')
    for mesh in object_.meshes:
        for line_segment in mesh.line_segments:
            p1 = mesh.points[line_segment.point1_index]
            p2 = mesh.points[line_segment.point2_index]
            ax.plot([p1.coordinate[0], p2.coordinate[0]],
                    [p1.coordinate[1], p2.coordinate[1]],
                    zs=[p1.coordinate[2], p2.coordinate[2]],
                    color=convert_rgb(line_segment.color),
                    linewidth = line_segment.thickness)
    plt.show()


def create_rotate_and_translate_matrix(x_axis_rotation, y_axis_rotation, z_axis_rotation, 
            x_axis_translation, y_axis_translation, z_axis_translation):

        Rz = np.array([[cos(z_axis_rotation), -sin(z_axis_rotation), 0, 0],
                       [sin(z_axis_rotation), cos(z_axis_rotation), 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])
        Rx = np.array([[1, 0, 0, 0],
                       [0, cos(x_axis_rotation), -sin(x_axis_rotation), 0],
                       [0, sin(x_axis_rotation), cos(x_axis_rotation), 0],
                       [0, 0, 0, 1]])
        Ry = np.array([[cos(y_axis_rotation), 0, sin(y_axis_rotation), 0],
                       [0, 1, 0, 0],
                       [-sin(y_axis_rotation), 0, cos(y_axis_rotation), 0],
                       [0, 0, 0, 1]])

        Txyz = np.array([[1, 0, 0, x_axis_translation],
                         [0, 1, 0, y_axis_translation],
                         [0, 0, 1, z_axis_translation],
                         [0, 0, 0, 1]])

        return np.matmul(Txyz,(np.matmul(Rz, np.matmul(Ry, Rx))))

