import numpy as np
from axiRenderer.objects.components import Point
def get_length(point1, point2):
    return np.linalg.norm(point1.coordinate-point2.coordinate)


def get_middle_point(point1, point2):
    point_ =  np.mean(np.array([point1.coordinate, point2.coordinate]), axis=0)
    return Point(point_[0], point_[1], point_[2])
