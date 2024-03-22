from axiRenderer.objects import Point

def find_nearest_line(point, lines):
    nearest_line = lines[0]
    min_distance = get_squared_distance(nearest_line[0], point)

    for line in lines:
        distance = get_squared_distance(line[0], point)
        if(distance == 0):
            return line
        if(min_distance > distance):
            starting_line = line
            min_distance = distance

        distance = get_squared_distance(line[1], point)
        if(distance == 0):
            line.reverse()
            return line
        if(min_distance > distance):
            line.reverse()
            starting_line = line
            min_distance = distance
    
    return nearest_line


def get_squared_distance(point1, point2):
    return (point1.coordinate[0] - point2.coordinate[1])**2\
            + (point1.coordinate[1] - point2.coordinate[1])**2

def arrange_lines_with_same_color(lines):
    
    starting_line = find_nearest_line(Point(0,0), lines)
    arranged_lines = [starting_line]
    current_point = starting_line[1]
    lines.remove(starting_line)
    
    while len(lines) != 0:
        next_line = find_nearest_line(current_point, lines)
        arranged_lines.append(next_line)
        current_point = next_line[1]
        lines.remove(next_line)

    return arranged_lines

    
def classify_lines_by_pen(lines):
    classified_lines = {}
    for line in lines:
        if(line[2] in classified_lines.keys()):
            classified_lines[line[2]].append([line[0], line[1]])
        else:
            classified_lines[line[2]] = [[line[0], line[1]]]
    return classified_lines

def plan_lines(lines):
    classified_lines = classify_lines_by_pen(lines)

    for pen in classified_lines:
        classified_lines[pen] = arrange_lines_with_same_color(classified_lines[pen])

    return classified_lines

