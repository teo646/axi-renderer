from math import cos, sin, pi
from axiRenderer.objects.draw import move_point, draw_line, draw_arc, draw_square, detail_pen


def draw_simple_window(mesh, bottom_center, window_heigth, window_width, window_offset):
    outer_frame_bottom_left = move_point(bottom_center, -window_width/2-window_offset, 0)
    mesh = draw_square(mesh, outer_frame_bottom_left, window_width + 2*window_offset, window_heigth+2*window_offset, detail_pen)
    inner_frame_bottom_left = move_point(bottom_center, -window_width/2, window_offset)
    mesh = draw_square(mesh, inner_frame_bottom_left, window_width, window_heigth, detail_pen)
    return mesh

#   _
#  / \
#  l l
#  l l
#draw something like this
def draw_arc_frame(mesh, bottom_center, width, heigth):
    bottom_left = move_point(bottom_center, -width/2,0)
    mesh = draw_line(mesh, bottom_left, 0, heigth, detail_pen)

    bottom_right = move_point(bottom_center, width/2,0)
    mesh = draw_line(mesh, bottom_right, 0, heigth, detail_pen)

    mesh = draw_arc(mesh, move_point(bottom_center, 0, heigth), width/2, detail_pen, start_angle=0, end_angle=pi)
    return mesh


def draw_simple_door(mesh, bottom_center, door_width, door_heigth, offset):
    #draw door edges
    mesh = draw_arc_frame(mesh, bottom_center, door_width, door_heigth)
    mesh = draw_arc_frame(mesh, bottom_center, door_width+2*offset, door_heigth)

    inner_frame_top_left = move_point(bottom_center, -door_width/2, door_heigth)
    mesh = draw_line(mesh, inner_frame_top_left, door_width, 0, detail_pen)

    #draw top deco
    top_deco_center = move_point(bottom_center, 0, door_heigth)
    for index in range(1, 5):
        mesh = draw_line(mesh, move_point(bottom_center, 0, door_heigth), cos(pi/5*index)*door_width/2, sin(pi/5*index)*door_width/2, detail_pen)

    #draw chocolates on the door
    deco_offset = offset/2
    chocolate_width = (door_width-2*offset)/2
    chocolate_heigth = (door_heigth-2*offset)/2

    door_bottom_left = move_point(bottom_center, -door_width/2 + deco_offset, deco_offset)
    mesh = draw_square(mesh, door_bottom_left, chocolate_width, chocolate_heigth, detail_pen)

    door_top_left = move_point(bottom_center, -door_width/2 + deco_offset, door_heigth - deco_offset)
    mesh = draw_square(mesh, door_top_left, chocolate_width, -chocolate_heigth, detail_pen)

    door_bottom_right = move_point(bottom_center, door_width/2 - deco_offset, deco_offset)
    mesh = draw_square(mesh, door_bottom_right, -chocolate_width, chocolate_heigth, detail_pen)

    door_top_right = move_point(bottom_center, door_width/2 - deco_offset, door_heigth - deco_offset)
    mesh = draw_square(mesh, door_top_right, -chocolate_width, -chocolate_heigth, detail_pen)

    #draw handle
    handle_center = move_point(bottom_center, door_width/2 - offset, door_heigth/2)
    mesh = draw_arc(mesh, handle_center, 0.3, detail_pen)
    mesh = draw_arc(mesh, handle_center, 0.15, detail_pen)

    return mesh


