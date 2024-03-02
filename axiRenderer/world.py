from .util import get_view_transformation_matrix, get_world_transformaion_matrix, convert_rgb
import matplotlib.pyplot as plt
from .mesh_arranger import arrange_mesh
from maskCanvas import canvas, line_seg
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
        
    def back_face_culling(self):
        processed_meshes = []
        for mesh in self.meshes:
            if(mesh.is_front_side()):
                processed_meshes.append(mesh)

        self.meshes = processed_meshes



    def view_transform(self, EYE, AT):
        transformation_matrix = get_view_transformation_matrix(EYE, AT)
        for mesh in self.meshes:
            mesh.transform(transformation_matrix)


    def display(self, EYE, AT):
        self.view_transform(EYE, AT)
        self.back_face_culling()

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
                        color=convert_rgb(line_segment.color),
                        linewidth = line_segment.thickness)
        ax.view_init(90, -90)
        plt.show()



    def draw_digital_image(self, EYE, AT):
        self.view_transform(EYE, AT)
        self.back_face_culling()
        self.meshes = arrange_mesh(self.meshes)
        c = canvas()
        for mesh in self.meshes:
            for line_segment in mesh.line_segments:
                p1 = mesh.points[line_segment.point1_index].coordinate[:2]
                p2 = mesh.points[line_segment.point2_index].coordinate[:2]
                c.registerLineSeg(line_seg([p1,p2], color=line_segment.color, thickness = line_segment.thickness))
            c.registerMask([mesh.points[index].coordinate[:2] for index in mesh.vertices_index])


        cv2.namedWindow("Resized_Window", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Resized_Window", 700, 700)
        cv2.imshow("Resized_Window", c.draw(10)[::-1])
        cv2.waitKey(0)
        cv2.destroyAllWindows()

                

        
