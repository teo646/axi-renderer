from axiRenderer.drawing_canvas import canvas, ReversedMask
from axiRenderer.utils.display import display_3d
from axiRenderer.utils.math import get_length, get_middle_point
from axiRenderer.utils.linear_algebra import get_normalized_vector
from axiRenderer.objects.components import Mesh, Path, Point
from axiRenderer.objects.draw import connect_points, water_pen
from axiRenderer.world.mesh_arranger import arrange_meshes
import numpy as np
import random
from math import cos, sin, ceil, floor
from copy import deepcopy


class RiverSurface(Mesh):
    def __init__(self, path, world_):
        super().__init__()
        self.vertices = path
        self.world = deepcopy(world_)
        self.remove_direction()
#        self.surfaceFunction = self.createSurfaceFunction(2)

    def _create_world_under_water(self):
        vector1 = self.vertices[1].coordinate[:3]\
                  - self.vertices[0].coordinate[:3]
        vector2 = self.vertices[-1].coordinate[:3]\
                  - self.vertices[0].coordinate[:3]
        normalized_normal = get_normalized_vector(np.cross(vector1, vector2))
        point_lying_on_the_plane = self.vertices[0].coordinate[:3]
        for object_ in self.world.objects:
            for mesh in object_.meshes:
                for point in mesh.vertices:
                    point.coordinate[:3] = point.coordinate[:3] - 2*np.dot(point.coordinate[:3]\
                                          -point_lying_on_the_plane, normalized_normal)*normalized_normal
                for path in mesh.paths:
                    for point in path.points:
                        point.coordinate[:3] = point.coordinate[:3] - 2*np.dot(point.coordinate[:3]\
                                              -point_lying_on_the_plane, normalized_normal)*normalized_normal
                mesh.reverse_direction()


    def view_transform(self, matrix):
        super().transform(matrix)        
        for object_ in self.world.objects:
            object_.view_transform(matrix)

        self._create_world_under_water()
        self.draw_reflections(matrix)
        return self

    def get_point_on_water_surface(self, point):
        point.coordinate[2] += 1.5*sin(0.4*point.coordinate[0])*sin(0.2*point.coordinate[1])
        point.coordinate[0] -= 0.2*cos(0.4*point.coordinate[0])*sin(0.4*point.coordinate[1])
        point.coordinate[1] += 0.2*cos(0.4*point.coordinate[0])*sin(0.4*point.coordinate[1])
        return point

    def split_points(self, point1, point2):
        points = [point1, point2]
        unit_line_length = 1
        while(unit_line_length < get_length(points[0], points[1])):
            for i in range(len(points)-1, 0, -1):
                points.insert(i, get_middle_point(points[i],points[i-1]))
        return points
    
    def get_paths_on_water(self, paths, matrix):
        inverse_matrix = np.linalg.inv(matrix) 
        paths_on_water = []
        for path in paths:
            for point in path.points:
                point.coordinate[2] = self.get_z_value_on_the_plane(point.coordinate)

        z = np.matmul(inverse_matrix, paths[0].points[0].coordinate)[2]
        for path in paths:
            points_after_noise = []
            for p1, p2 in zip(path.points, path.points[1:]):
                points = self.split_points(p1, p2)
                for p in points:
                    p.coordinate = np.matmul(inverse_matrix,p.coordinate)
                    p.coordinate[2] = z
                    p = self.get_point_on_water_surface(p)
                    p.coordinate = np.matmul(matrix,p.coordinate)
                points_after_noise += points[:-1]

            points_after_noise.append(path.points[-1])
            paths_on_water.append(Path(points_after_noise, self.create_color_under_water(path.pen)))
        return paths_on_water
    
    def create_color_under_water(self, pen):
        pen = list(pen)
        color = list(pen[0])
        color = [x*0.7 for x in color]
        color = tuple(color)
        pen[0] = color
        pen = tuple(pen)
        return pen
        

    def draw_water_flow(self, canvas):
        x_min = x_max = self.vertices[0].coordinate[0]
        y_min = y_max = self.vertices[0].coordinate[1]
        for point in self.vertices:
            if(x_min > point.coordinate[0]):
                x_min = point.coordinate[0]
            if(x_max < point.coordinate[0]):
                x_max = point.coordinate[0]
            if(y_min > point.coordinate[1]):
                y_min = point.coordinate[1]
            if(y_max < point.coordinate[1]):
                y_max = point.coordinate[1]

        for y_coordinate in np.arange(y_min, y_max, 0.5):
            canvas.draw_path(Path([Point(x_min, y_coordinate), Point(x_max, y_coordinate)], water_pen))

        return canvas

    def draw_reflections(self, matrix):
        self.world.back_face_culling()
        meshes = [mesh for object_ in self.world.objects for mesh in object_.meshes]
        meshes = arrange_meshes(meshes)

        c = canvas()
        c.register_mask(ReversedMask(self.vertices))
        c = self.draw_water_flow(c)
        for mesh in meshes:
            c = mesh.draw_digital_image(c)


        self.paths += self.get_paths_on_water(c.paths, matrix)
        vertices =  self.get_paths_on_water([Path(self.vertices, ((0,0,0), 1))], matrix)[0].points
        for point in vertices:
            point.coordinate[2] = self.get_z_value_on_the_plane(point.coordinate)

        self.vertices = vertices


    def get_vertices_after_offset(self):
        center_x = sum([point.coordinate[0] for point in self.vertices])/len(self.vertices)
        center_y = sum([point.coordinate[1] for point in self.vertices])/len(self.vertices)
        return [[center_x, center_y, 0, 1]]

