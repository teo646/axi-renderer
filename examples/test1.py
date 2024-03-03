from objects import get_building1
from axiRenderer import world
from math import pi
from objects import Point
def main():

    w = world()
    w.put_object(get_building1(5, 7, 35), 0, 0, 0, 42, 200, 0)
    w.put_object(get_building1(3, 5, 35), 0, 0, 0, 101, 200, 0)
    w.put_object(get_building1(7, 7, 35), 0, 0, 0, 160, 200, 0)
    w.put_object(get_building1(7, 3, 35), 0, 0, 0, 210, 200, 0)
    w.put_object(get_building1(7, 3, 35), 0, 0, 0, 210, 150, 0)
    w.display(Point(-100,-20,200), Point(-50,100,0))

if __name__ =="__main__":
    main()
