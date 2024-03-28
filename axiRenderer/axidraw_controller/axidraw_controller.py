from .plan_paths import plan_paths
from .crop_paths import crop_paths
from pyaxidraw import axidraw
import numpy as np
import cv2

#horizontal direction
SCREEN_DIR = 1
A3_X_LEN = 297
A3_Y_LEN = 420
class AxidrawController:
    def __init__(self, canvas, paper_x=A3_X_LEN, paper_y=A3_Y_LEN):
        self.paper_x = paper_x
        self.paper_y = paper_y
        self.paths = crop_paths(canvas.get_fitting_paths(0), self.paper_x, self.paper_y, 10)

    def preview(self, scale=20):

        image = np.full((self.paper_y*scale, self.paper_x*scale ,3), 255, dtype='uint8') 
        for path in self.paths:
            for p1, p2 in zip(path.points, path.points[1:]):
                p1_cv2 = np.array(p1.coordinate[:2]*scale, dtype="uint32")
                p2_cv2 = np.array(p2.coordinate[:2]*scale, dtype="uint32")
                image = cv2.line(image, p1_cv2, p2_cv2, path.pen[0], int(path.pen[1]*scale))
        if((SCREEN_DIR == 0) != (self.paper_x > self.paper_y)):
            image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        cv2.namedWindow("preview", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("preview", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('preview',image[::-1])
        cv2.imwrite('./output/image.jpg', image[::-1])
        cv2.waitKey(0)
        cv2.destroyWindow('preview') 

    def draw(self, is_axidraw_drawing, is_digital_drawing, scale=20):
        print("arranging lines ...")
        paths = plan_paths(self.paths)
        print("arranging lines done")

        #setup axidraw
        if(is_axidraw_drawing):
            ad = axidraw.AxiDraw() # Initialize class
            ad.interactive()            # Enter interactive mode
            connected = ad.connect()    # Open serial port to AxiDraw
            
            if not connected:
                is_axidraw_drawing = False
            else:
                ad.options.units = 2              # set working units to mm.
                ad.options.pen_pos_up = 60        # select a large range for the pen up/down swing
                ad.options.pen_pos_down = 41
                ad.options.model = 2
                ad.update()


        #setup digital image
        if(is_digital_drawing):
            digital_image = np.full((self.paper_y*scale, self.paper_x*scale ,3), 255, dtype='uint8')
            cv2.namedWindow("digital_image", cv2.WINDOW_NORMAL)
            cv2.moveWindow("digital_image", 900, -900)
            cv2.setWindowProperty("digital_image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        #draw image
        for pen in paths:
            if(is_axidraw_drawing):
                ad.goto(0, 0)
                print("equip ", pen, "on the axidraw")
                while 1:
                    input_ = str(input())
                    if(input_ == ""):
                        break

            for path in paths[pen]:
                if(is_axidraw_drawing):
                    ad.draw_path([point.coordinate[:2][::-1] for point in path.points])     
                if(is_digital_drawing):
                    for p1, p2 in zip(path.points, path.points[1:]):
                        p1_cv2 = np.array(p1.coordinate[:2]*scale, dtype="uint32")
                        p2_cv2 = np.array(p2.coordinate[:2]*scale, dtype="uint32")
                        digital_image = cv2.line(digital_image, p1_cv2, p2_cv2, pen[0], int(pen[1]*scale))

                    if((SCREEN_DIR == 0) != (self.paper_x > self.paper_y)):
                        digital_image = cv2.rotate(digital_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
                        cv2.imshow('digital_image',digital_image[::-1])
                        digital_image = cv2.rotate(digital_image, cv2.ROTATE_90_CLOCKWISE)

                    else:
                        cv2.imshow('digital_image',digital_image[::-1])

                    cv2.waitKey(1)
    

        #terminate process
        if(is_axidraw_drawing):
            ad.goto(0, 0)
            ad.disconnect()
        if(is_digital_drawing):
            cv2.waitKey(0)
            cv2.destroyAllWindows()

