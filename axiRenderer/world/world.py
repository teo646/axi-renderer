from axiRenderer.utils import get_view_transformation_matrix, get_world_transformaion_matrix, cv2_color_to_plt_color
from axiRenderer.utils.display import display_3d
from axiRenderer.drawing_canvas import canvas
import time
import matplotlib.pyplot as plt
from .mesh_arranger import arrange_meshes
import cv2
import numpy as np

class world:
    def __init__(self):
        self.objects = []


    def put_object(self, object_, x_axis_rotation, y_axis_rotation, z_axis_rotation, 
                    x_axis_translation, y_axis_translation, z_axis_translation, scale): 
        transformation_matrix = get_world_transformaion_matrix(x_axis_rotation,
                                                               y_axis_rotation,
                                                               z_axis_rotation,
                                                               x_axis_translation,
                                                               y_axis_translation,
                                                               z_axis_translation)
        scale_matrix = np.identity(4)
        scale_matrix[:3] *= scale
        transformation_matrix = np.matmul(transformation_matrix, scale_matrix)
        self.objects.append(object_.world_transform(transformation_matrix))


    def back_face_culling(self):
        self.objects = [object_.back_face_culling() for object_ in self.objects ]



    def view_transform(self, EYE, AT):
        transformation_matrix = get_view_transformation_matrix(EYE, AT)
        for object_ in self.objects:
            object_.view_transform(transformation_matrix)
     

    def draw_digital_image(self, EYE, AT):
        #start = time.time()
        self.view_transform(EYE, AT)
        self.back_face_culling()
        meshes = [mesh for object_ in self.objects for mesh in object_.meshes]
        meshes = arrange_meshes(meshes)
        c = canvas()
        for mesh in meshes:
            c = mesh.draw_digital_image(c)

        return c


                

        
