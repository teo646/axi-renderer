import matplotlib.pyplot as plt
from .color import cv2_color_to_plt_color

def display_3d(mesh_or_object_or_world):
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection='3d')
    plt.xlabel('x')
    plt.ylabel('y')

    #if it is mesh object
    if(hasattr(mesh_or_object_or_world, 'meshes')):
        target = mesh_or_object_or_world.meshes
    elif(hasattr(mesh_or_object_or_world, 'objects')):
        target = [mesh for object_ in mesh_or_object_or_world.objects for mesh in object_.meshes]
    else:
        target = mesh_or_object_or_world.meshes

    for mesh in target:
        for path in mesh.paths:
            for p1, p2 in zip(path.points, path.points[1:]):
                ax.plot([p1.coordinate[0], p2.coordinate[0]],
                        [p1.coordinate[1], p2.coordinate[1]],
                        zs=[p1.coordinate[2], p2.coordinate[2]],
                        color=cv2_color_to_plt_color(path.pen[0]),
                        linewidth = path.pen[1])
    plt.show()

def display_3d_vertices(world):
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection='3d')
    plt.xlabel('x')
    plt.ylabel('y')

    meshes = [mesh for object_ in world.objects for mesh in object_.meshes]

    for mesh in meshes:
        for p1, p2 in zip(mesh.vertices, mesh.vertices[1:]):
                ax.plot([p1.coordinate[0], p2.coordinate[0]],
                        [p1.coordinate[1], p2.coordinate[1]],
                        zs=[p1.coordinate[2], p2.coordinate[2]],
                        color=(0,0,0),
                        linewidth = 3)

    plt.show()
