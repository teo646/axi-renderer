import numpy as np
import cv2
from .mask import Mask
from .util import show_image, is_valid_line, is_valid_mask, cv2_draw_line

from axiRenderer.objects.components import Point, Mesh
from math import floor, ceil

class canvas():
    def __init__(self):
        self.lines = []
        self.masks = []


    def register_line_segment(self, point1, point2, pen):

        if(is_valid_line(point1, point2)):
            line_segments_to_mask  = [[point1, point2]] 
            for mask in self._get_mask_in_region(point1, point2):
                masked_lines = []
                for line in line_segments_to_mask:
                    if(is_valid_line(line[0], line[1])):
                        masked_lines += mask.mask_line_segment(line[0], line[1])
                line_segments_to_mask = masked_lines
            
            for line in line_segments_to_mask:
                self.lines.append((line[0], line[1], pen))
        
    
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

    def _get_range_of_points(self):
        x_min = x_max = self.lines[0][0].coordinate[0]
        y_min = y_max = self.lines[0][0].coordinate[1]
        for line in self.lines:
            for i in range(2):
                if(line[i].coordinate[0] > x_max):
                    x_max = line[i].coordinate[0]
                if(line[i].coordinate[0] < x_min):
                    x_min = line[i].coordinate[0]
                if(line[i].coordinate[1] > y_max):
                    y_max = line[i].coordinate[1]
                if(line[i].coordinate[1] < y_min):
                    y_min = line[i].coordinate[1]

        return floor(x_min), ceil(x_max), floor(y_min), ceil(y_max)


    def show(self, magnification):

        x_min, x_max, y_min, y_max = self._get_range_of_points()
        image = np.full(((y_max-y_min)*magnification,(x_max-x_min)*magnification,3), 255, dtype='uint8')

        for line in self.lines:
            image = cv2_draw_line(image, line, magnification, -x_min, -y_min)

        show_image(image[::-1])
