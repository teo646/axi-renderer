import numpy as np
from math import cos, sin
class Point:
    def __init__(self,x,y,z=0):
        self.coordinate = np.array([x,y,z,1])
    
    def cv2_version(self):
        return self.coordinate[:2].astype("uint32")

class Path:
    def __init__(self, points, pen):
        self.points = points
        self.reverse = False
        self.pen = pen

    def reverse_direction(self):
        self.reverse = True


#Should be first drawn on the xy plane
#and then transformed.

class Mesh:
    def __init__(self):
        self.paths = []
        self.vertices = []
        self.bi_direction = False


    def get_vertices_after_offset(self):
        ratio = 0.01
        center_x = sum([point.coordinate[0] for point in self.vertices])/len(self.vertices)
        center_y = sum([point.coordinate[1] for point in self.vertices])/len(self.vertices)
        return [point.coordinate*(1-ratio)+np.array([center_x, center_y,0,0])*ratio for point in self.vertices]
    
    def is_front_side(self):
        if(self.bi_direction):
            return True
        if(len(self.vertices)<3):
            print("You should put at least 3 vertices index")
            return False
        else:
            v1 = self.vertices[1].coordinate[:2] - self.vertices[0].coordinate[:2]
            v2 = self.vertices[2].coordinate[:2] - self.vertices[0].coordinate[:2]
            det = np.linalg.det(np.array([v2,v1]))
            if(det>0):
                return True
            else:
                return False

    def get_z_value_on_the_plane(self,coordinate):
        point_on_plane= self.vertices[0].coordinate[:3]
        v1 = self.vertices[1].coordinate[:3] - self.vertices[0].coordinate[:3]
        v2 = self.vertices[2].coordinate[:3] - self.vertices[0].coordinate[:3]
        normal_vect = np.cross(v1, v2)
        return (np.dot(normal_vect, point_on_plane)-normal_vect[0]*coordinate[0]-normal_vect[1]*coordinate[1])/normal_vect[2]

    def is_including_point(self, coordinate):
        inside = False
        for index in range(len(self.vertices)):
            point1 = self.vertices[index-1].coordinate
            point2 = self.vertices[index].coordinate
            intersect = ((point1[1] > coordinate[1]) != (point2[1] > coordinate[1])) and (coordinate[0] < (point2[0] - point1[0]) * (coordinate[1] - point1[1]) / (point2[1] - point1[1]) + point1[0])
            if(intersect):
                inside = not inside

        return inside


    def transform(self,matrix):
        for path in self.paths:
            for point in path.points:
                point.coordinate = np.matmul(matrix,point.coordinate)

        for point in self.vertices:
            point.coordinate = np.matmul(matrix,point.coordinate)
        return self

    world_transform = transform
    view_transform = transform

    def reverse_direction(self):
        self.vertices.reverse()
        return self

    def remove_direction(self):
        self.bi_direction = True
        return self

    def draw_digital_image(self, canvas_):
        for path in self.paths:
            canvas_.draw_path(path)
        canvas_.register_mask(self.vertices)
        return canvas_

class Object:
    def __init__(self, meshes):
        self.meshes = meshes

    def world_transform(self, matrix):
        for mesh in self.meshes:
            mesh.world_transform(matrix)

        return self


    def back_face_culling(self):
        self.meshes = [mesh for mesh in self.meshes if mesh.is_front_side()]
        return self

    def view_transform(self, matrix):
        for mesh in self.meshes:
            mesh.view_transform(matrix)




