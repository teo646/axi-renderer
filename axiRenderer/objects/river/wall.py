from axiRenderer.objects.components import Point, Mesh
from axiRenderer.objects.draw import move_point, draw_square, draw_line, draw_arc,\
                             outline_pen, detail_pen, roof_pen
from axiRenderer.objects.buildings import draw_simple_window, draw_arc_frame,\
                                          draw_simple_door 
from axiRenderer.utils.display import display_3d
from math import cos, tan
from copy import deepcopy

def get_wall_inner_mesh(length, heigth):
    mesh = Mesh()
    mesh = draw_square(mesh, Point(0,0), length, heigth, outline_pen)
    mesh.vertices = deepcopy(mesh.paths[0].points)
    for i in range(int(heigth/2)-1):
        mesh = draw_line(mesh, Point(0, i*2+2), length, 0, roof_pen)
        for j in range(int(length/4)-1):
            if(i%2 == 0):
                mesh = draw_line(mesh, Point(j*4+4, i*2+2), 0, 2, roof_pen)
            else:
                mesh = draw_line(mesh, Point(j*4+2, i*2+2), 0, 2, roof_pen)

    return mesh

def get_wall_outer_mesh(length, heigth):
    mesh = Mesh()
    mesh = draw_square(mesh, Point(0,0), length, heigth, outline_pen)
    mesh.vertices = deepcopy(mesh.paths[0].points)

    mesh = draw_line(mesh, Point(0, 8), length, 0, outline_pen)
    mesh = draw_line(mesh, Point(0, heigth - 8), length, 0, outline_pen)
    for i in range(int(length/16)+1):
        mesh = draw_line(mesh, Point(i*16, 0), 0, 8, outline_pen)
        mesh = draw_line(mesh, Point(i*16, heigth - 8), 0, 8, outline_pen)
    for i in range(4, int(heigth/2)-4):
        mesh = draw_line(mesh, Point(0, i*2+2), length, 0, roof_pen)
        for j in range(int(length/4)-1):
            if(i%2 == 0):
                mesh = draw_line(mesh, Point(j*4+4, i*2+2), 0, -2, roof_pen)
            else:
                mesh = draw_line(mesh, Point(j*4+2, i*2+2), 0, -2, roof_pen)


    return mesh


def get_wall_top_mesh(length, width):
    mesh = Mesh()
    mesh = draw_square(mesh, Point(0,0), length, width, outline_pen)
    mesh.vertices = deepcopy(mesh.paths[0].points)
    for i in range(int(length/16)+1):
        mesh = draw_line(mesh, Point(i*16, 0), 0, width, outline_pen)
    return mesh


