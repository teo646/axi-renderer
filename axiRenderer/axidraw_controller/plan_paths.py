from axiRenderer.objects import Point

def find_nearest_path(point, paths):
    nearest_path = paths[0]
    min_distance = get_squared_distance(nearest_path.points[0], point)

    for path in paths:
        distance = get_squared_distance(path.points[0], point)
        if(distance == 0):
            return path
        if(min_distance > distance):
            nearest_path = path
            min_distance = distance

        distance = get_squared_distance(path.points[-1], point)
        if(distance == 0):
            path.points.reverse()
            return path
        if(min_distance > distance):
            path.points.reverse()
            nearest_path = path
            min_distance = distance
    
    return nearest_path


def get_squared_distance(point1, point2):
    return (point1.coordinate[0] - point2.coordinate[0])**2\
            + (point1.coordinate[1] - point2.coordinate[1])**2

def arrange_paths(paths):
    starting_path = find_nearest_path(Point(0,0), paths)
    arranged_paths = [starting_path]
    current_point = starting_path.points[1]
    paths.remove(starting_path)
    
    while len(paths) != 0:
        next_path = find_nearest_path(current_point, paths)
        arranged_paths.append(next_path)
        current_point = next_path.points[1]
        paths.remove(next_path)

    return arranged_paths

    
def classify_paths_by_pen(paths):
    classified_paths = {}
    for path in paths:
        if(path.pen in classified_paths.keys()):
            classified_paths[path.pen].append(path)
        else:
            classified_paths[path.pen] = [path]
    return classified_paths

def plan_paths(paths):
    classified_paths = classify_paths_by_pen(paths)

    for pen in classified_paths:
        classified_paths[pen] = arrange_paths(classified_paths[pen])

    return classified_paths

