#case where you have to rotate image 90 degrees
from axiRenderer.drawing_canvas.canvas import canvas
from axiRenderer.drawing_canvas.mask import ReversedMask
from axiRenderer.objects.components import Point
import numpy as np

def crop_paths(paths, field_x_len, field_y_len, offset):

    drawing_x_len = 0
    drawing_y_len = 0

    for path in paths:
        for point in path.points:
            if(drawing_x_len < point.coordinate[0]):
                drawing_x_len = point.coordinate[0]
            if(drawing_y_len < point.coordinate[1]):
                drawing_y_len = point.coordinate[1]

    #case where image should be rotated 90 degrees
    if((drawing_x_len/drawing_y_len-1)*(field_x_len/field_y_len-1) < 0):
        Rz = np.array([[0, -1, 0, 0],
                       [1, 0, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])
        for path in paths:
            for point in path.points:
                point.coordinate = np.matmul(Rz, point.coordinate)
                point.coordinate[0] += drawing_y_len

    tmp = drawing_x_len
    drawing_x_len = drawing_y_len
    drawing_y_len = tmp
    drawing_x_center = drawing_x_len/2
    drawing_y_center = drawing_y_len/2


    c = canvas()
    c.register_mask(ReversedMask([Point(drawing_x_center-field_x_len/2+offset, drawing_y_center-field_y_len/2+offset),
                                  Point(drawing_x_center+field_x_len/2-offset, drawing_y_center-field_y_len/2+offset),
                                  Point(drawing_x_center+field_x_len/2-offset, drawing_y_center+field_y_len/2-offset),
                                  Point(drawing_x_center-field_x_len/2+offset, drawing_y_center+field_y_len/2-offset)]))


    for path in paths:
        c.draw_path(path)

    return c.get_fitting_paths(offset)


    
    

