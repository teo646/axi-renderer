import numpy as np
from math import cos, sin
from axiRenderer import get_normalized_vector
class Point:
    def __init__(self,x,y,z=0):
        self.coordinate = np.array([x,y,z,1])


class Line_segment:
    def __init__(self, point1_index, point2_index, pen):
        self.point1_index = point1_index
        self.point2_index = point2_index
        self.color = pen[0]
        self.thickness = pen[1]


#Should be first drawn on the xy plane
#and then transformed.

class Polygon_mesh:
    def __init__(self):
        self.points = []
        self.vertices_index = []
        self.line_segments = []
        self.bi_direction = False
    
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

    def transform(self,matrix):
        for point in self.points:
            point.coordinate = np.matmul(matrix,point.coordinate)

        return self

    def reverse_dir(self):
        self.vertices_index.reverse()
        return self

    def remove_dir(self):
        self.bi_direction = True
        return self

class Object:
    def __init__(self, meshes):
        self.meshes = meshes

    def transform(self, matrix):
        for mesh in self.meshes:
            mesh.transform(matrix)

        return self


    def back_face_culling(self):
        self.meshes = [mesh for mesh in self.meshes if mesh.is_front_side()]





