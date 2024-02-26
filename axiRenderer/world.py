from .util import get_view_transformation_matrix, get_world_transformaion_matrix, convert_rgb
import matplotlib.pyplot as plt

class world:
    def __init__(self):
        self.objects = []


    def put_object(self, object_, x_axis_rotation, y_axis_rotation, z_axis_rotation, 
                    x_axis_translation, y_axis_translation, z_axis_translation): 
        transformation_matrix = get_world_transformaion_matrix(x_axis_rotation,
                                                               y_axis_rotation,
                                                               z_axis_rotation,
                                                               x_axis_translation,
                                                               y_axis_translation,
                                                               z_axis_translation)
        self.objects.append(object_.transform(transformation_matrix))
        
    def back_face_culling(self):
        for object_ in self.objects:
            object_.back_face_culling()


    def view_transform(self, EYE, AT):
        transformation_matrix = get_view_transformation_matrix(EYE, AT)
        for object_ in self.objects:
            object_.transform(transformation_matrix)


    def display(self, EYE, AT):
        self.view_transform(EYE, AT)
        self.back_face_culling()

        fig = plt.figure(figsize=(9, 6))
        ax = fig.add_subplot(111, projection='3d', aspect='equal')
        ax.axes.set_aspect(aspect='equal')
        plt.xlabel('x')
        plt.ylabel('y')
        for object_ in self.objects:
            for mesh in object_.meshes:
                for line_segment in mesh.line_segments:
                    p1 = mesh.points[line_segment.point1_index]
                    p2 = mesh.points[line_segment.point2_index]
                    ax.plot([p1.coordinate[0], p2.coordinate[0]],
                            [p1.coordinate[1], p2.coordinate[1]],
                            zs=[p1.coordinate[2], p2.coordinate[2]],
                            color=convert_rgb(line_segment.color),
                            linewidth = line_segment.thickness)
        ax.view_init(90, -90)
        plt.show()

    def draw_digital_image(self, EYE, AT):


