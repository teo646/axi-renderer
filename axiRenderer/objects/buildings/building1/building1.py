from axiRenderer.utils.display import display_3d
from axiRenderer.objects.components import Object
from axiRenderer.utils.linear_algebra import get_world_transformaion_matrix
from .sides import get_front_mesh, get_side_mesh, get_back_mesh, get_roof_mesh
from math import pi
import pickle
import os
def get_building1(num_floor, num_room, depth):
    is_debug = True
    path = os.path.dirname(os.path.abspath(__file__))
    file_name = path + '/models/'+str(num_floor)+','+str(num_room)+','+str(depth)+'.p'
    if(not is_debug and os.path.isfile(file_name)):
        with open(file_name, 'rb') as file:    # open building1.p as read mode if you have one
            building = pickle.load(file)

    else:
        with open(file_name, 'wb') as file:    # write file
            building = Building1(num_floor, num_room, depth)
            pickle.dump(building, file)

    return building

class Building1(Object):
    def __init__(self, num_floor, num_room, depth):
        roof_angle = 0.17
        eave_length = 5
        meshes = []
        front = get_front_mesh(num_floor, num_room).transform(get_world_transformaion_matrix(pi/2,0,0,-num_room*9/2, -depth/2, 0))
        meshes.append(front)
        right_side = get_side_mesh(num_floor, depth, roof_angle).transform(get_world_transformaion_matrix(pi/2,0,pi/2,num_room*9/2, -depth/2, 0))
        meshes.append(right_side.reverse_dir())
        left_side = get_side_mesh(num_floor, depth, roof_angle).transform(get_world_transformaion_matrix(pi/2,0,pi/2,-num_room*9/2, -depth/2, 0))
        meshes.append(left_side)
        back = get_back_mesh(num_floor, num_room, depth, roof_angle).transform(get_world_transformaion_matrix(pi/2,0,0,-num_room*9/2, depth/2, 0))
        meshes.append(back)
        roof = get_roof_mesh(num_room, depth, roof_angle, eave_length).transform(get_world_transformaion_matrix(roof_angle,0,0,-num_room*9/2, -depth/2, num_floor*12+6))
        meshes.append(roof.remove_dir())
        super().__init__(meshes)

def main():
    b = get_building1(5, 7, 40)
    display_3d(b)

if __name__ == "__main__":
    main()
