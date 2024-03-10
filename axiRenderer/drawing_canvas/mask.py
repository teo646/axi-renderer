import numpy as np
from bisect import bisect_left
from .util import *
from axiRenderer.objects.components import Point, LineSegment

class Mask:

    def is_in_the_region(self, region):
        if(self.region[0]<region[1] and self.region[1]>region[0] and self.region[3] > region[2] and self.region[2] < region[3]):
            return True
        else:
            return False

    def _remove_duplicated_index(self, path):
        duplicated_index = []
        for i in range(len(path)):
            if(path[i-1].coordinate[0] == path[i].coordinate[0]\
               and path[i-1].coordinate[1] == path[i].coordinate[1]):
                duplicated_index.append(i)
        for i in reversed(duplicated_index):
            del path[i]
        
        return path

    def _get_region(self):
        x_min = x_max = self.path[0].coordinate[0]
        y_min = y_max = self.path[0].coordinate[1]
        for point in self.path:
            if(point.coordinate[0] > x_max):
                x_max = point.coordinate[0]
            if(point.coordinate[0] < x_min):
                x_min = point.coordinate[0]
            if(point.coordinate[1] > y_max):
                y_max = point.coordinate[1]
            if(point.coordinate[1] < y_min):
                y_min = point.coordinate[1]

        return [x_min, x_max, y_min, y_max]

    def __init__(self, path):
        self.path = self._remove_duplicated_index(path)
        self.region = self._get_region()


    def _arrange_points(self, use_x_intercept, point1, point2):
        if((not use_x_intercept) and point1.coordinate[0] > point2.coordinate[0]):
            return point2, point1
        elif(use_x_intercept and point1.coordinate[1] > point2.coordinate[1]):
            return point2, point1
        return point1, point2

    def _get_intersections(self, use_x_interception, point1, point2):

        if(use_x_interception):
            get_intercept_function = get_x_intercept_function(point1, point2)
        else:
            get_intercept_function = get_y_intercept_function(point1, point2)

        intersections = []
        intercept = get_intercept_function(point1)
        #get intersections between mask and line(not line segment)
        vertex1_sign = get_intercept_function(self.path[-1]) - intercept
        for index in range(len(self.path)):
            vertex2_sign = get_intercept_function(self.path[index]) - intercept
            #basic intersecting case
            if(vertex1_sign*vertex2_sign < 0):
                intersection = get_line_intersection(point1, point2, self.path[index-1], self.path[index])
                if(intersection):
                    intersections.append(intersection)
            #case where a vertex lies on the line
            elif(vertex1_sign == 0 and (get_intercept_function(self.path[index-2])-intercept)*vertex2_sign < 0):
                intersections.append(self.path[index-1])
            vertex1_sign = vertex2_sign

        return intersections


    #mask line segment
    def mask_line_segment(self, point1, point2):

        if(abs(point2.coordinate[1] - point1.coordinate[1]) > abs(point2.coordinate[0] - point1.coordinate[0])):
            use_x_intercept = True
        else:
            use_x_intercept = False


        point1, point2 = self._arrange_points(use_x_intercept, point1, point2)

        intersections = self._get_intersections(use_x_intercept, point1, point2)

        masked_lines = self._get_masked_lines(use_x_intercept, intersections, point1, point2)
        return masked_lines

    def _get_masked_lines(self, use_x_intercept, intersections, point1, point2):

        if(use_x_intercept):
            intersections = sorted(intersections, key= lambda point: point.coordinate[1])
            point1_index = bisect_left(KeyWrapper(intersections, key=lambda c: c.coordinate[1]), point1.coordinate[1])
            point2_index = bisect_left(KeyWrapper(intersections, key=lambda c: c.coordinate[1]), point2.coordinate[1])
        else:
            intersections = sorted(intersections, key= lambda point:point.coordinate[0])
            point1_index = bisect_left(KeyWrapper(intersections, key=lambda c: c.coordinate[0]), point1.coordinate[0])
            point2_index = bisect_left(KeyWrapper(intersections, key=lambda c: c.coordinate[0]), point2.coordinate[0])

        #if there is no intersections
        if(point1_index == point2_index):
            #no masking 
            if(point1_index%2 == 0):
                return [[point1, point2]]
            else:
                return []

        #if there is any intersection
        masked_lines = []
        if(point1_index%2 == 0):
            masked_lines.append([point1, intersections[point1_index]])
            point1_index += 1
        if(point2_index%2 == 0):
            masked_lines.append([intersections[point2_index-1], point2])
            point2_index -= 1
        for index in range(point1_index, point2_index, 2):
            masked_lines.append([intersections[index], intersections[index+1]])

        return masked_lines

#mask that let you only draw inside of the maclass reverse_mask(mask):
class ReversedMask(Mask):
    def __init__(self):
        super().__init__(path)

    def mask_line_segment(self, point1, point2):
        point1, point2 = self._arrange_points(point1, point2)
        intersections, point1_index, point2_index = self._get_intersections_and_index(point1, point2)

        #if there is no intersections
        if(point1_index == point2_index):
            #no masking
            if(point1_index%2 == 0):
                return []
            else:
                return [[point1, point2]]

        intersections, point1_index, point2_index = self.getIntersectionsAndIndex(line)

        #if there is no intersections
        if(point1_index == point2_index):
            #no masking
            if(point1_index%2 == 0):
                return []
            else:
                return [line]

        #if there is any intersection
        masked_lines = []
        if(point1_index%2 == 1):
            masked_lines.append([line.points[0], intersections[point1_index]])
            point1_index += 1
        if(point2_index%2 == 1):
            masked_lines.append([intersections[point2_index-1], line.points[1]])
            point2_index -= 1
        for index in range(point1_index, point2_index, 2):
            masked_lines.append([intersections[index], intersections[index+1]])

        return masked_lines
