import d3dshot
import cv2
import numpy as np
import time
# import scipy.misc



d = d3dshot.create(capture_output="numpy")
d.capture(target_fps=30)
time.sleep(5)
lastF = d.get_latest_frame()
cv2.imshow("crossout", cv2.cvtColor(lastF, cv2.COLOR_BGR2RGB))

# while True:
#     lastF = d.get_latest_frame()
#     cv2.imshow("crossout", cv2.cvtColor(lastF, cv2.COLOR_BGR2RGB))


print("a")
