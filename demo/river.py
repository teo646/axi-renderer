from axiRenderer.objects import get_building1, get_building2, get_building1_corner, get_building2_corner
from axiRenderer.world import world
from math import pi
from axiRenderer.objects import Point
from axiRenderer.objects.river.river import River
import time
from axiRenderer.utils.display import display_3d

def main():
    w = world()
    w.put_object(get_building1(5, 7, 35), 0, 0, 0, 42, 200, 0)
    w.put_object(get_building1(3, 5, 35), 0, 0, 0, 101, 200, 0)
    w.put_object(get_building2(7, 7, 35), 0, 0, 0, 160, 200, 0)
    w.put_object(get_building2(7, 3, 35), 0, 0, 0, 210, 200, 0)
    w.put_object(get_building2(9, 9, 35), 0, 0, 0, 269, 200, 0)
    w.put_object(get_building2(3, 3, 35), 0, 0, 0, 328, 200, 0)
    w.put_object(get_building2(6, 7, 35), 0, 0, 0, 378, 200, 0)
    w.put_object(get_building2(2, 5, 35), 0, 0, 0, 437, 200, 0)
    w.put_object(get_building1(2, 3, 35), 0, 0, 0, 24, 150, 0)
    w.put_object(get_building1(5, 5, 35), 0, 0, 0, 65, 150, 0)
    w.put_object(get_building2(8, 7, 35), 0, 0, 0, 124, 150, 0)
    w.put_object(get_building1(5, 3, 35), 0, 0, 0, 174, 150, 0)
    w.put_object(get_building2(6, 6, 35), 0, 0, 0, 229.5, 150, 0)
    w.put_object(get_building2(7, 5, 35), 0, 0, 0, 284, 150, 0)
    w.put_object(get_building2(4, 3, 35), 0, 0, 0, 334, 150, 0)
    w.put_object(get_building2(6, 11, 35), 0, 0, 0, 402, 150, 0)
    w.put_object(River(200, 800, w), 0,0,0,200, -5,0)
    w.draw_digital_image(Point(100,100, 70), Point(120,150,30))

if __name__ =="__main__":
    main()