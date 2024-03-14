from axiRenderer.utils import get_view_transformation_matrix, get_world_transformaion_matrix, cv2_color_to_plt_color
from axiRenderer.utils.display import display_3d
from axiRenderer.drawing_canvas import canvas
import time
import matplotlib.pyplot as plt
from .mesh_arranger import arrange_meshes
import cv2

class world:
    def __init__(self):
        self.meshes = []


    def put_object(self, object_, x_axis_rotation, y_axis_rotation, z_axis_rotation, 
                    x_axis_translation, y_axis_translation, z_axis_translation): 
        transformation_matrix = get_world_transformaion_matrix(x_axis_rotation,
                                                               y_axis_rotation,
                                                               z_axis_rotation,
                                                               x_axis_translation,
                                                               y_axis_translation,
                                                               z_axis_translation)
        for mesh in object_.meshes:
            self.meshes.append(mesh.transform(transformation_matrix))
        

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
                        color=cv2_color_to_plt_color(line_segment.color),
                        linewidth = line_segment.thickness)
        ax.view_init(90, -90)
        plt.show()



    def draw_digital_image(self, EYE, AT):
        self.meshes = arrange_meshes(self.meshes)
        view_transformation_matrix = get_view_transformation_matrix(EYE, AT)
        c = canvas()
        for mesh in self.meshes:
            c = mesh.draw_digital_image(c, view_transformation_matrix)
        c.show(10)


                

        
