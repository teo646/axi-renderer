from axiRenderer.drawing_canvas import canvas, ReversedMask
from axiRenderer.utils.display import display_3d
from axiRenderer.utils.math import get_length, get_middle_point
from axiRenderer.utils.linear_algebra import get_normalized_vector
from axiRenderer.objects.components import Mesh, LineSegment
from axiRenderer.objects.draw import connect_points
from axiRenderer.world.mesh_arranger import arrange_meshes
import numpy as np
import random
from math import cos, sin
import copy


class RiverSurface(Mesh):
    def __init__(self, path, world_):
        pen = ((80,80,80), 0.2)
        super().__init__()
        self.points = path
        self.vertices_index = [i for i in range(len(path))]
        self.world = copy.deepcopy(world_)
#        self.surfaceFunction = self.createSurfaceFunction(2)

    def _create_world_under_water(self):
        vector1 = self.points[self.vertices_index[0]].coordinate[:3]\
                  - self.points[self.vertices_index[1]].coordinate[:3]
        vector2 = self.points[self.vertices_index[0]].coordinate[:3]\
                  - self.points[self.vertices_index[-1]].coordinate[:3]
        normalized_normal = get_normalized_vector(np.cross(vector1, vector2))
        point_lying_on_the_plane = self.points[self.vertices_index[0]].coordinate[:3]
        for mesh in self.world.meshes:
            for point in mesh.points:
                point.coordinate[:3] = point.coordinate[:3] - 2*np.dot(point.coordinate[:3]\
                                      -point_lying_on_the_plane, normalized_normal)*normalized_normal
            mesh.reverse_dir()


    def view_transform(self, matrix):
        super().transform(matrix)        
        for mesh in self.world.meshes:
            mesh.view_transform(matrix)

        self._create_world_under_water()
        self.draw_reflections(matrix)
        return self

    def get_point_on_water_surface(self, point):
        point.coordinate[2] += cos(0.2*point.coordinate[0])*sin(0.2*point.coordinate[1])
        point.coordinate[0] -= cos(0.2*point.coordinate[0])*sin(0.2*point.coordinate[1])
        point.coordinate[1] += cos(0.2*point.coordinate[0])*sin(0.2*point.coordinate[1])
        return point

    def split_points(self, point1, point2):
        points = [point1, point2]
        unit_line_length = 1
        while(unit_line_length < get_length(points[0], points[1])):
            for i in range(len(points)-1, 0, -1):
                    points.insert(i, get_middle_point(points[i],points[i-1]))
        return points


    def draw_reflections(self, matrix):
        inverse_matrix = np.linalg.inv(matrix) 
        #self.line_segments = []
        c = canvas()
        c.register_mask(ReversedMask([self.points[i] for i in self.vertices_index]))
        self.world.back_face_culling()
        self.world.meshes = arrange_meshes(self.world.meshes)
        for mesh in self.world.meshes:
            c = mesh.draw_digital_image(c)
        # we need to put all of the lines back to lines

        for line in c.lines:
            line[0].coordinate[2] = self.get_z_value_on_the_plane(line[0].coordinate)
            line[1].coordinate[2] = self.get_z_value_on_the_plane(line[1].coordinate)

        for line in c.lines:
            line[0].coordinate = np.matmul(inverse_matrix,line[0].coordinate)
            line[1].coordinate = np.matmul(inverse_matrix,line[1].coordinate)
            points = self.split_points(line[0], line[1])
            for p in points:
                p = self.get_point_on_water_surface(p)
                p.coordinate = np.matmul(matrix,p.coordinate)
            for i in range(len(points)-1):
                connect_points(self, points[i], points[i+1], line[2])
            
