
from objects import Object, display_object, display_mesh
from axiRenderer import get_world_transformaion_matrix
from .sides import get_front_mesh, get_side_mesh, get_back_mesh, get_front_roof_mesh, get_rear_roof_mesh
from math import pi
import pickle
import os

def get_building2(num_floor, num_room, depth):
    path = os.path.dirname(os.path.abspath(__file__))
    file_name = path + '/models/'+str(num_floor)+','+str(num_room)+','+str(depth)+'.p'
    if(os.path.isfile(file_name)):
        with open(file_name, 'rb') as file:    # open building2.p as read mode if you have one
            building = pickle.load(file)

    else:
        with open(file_name, 'wb') as file:    # write file
            building = Building2(num_floor, num_room, depth)
            pickle.dump(building, file)

    return building

class Building2(Object):
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
        front_roof = get_front_roof_mesh(num_room, depth, roof_angle, eave_length).transform(get_world_transformaion_matrix(roof_angle,0,0,-num_room*9/2, -depth/2, num_floor*12+6))
        meshes.append(front_roof.remove_dir())
        rear_roof = get_rear_roof_mesh(num_room, depth, roof_angle).transform(get_world_transformaion_matrix(roof_angle,0,pi, num_room*9/2, depth/2, num_floor*12+6))
        meshes.append(rear_roof)
        super().__init__(meshes)

def main():
    b = get_building2(5, 7, 20)
    display_object(b)

if __name__ == "__main__":
    main()
