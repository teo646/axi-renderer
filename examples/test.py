from objects import get_building1
from axiRenderer import world
from math import pi
from objects import Point
def main():

    w = world()
    w.put_object(get_building1(5, 7, 20), 0, 0, pi/6, 300, 200, 0)
    w.put_object(get_building1(3, 5, 30), 0, 0, 0, 400, 300, 0)
    w.put_object(get_building1(7, 7, 28), 0, 0, pi/3, 400, 200, 0)
    w.draw_digital_image(Point(0,0,200), Point(150,150,0))

if __name__ =="__main__":
    main()
