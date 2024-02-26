import numpy as np
from math import cos, sin

def get_normalized_vector(vector):
    return vector/np.sqrt(np.sum(vector ** 2))

def convert_rgb(rgb):
    return tuple(i/255 for i in rgb)[::-1]

def get_world_transformaion_matrix(x_axis_rotation, y_axis_rotation, z_axis_rotation,
            x_axis_translation, y_axis_translation, z_axis_translation):

        Rz = np.array([[cos(z_axis_rotation), -sin(z_axis_rotation), 0, 0],
                       [sin(z_axis_rotation), cos(z_axis_rotation), 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])
        Rx = np.array([[1, 0, 0, 0],
                       [0, cos(x_axis_rotation), -sin(x_axis_rotation), 0],
                       [0, sin(x_axis_rotation), cos(x_axis_rotation), 0],
                       [0, 0, 0, 1]])
        Ry = np.array([[cos(y_axis_rotation), 0, sin(y_axis_rotation), 0],
                       [0, 1, 0, 0],
                       [-sin(y_axis_rotation), 0, cos(y_axis_rotation), 0],
                       [0, 0, 0, 1]])

        Txyz = np.array([[1, 0, 0, x_axis_translation],
                         [0, 1, 0, y_axis_translation],
                         [0, 0, 1, z_axis_translation],
                         [0, 0, 0, 1]])

        return np.matmul(Txyz,(np.matmul(Rz, np.matmul(Ry, Rx))))

def get_view_transformation_matrix(EYE, AT):
    EYE = EYE.coordinate[:-1]
    AT = AT.coordinate[:-1]
    UP = [0,0,1]

    n = get_normalized_vector(EYE-AT)
    u = get_normalized_vector(np.cross(UP, n))
    v = np.cross(n,u)


    R = np.array([np.append(u, [0]),
                  np.append(v, [0]),
                  np.append(n, [0]),
                  [0, 0, 0, 1]])

    Txyz = np.array([[1, 0, 0, -EYE[0]],
                     [0, 1, 0, -EYE[1]],
                     [0, 0, 1, -EYE[2]],
                     [0, 0, 0, 1]])

    return np.matmul(R, Txyz)

