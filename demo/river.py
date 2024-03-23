from axiRenderer.objects import get_building1, get_building2, get_building1_corner, get_building2_corner
from axiRenderer.world import world
from axiRenderer.axidraw_controller.axidraw_controller import AxidrawController
from math import pi
from axiRenderer.objects import Point
from axiRenderer.objects.river.river import River
import time
from axiRenderer.utils.display import display_3d

def main():
    w = world()
    w.put_object(get_building1(5, 7, 35), 0, 0, 0, 21, 100, 0, 0.5)
    w.put_object(get_building1(3, 5, 35), 0, 0, 0, 50.5, 100, 0, 0.5)
    w.put_object(get_building2(7, 7, 35), 0, 0, 0, 80, 100, 0, 0.5)
    w.put_object(get_building2(7, 3, 35), 0, 0, 0, 105, 100, 0, 0.5)
    w.put_object(get_building2(9, 9, 35), 0, 0, 0, 134.5, 100, 0, 0.5)
    w.put_object(get_building2(3, 3, 35), 0, 0, 0, 164, 100, 0, 0.5)
    w.put_object(get_building2(6, 7, 35), 0, 0, 0, 189, 100, 0, 0.5)
    w.put_object(get_building2(2, 5, 35), 0, 0, 0, 218.5, 100, 0, 0.5)
    w.put_object(get_building1(2, 3, 35), 0, 0, 0, 12, 75, 0, 0.5)
    w.put_object(get_building1(5, 5, 35), 0, 0, 0, 32.5, 75, 0, 0.5)
    w.put_object(get_building2(8, 7, 35), 0, 0, 0, 62, 75, 0, 0.5)
    w.put_object(get_building1(5, 3, 35), 0, 0, 0, 87, 75, 0, 0.5)
    w.put_object(get_building2(6, 6, 35), 0, 0, 0, 114.75, 75, 0, 0.5)
    w.put_object(get_building2(7, 5, 35), 0, 0, 0, 142, 75, 0, 0.5)
    w.put_object(get_building2(4, 3, 35), 0, 0, 0, 167, 75, 0, 0.5)
    w.put_object(get_building2(6, 11, 35), 0, 0, 0, 201, 75, 0, 0.5)
    w.put_object(River(200, 800, w), 0,0,0,100, -2.5,0, 0.5)
    canvas = w.draw_digital_image(Point(100,100, 70), Point(120,150,30))
    ac = AxidrawController(canvas)
    print("press 'y' if you want to draw the image")
    ac.preview(20)
    if(str(input()) == 'y'):
        ac.draw(True, True)


if __name__ =="__main__":
    main()
