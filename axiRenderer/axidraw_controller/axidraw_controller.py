from .arrange_lines import plan_lines
from pyaxidraw import axidraw
import numpy as np
import cv2

DIGITAL_IMAGE_MAGNIFICATION = 20

def draw_lines(lines, is_axidraw_drawing, is_digital_drawing):
    print("arranging lines")
    lines = plan_lines(lines)
    print("arranging lines done")
    if(is_axidraw_drawing):
        ad = axidraw.AxiDraw() # Initialize class

        ad.interactive()            # Enter interactive mode
        connected = ad.connect()    # Open serial port to AxiDraw

        if not connected:
            is_axidraw_drawing = False


    if(is_digital_drawing):
        digital_image = np.full((297*DIGITAL_IMAGE_MAGNIFICATION, 420*DIGITAL_IMAGE_MAGNIFICATION ,3), 255, dtype='uint8')


    for pen in lines:
        if(is_axidraw_drawing):
            print("equip ", pen, "on the axidraw")
            while 1:
                input_ = str(input())
                if(input_ == ""):
                    break

        for line in lines[pen]:
            if(is_axidraw_drawing):
                #put some code to move axidraw
                pass
            if(is_digital_drawing):
                print(line)
                print(pen)
                digital_image = cv2.line(digital_image, line[0].cv2_version(), line[1].cv2_version(), pen[0], pen[1])
                cv2.imshow('frame',digital_image)
                cv2.waitKey(1)


    cv2.destroyAllWindows()

