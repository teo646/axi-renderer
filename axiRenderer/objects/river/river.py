from axiRenderer.objects.components import Object, Point
from axiRenderer.utils.linear_algebra import get_world_transformaion_matrix
from math import pi
from .river_surface import RiverSurface
from .wall import get_wall_inner_mesh, get_wall_outer_mesh,\
                  get_wall_top_mesh
import copy
class River(Object):
    def __init__(self, width, length, world):
        meshes = []
        path = [Point(0,0),
                Point(length,0),
                Point(length, width),
                Point(0, width)]

        wall_width = 8
        wall_heigth = 20
        river_surface_depth = 7

        wall_inner_mesh = get_wall_inner_mesh(length, wall_heigth+river_surface_depth)
        meshes.append(wall_inner_mesh.transform(get_world_transformaion_matrix(pi/2,0,0,-length/2, -width/2, -river_surface_depth)))
        wall_outer_mesh = get_wall_outer_mesh(length, wall_heigth)
        meshes.append(wall_outer_mesh.transform(get_world_transformaion_matrix(pi/2,0,0,-length/2, -width/2 - wall_width, 0)).reverse_dir())
        wall_top_mesh = get_wall_top_mesh(length, wall_width)
        meshes.append(wall_top_mesh.transform(get_world_transformaion_matrix(0,0,0,-length/2, -width/2 - wall_width, wall_heigth)).reverse_dir())

        wall_inner_mesh = get_wall_inner_mesh(length, wall_heigth+river_surface_depth)
        meshes.append(wall_inner_mesh.transform(get_world_transformaion_matrix(pi/2,0,0,-length/2, width/2, -river_surface_depth)).reverse_dir())
        wall_outer_mesh = get_wall_outer_mesh(length, wall_heigth)
        meshes.append(wall_outer_mesh.transform(get_world_transformaion_matrix(pi/2,0,0,-length/2, width/2 + wall_width, 0)))
        wall_top_mesh = get_wall_top_mesh(length, wall_width)
        meshes.append(wall_top_mesh.transform(get_world_transformaion_matrix(0,0,0, -length/2, width/2, wall_heigth)).reverse_dir())
        river_surface = RiverSurface(path, world)
        meshes.append(river_surface.transform(get_world_transformaion_matrix(0,0,0, -length/2, -width/2, -river_surface_depth)).reverse_dir())

        super().__init__(meshes)

    def world_transform(self, matrix):
        super().world_transform(matrix)
        for mesh in self.meshes[:-1]:
            self.meshes[-1].world.meshes.append(copy.deepcopy(mesh))

        return self
