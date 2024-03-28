import numpy as np
import cv2
from .mask import Mask, ReversedMask
from .util import show_image, is_valid_line, is_valid_mask, cv2_draw_line, \
                  identical_points
from axiRenderer.objects.components import Point, Mesh, Path
from math import floor, ceil
from copy import deepcopy

class canvas():
    def __init__(self):
        self.paths = []
        self.masks = []

    def draw_path(self, path):
        current_point = path.points[0]
        current_path = [current_point]
        for p1, p2 in zip(path.points, path.points[1:]):
            for line in self.mask_segment(p1,p2):
                if(identical_points(current_point, line[0])):
                    current_point = line[1]
                    current_path.append(current_point)
                else:
                    if(not len(current_path) == 1):
                        self.paths.append(Path(current_path, path.pen))
                    current_path = [line[0], line[1]]
                    current_point = line[1]
        if(not len(current_path) == 1):
            self.paths.append(Path(current_path, path.pen))


    def mask_segment(self, point1, point2):
        if(is_valid_line(point1, point2)):
            segments_to_mask  = [[point1, point2]] 
            for mask in self._get_mask_in_region(point1, point2):
                masked_lines = []
                for line in segments_to_mask:
                    if(is_valid_line(line[0], line[1])):
                        masked_lines += mask.mask_line_segment(line[0], line[1])
                segments_to_mask = masked_lines
            
            return segments_to_mask
        return []
    
    def _get_mask_in_region(self, point1, point2):
        region = [point1.coordinate[0] if point1.coordinate[0] < point2.coordinate[0] else point2.coordinate[0],
                  point1.coordinate[0] if point1.coordinate[0] > point2.coordinate[0] else point2.coordinate[0],
                  point1.coordinate[1] if point1.coordinate[1] < point2.coordinate[1] else point2.coordinate[1],
                  point1.coordinate[1] if point1.coordinate[1] > point2.coordinate[1] else point2.coordinate[1]]
        mask_in_region = []
        for mask in self.masks:
            if(mask.is_in_the_region(region)):
                mask_in_region.append(mask)

        return mask_in_region


    #you can either put mask or path as a parameter
    def register_mask(self, mask_):
        if(not isinstance(mask_, Mask)):
            mask_ = Mask(mask_)

        if(is_valid_mask(mask_)):
            self.masks.append(mask_)

    def get_range_of_points(self):
        x_min = x_max = self.paths[0].points[0].coordinate[0]
        y_min = y_max = self.paths[0].points[0].coordinate[1]
        for path in self.paths:
            for point in path.points:
                if(point.coordinate[0] > x_max):
                    x_max = point.coordinate[0]
                if(point.coordinate[0] < x_min):
                    x_min = point.coordinate[0]
                if(point.coordinate[1] > y_max):
                    y_max = point.coordinate[1]
                if(point.coordinate[1] < y_min):
                    y_min = point.coordinate[1]

        return floor(x_min), ceil(x_max), floor(y_min), ceil(y_max)
    

    def get_fitting_paths(self,offset):
        x_min, x_max, y_min, y_max = self.get_range_of_points()

        #offset paths
        fitting_paths = []
        for path in self.paths:
            fitting_path = []
            for point in path.points:
                fitting_point = deepcopy(point)
                fitting_point.coordinate[0] -= x_min-offset
                fitting_point.coordinate[1] -= y_min-offset
                fitting_path.append(fitting_point)
            fitting_paths.append(Path(fitting_path, path.pen))

        return fitting_paths



