





import cv2
import numpy as np

# orange 1 : [0,101,203 ] => [[[ 15 255 203]]]

# orange 2 : [7,102,203 ]



color = np.uint8([[[7,102,203 ]]])
hsv_color = cv2.cvtColor(color,cv2.COLOR_BGR2HSV)
print(hsv_color)