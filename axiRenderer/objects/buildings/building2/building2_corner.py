from axiRenderer.utils.display import display_3d
from axiRenderer.objects.components import Object
from axiRenderer.utils.linear_algebra import get_world_transformaion_matrix
from .sides import get_front_mesh, get_side_mesh, get_corner_back_mesh, get_corner_front_roof_mesh, get_corner_rear_roof_mesh
from math import pi, tan
import pickle
import os
def get_building2_corner(num_floor, num_room_x, num_room_y, depth):
    is_debug = True
    path = os.path.dirname(os.path.abspath(__file__))
    file_name = path + '/models/'+'corner'+str(num_floor)+','+str(num_room_x)+','+str(num_room_y)+','+str(depth)+'.p'
    if(not is_debug and os.path.isfile(file_name)):
        with open(file_name, 'rb') as file:    # open building1.p as read mode if you have one
            building = pickle.load(file)

    else:
        with open(file_name, 'wb') as file:    # write file
            building = Building2_corner(num_floor, num_room_x, num_room_y, depth)
            pickle.dump(building, file)

    return building

class Building2_corner(Object):
    def __init__(self, num_floor, num_room_x, num_room_y, depth):
        roof_angle = 0.17
        eave_length = 5
        meshes = []

        x_front = get_front_mesh(num_floor, num_room_x).transform(get_world_transformaion_matrix(pi/2,0,0,-num_room_x*9/2, -depth/2, 0))
        meshes.append(x_front)
        y_front = get_front_mesh(num_floor, num_room_y).transform(get_world_transformaion_matrix(pi/2,0,pi/2,num_room_x*9/2, -depth/2, 0))
        meshes.append(y_front)
        x_left_side = get_side_mesh(num_floor, depth, roof_angle).transform(get_world_transformaion_matrix(pi/2,0,pi/2,-num_room_x*9/2, -depth/2, 0))
        meshes.append(x_left_side)
        y_right_side = get_side_mesh(num_floor, depth, roof_angle).transform(get_world_transformaion_matrix(pi/2,0,pi,num_room_x*9/2, num_room_y*9-depth/2, 0))
        meshes.append(y_right_side.reverse_direction())

        x_back = get_corner_back_mesh(num_floor, num_room_x,depth).transform(get_world_transformaion_matrix(pi/2,0,0,-num_room_x*9/2, depth/2, 0))
        meshes.append(x_back.reverse_direction())
        y_back = get_corner_back_mesh(num_floor, num_room_y,depth).transform(get_world_transformaion_matrix(pi/2,0,pi/2,num_room_x*9/2-depth, depth/2, 0))
        meshes.append(y_back)
        front_x_roof = get_corner_front_roof_mesh(num_room_x, depth, roof_angle, eave_length).transform(get_world_transformaion_matrix(roof_angle,0,0,-num_room_x*9/2, -depth/2, num_floor*12+6))
        meshes.append(front_x_roof.remove_direction())
        rear_x_roof = get_corner_rear_roof_mesh(num_room_x, depth, roof_angle).transform(get_world_transformaion_matrix(-roof_angle,0,0,-num_room_x*9/2, 0, num_floor*12+6+depth*tan(roof_angle)/2))
        meshes.append(rear_x_roof.reverse_direction())

        front_y_roof = get_corner_front_roof_mesh(num_room_y, depth, roof_angle, eave_length).transform(get_world_transformaion_matrix(pi-roof_angle,0,-pi/2,num_room_x*9/2, num_room_y*9-depth/2, num_floor*12+6))
        meshes.append(front_y_roof.remove_direction())
        rear_y_roof = get_corner_rear_roof_mesh(num_room_y, depth, roof_angle).transform(get_world_transformaion_matrix(-pi+roof_angle,0,-pi/2,num_room_x*9/2-depth/2, num_room_y*9-depth/2, num_floor*12+6+depth*tan(roof_angle)/2))
        meshes.append(rear_y_roof.remove_direction())
        super().__init__(meshes)

def main():
    b = get_building2_corner(5, 7, 5, 20)
    display_3d(b)

if __name__ == "__main__":
    main()
