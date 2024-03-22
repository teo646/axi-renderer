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
        self.meshes = []


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
        for mesh in object_.world_transform(transformation_matrix).meshes:
            self.meshes.append(mesh)


    def back_face_culling(self):
        processed_meshes = []
        for mesh in self.meshes:
            if(mesh.is_front_side()):
                processed_meshes.append(mesh)

        self.meshes = processed_meshes



    def view_transform(self, EYE, AT):
        transformation_matrix = get_view_transformation_matrix(EYE, AT)
        for mesh in self.meshes:
            mesh.view_transform(transformation_matrix)
     

    def display(self, EYE, AT):
        self.view_transform(EYE, AT)

        fig = plt.figure(figsize=(9, 6))
        ax = fig.add_subplot(111, projection='3d', aspect='equal')
        ax.axes.set_aspect(aspect='equal')
        plt.xlabel('x')
        plt.ylabel('y')
        for mesh in self.meshes:
            for line_segment in mesh.line_segments:
                p1 = mesh.points[line_segment.point1_index]
                p2 = mesh.points[line_segment.point2_index]
                ax.plot([p1.coordinate[0], p2.coordinate[0]],
                        [p1.coordinate[1], p2.coordinate[1]],
                        zs=[p1.coordinate[2], p2.coordinate[2]],
                        color=cv2_color_to_plt_color(line_segment.pen[0]),
                        linewidth = line_segment.pen[1])
        ax.view_init(90, -90)
        plt.show()


    def draw_digital_image(self, EYE, AT):
        #start = time.time()
        self.view_transform(EYE, AT)
        self.back_face_culling()
        self.meshes = arrange_meshes(self.meshes)
        c = canvas()
        for mesh in self.meshes:
            c = mesh.draw_digital_image(c)
        #end = time.time()
        #print("time spent: "+str(end - start))
        c.show(20)
        return c


                

        
