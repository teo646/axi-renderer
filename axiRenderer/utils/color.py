

def cv2_color_to_plt_color(rgb):
    return tuple(i/255 for i in rgb)[::-1]

