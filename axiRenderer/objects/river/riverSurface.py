from maskCanvas import canvas, reverse_mask, point, line_seg
from objects import display_mesh, Line_segment, Point, Polygon_mesh, move_point, draw_square, draw_line, draw_arc
import numpy as np
import random
from math import cos, sin
import copy

def get_normalized_normal(v1, v2):
    normal = np.cross(v1, v2)
    return normal / np.sqrt(np.sum(normal ** 2))

class River_surface(Polygon_mesh):
    def __init__(self, path, world):
        super().__init__()
        self.world = copy.deepcopy(world)
        self.path = path
        #self.canvas = canvas()
        #self.canvas.registerMask(reverse_mask(path))
        #self.registerMask(reverse_mask(path))
        self.surfaceFunction = self.createSurfaceFunction(2)

    def create_world_under_water(self):
        vector1 = self.path[1].coordinate[:3] - self.path[0].coordinate[:3]
        vector2 = self.path[-1].coordinate[:3] - self.path[0].coordinate[:3]
        normalized_normal = get_normalized_normal(vector1, vector2)
        point_lying_on_the_plane = self.path[0].coordinate[:3]
        for mesh in self.world.meshes:
            for point in mesh.points:
                point.coordinate[:3] = point.coordinate[:3] - 2*np.dot(point.coordinate[:3]-point_lying_on_the_plane, normalized_normal)*normalized_normal
        


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


    def transform(self, matrix):
        for mesh in self.world.meshes:
            mesh.transform(matrix)
        self.world.back_face_culling()
        self.world.meshes = arrange_mesh(self.meshes)

        c = canvas()
        c.registerMask(reverse_mask(self.path))
        for mesh in self.world.meshes:
            for line_segment in mesh.line_segments():
                p1 = mesh.points[line_segment.point1_index].coordinate[:2]
                p2 = mesh.points[line_segment.point2_index].coordinate[:2]
                c.registerLineSeg(line_seg([p1,p2], color=line_segment.color, thickness = line_segment.thickness))
            c.registerMask([mesh.points[index].coordinate[:2] for index in mesh.vertices_index])
        # we need to put all of the lines back to lines
        for line_seg in c.getLines():
            self.put_line_on_world(line_seg, world)




