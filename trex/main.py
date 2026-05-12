import cv2
import numpy as np
import time
import mss
from math import dist

cv2.namedWindow('Main', cv2.WINDOW_NORMAL)
cv2.moveWindow('Main', 50, 50)

with mss.mss() as sct:
    monitor = sct.monitors[1]

    while True:
        screen = np.array(sct.grab(monitor))
        cv2.imshow('Main', screen)

        key = cv2.waitKey(50) & 0xFF
        if key == ord('q') or key == ord('й') or key == 27:
            break

cv2.destroyAllWindows()


