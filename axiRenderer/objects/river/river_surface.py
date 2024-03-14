from axiRenderer.drawing_canvas import canvas, ReversedMask
from axiRenderer.utils.display import display_3d
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
        self._create_world_under_water()
        self.line_segments.append(LineSegment(0,1,pen))
        self.line_segments.append(LineSegment(1,2,pen))
        self.line_segments.append(LineSegment(2,3,pen))
        self.line_segments.append(LineSegment(3,0,pen))
#        self.surfaceFunction = self.createSurfaceFunction(2)

    def _create_world_under_water(self):
        vector1 = self.points[self.vertices_index[0]].coordinate[:3] - self.points[self.vertices_index[1]].coordinate[:3]
        vector2 = self.points[self.vertices_index[0]].coordinate[:3] - self.points[self.vertices_index[-1]].coordinate[:3]
        normalized_normal = get_normalized_vector(np.cross(vector1, vector2))
        point_lying_on_the_plane = self.points[self.vertices_index[0]].coordinate[:3]
        for mesh in self.world.meshes:
            for point in mesh.points:
                point.coordinate[:3] = point.coordinate[:3] - 2*np.dot(point.coordinate[:3]-point_lying_on_the_plane, normalized_normal)*normalized_normal
            mesh.reverse_dir()


    def view_transform(self, matrix):
        print("hello")
        for point in self.points:
            point.coordinate = np.matmul(matrix,point.coordinate)
        
        for mesh in self.world.meshes:
            mesh.view_transform(matrix)

        return self

    def draw_digital_image(self, canvas_):
        print("hi")

        c = canvas()
        c.register_mask(ReversedMask([self.points[i] for i in self.vertices_index]))
        self.world.back_face_culling()
        self.world.meshes = arrange_meshes(self.world.meshes)
        for mesh in self.world.meshes:
            c = mesh.draw_digital_image(c)
        # we need to put all of the lines back to lines
        for line in c.lines:
            canvas_.register_line_segment(line[0], line[1], line[2])
        return canvas_

        
'''

    def getHeightPoint(self, point_, length):
        return point(point_.x, point_.y - cos(self.pitch)*length)

    def getPointWithNoise(self, point):
        return self.getHeightPoint(point, self.surfaceFunction(point))


    def createSurfaceFunction(self, max_amplitude):
        def function(point):
            return max_amplitude*cos(0.3*point.x)*sin(0.3*point.y)-self.water_level

        return function

    def getLength(self, point1, point2):
        return np.sqrt((point1.x-point2.x)**2 + (point1.y-point2.y)**2)

    def getMidPoint(self, point1, point2):
        return point((point1.x+point2.x)/2, (point1.y+point2.y)/2)

    def splitPoints(self, points):
        unit_line_length = 1
        while(unit_line_length < self.getLength(points[0], points[1])):
            for i in range(len(points)-1, 0, -1):
                    points.insert(i, self.getMidPoint(points[i],points[i-1]))
        return points

    def registerLineSeg(self, line):
        if(not isinstance(line, line_seg)):
            line = line_seg(line, self.color, self.thickness)
        points = self.splitPoints(line.points)
        noised_points = []
        for p in points:
            noised_points.append(self.getPointWithNoise(p))

        for i in range(len(noised_points)-1):
            super().registerLineSeg([noised_points[i],noised_points[i+1]])

'''

