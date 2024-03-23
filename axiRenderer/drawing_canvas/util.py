import cv2
from axiRenderer.objects.components import Point
import numpy as np


def show_image(image):
# Naming a window
    cv2.namedWindow("Resized_Window", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Resized_Window", 700, 700)
    cv2.imshow("Resized_Window", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_line_intersection(A,B,C,D):
        a1 = B.coordinate[1] - A.coordinate[1]
        b1 = A.coordinate[0] - B.coordinate[0]
        c1 = a1*(A.coordinate[0]) + b1*(A.coordinate[1])

        # Line CD represented as a2x + b2y = c2
        a2 = D.coordinate[1] - C.coordinate[1]
        b2 = C.coordinate[0] - D.coordinate[0]
        c2 = a2*(C.coordinate[0]) + b2*(C.coordinate[1])

        determinant = a1*b2 - a2*b1

        if(determinant == 0):
            print("you tried to get intersection of parallel lines")
            return None
        else:
            x = (b2*c1 - b1*c2)/determinant
            y = (a1*c2 - a2*c1)/determinant
            return Point(x,y,0)

def get_x_intercept_function(point1, point2):
    def tmp(point):
        slope_reciprocal = (point2.coordinate[0] - point1.coordinate[0])/(point2.coordinate[1] - point1.coordinate[1]) 
        return point.coordinate[0] - point.coordinate[1]*slope_reciprocal

    return tmp

def get_y_intercept_function(point1, point2):
    def tmp(point):
        slope = (point2.coordinate[1] - point1.coordinate[1])/(point2.coordinate[0] - point1.coordinate[0])
        return point.coordinate[1] - point.coordinate[0]*slope
    return tmp

class KeyWrapper:
    def __init__(self, iterable, key):
        self.it = iterable
        self.key = key

    def __getitem__(self, i):
        return self.key(self.it[i])

    def __len__(self):
        return len(self.it)

def is_valid_line(point1, point2):
    if(point1.coordinate[0] == point2.coordinate[0]\
       and point1.coordinate[1] == point2.coordinate[1]):
        return False
    return True

def is_valid_mask(mask_):
    if(len(mask_.path)>2):
        return True
    return False

def convert_point(point, magnification, dx, dy):
    return np.array([(point.coordinate[0] + dx)*magnification, (point.coordinate[1] + dy)*magnification], dtype = "uint32")

def cv2_draw_line(image, line, magnification, dx, dy):
    return cv2.line(image, convert_point(line[0], magnification, dx, dy), convert_point(line[1], magnification, dx, dy), line[2][0], int(line[2][1]*magnification))


def identical_points(point1, point2):
    if(point1.coordinate[0] == point2.coordinate[0]\
       and point1.coordinate[1] == point2.coordinate[1]):
        return True
    return False


