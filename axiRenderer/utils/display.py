import matplotlib.pyplot as plt
from .color import cv2_color_to_plt_color

def display_3d(mesh_or_object_or_world):
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection='3d')
    plt.xlabel('x')
    plt.ylabel('y')

    #if it is mesh object
    if(not hasattr(mesh_or_object_or_world, 'meshes')):
        target = [mesh_or_object_or_world]
    else:
        target = mesh_or_object_or_world.meshes

    for mesh in target:
        for line_segment in mesh.line_segments:
            p1 = mesh.points[line_segment.point1_index]
            p2 = mesh.points[line_segment.point2_index]
            ax.plot([p1.coordinate[0], p2.coordinate[0]],
                    [p1.coordinate[1], p2.coordinate[1]],
                    zs=[p1.coordinate[2], p2.coordinate[2]],
                    color=cv2_color_to_plt_color(line_segment.pen[0]),
                    linewidth = line_segment.pen[1])
    plt.show()


