

def get_overlaying_meshes(meshes, coordinate):
    overlaying_meshes = []
    for mesh in meshes:
        if(mesh.is_including_point(coordinate)):
            overlaying_meshes.append(mesh)
    return overlaying_meshes


def get_order_of_meshes_on_point(meshes, coordinate):
    overlaying_meshes = get_overlaying_meshes(meshes, coordinate)
    return sorted(overlaying_meshes, key = lambda mesh: mesh.get_z_value_on_the_plane(coordinate), reverse = True)


def merge_lists_and_maintain_order(lists):
    class Node_element:
        def __init__(self, value):
            self.value = value
            self.predecessor = set()
            self.successor = set()
            self.collected = False

    elements = {}
    for list_ in lists:
        if(len(list_) == 1):
            if list_[0] not in elements:
                elements[list_[0]] = Node_element(list_[0])
        for i in range(len(list_) - 1):
            value = list_[i]
            next_value = list_[i + 1]
            if value not in elements:
                elements[value] = Node_element(value)
            if next_value not in elements:
                elements[next_value] = Node_element(next_value)
            node = elements[value]
            next_node = elements[next_value]
            node.successor.add(next_node)
            next_node.predecessor.add(node)

    def add_elements_in_array(head, array):
        areAllPredecessorsCollected = True
        for element in head.predecessor:
            if not element.collected:
                areAllPredecessorsCollected = False
                break
        if not areAllPredecessorsCollected:
            return
        array.append(head.value)
        head.collected = True
        for element in head.successor:
            if not element.collected:
                add_elements_in_array(element, array)

    results = []
    for element in elements.values():
        if len(element.predecessor) == 0:
            add_elements_in_array(element, results)
    return results



#input 2d transformed meshes to get order for drawing
def arrange_mesh(transformed_meshes):
    meshes = transformed_meshes
    mesh_ordered_lists = []
    for mesh in meshes:
        for vertice in mesh.get_vertices_after_offset():
            mesh_ordered_list = get_order_of_meshes_on_point(meshes, vertice)
            mesh_ordered_lists.append(mesh_ordered_list)


    return merge_lists_and_maintain_order(mesh_ordered_lists)
