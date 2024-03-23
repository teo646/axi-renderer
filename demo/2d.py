from axiRenderer.objects import get_building1, get_building2, get_building1_corner, get_building2_corner
from axiRenderer.world import world
from math import pi
from axiRenderer.objects import Point
from axiRenderer.axidraw_controller.axidraw_controller import AxidrawController
import time
from axiRenderer.utils.display import display_3d

def main():
    w = world()
    w.put_object(get_building1(5, 7, 35), 0, 0, 0, 42, 200, 0, 0.3)
    canvas = w.draw_digital_image(Point(100,100, 100), Point(120,150,30))

    ac = AxidrawController(canvas)
    print("press 'y' if you want to draw the image")
    ac.preview(20)
    if(str(input()) == 'y'):
        ac.draw(True, True)
    
if __name__ =="__main__":
    main()
