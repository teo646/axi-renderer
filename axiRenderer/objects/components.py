import numpy as np
from math import cos, sin
class Point:
    def __init__(self,x,y,z=0):
        self.coordinate = np.array([x,y,z,1])


class LineSegment:
    def __init__(self, point1_index, point2_index, pen):
        self.point1_index = point1_index
        self.point2_index = point2_index
        self.pen = pen


#Should be first drawn on the xy plane
#and then transformed.

class Mesh:
    def __init__(self):
        self.points = []
        self.vertices_index = []
        self.line_segments = []
        self.bi_direction = False


    def get_vertices_after_offset(self):
        ratio = 0.01
        center_x = sum([self.points[index].coordinate[0] for index in self.vertices_index])/len(self.vertices_index)
        center_y = sum([self.points[index].coordinate[1] for index in self.vertices_index])/len(self.vertices_index)
        return [self.points[index].coordinate*(1-ratio)+np.array([center_x, center_y,0,0])*ratio for index in self.vertices_index]
    
    def is_front_side(self):
        if(self.bi_direction):
            return True
        if(len(self.vertices_index)<3):
            print("You should put at least 3 vertices index")
            return False
        else:
            v1 = self.points[self.vertices_index[1]].coordinate[:2] - self.points[self.vertices_index[0]].coordinate[:2]
            v2 = self.points[self.vertices_index[2]].coordinate[:2] - self.points[self.vertices_index[0]].coordinate[:2]
            det = np.linalg.det(np.array([v2,v1]))
            if(det>0):
                return True
            else:
                return False

    def get_z_value_on_the_plane(self,coordinate):
        point_on_plane= self.points[self.vertices_index[0]].coordinate[:3]
        v1 = self.points[self.vertices_index[1]].coordinate[:3] - self.points[self.vertices_index[0]].coordinate[:3]
        v2 = self.points[self.vertices_index[2]].coordinate[:3] - self.points[self.vertices_index[0]].coordinate[:3]
        normal_vect = np.cross(v1, v2)
        return (np.dot(normal_vect, point_on_plane)-normal_vect[0]*coordinate[0]-normal_vect[1]*coordinate[1])/normal_vect[2]

    def is_including_point(self, coordinate):
        inside = False
        for index in range(len(self.vertices_index)):
            point1 = self.points[self.vertices_index[index-1]].coordinate
            point2 = self.points[self.vertices_index[index]].coordinate
            intersect = ((point1[1] > coordinate[1]) != (point2[1] > coordinate[1])) and (coordinate[0] < (point2[0] - point1[0]) * (coordinate[1] - point1[1]) / (point2[1] - point1[1]) + point1[0])
            if(intersect):
                inside = not inside

        return inside


    def transform(self,matrix):
        for point in self.points:
            point.coordinate = np.matmul(matrix,point.coordinate)

        return self


    world_transform = transform
    view_transform = transform

    def reverse_dir(self):
        self.vertices_index.reverse()
        return self

    def remove_dir(self):
        self.bi_direction = True
        return self

    def draw_digital_image(self, canvas_):
        for line_segment in self.line_segments:
            p1 = self.points[line_segment.point1_index]
            p2 = self.points[line_segment.point2_index]
            canvas_.register_line_segment(p1, p2, line_segment.pen)
        canvas_.register_mask([self.points[index] for index in self.vertices_index])
        return canvas_

class Object:
    def __init__(self, meshes):
        self.meshes = meshes

    def transform(self, matrix):
        for mesh in self.meshes:
            mesh.transform(matrix)

        return self


    def back_face_culling(self):
        self.meshes = [mesh for mesh in self.meshes if mesh.is_front_side()]





