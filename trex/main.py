import cv2
import numpy as np
import time
import mss
from math import dist

cv2.namedWindow('Main', cv2.WINDOW_NORMAL)
cv2.namedWindow('Game', cv2.WINDOW_NORMAL)
cv2.moveWindow('Main', 50, 50)
cv2.moveWindow('Game', 50, 50)

game_area = None
with mss.mss() as sct:
    monitor = sct.monitors[1]
    while True:
        screen = np.array(sct.grab(monitor))[:, :, :-1]
        if game_area is not None: #если не пуста область игры, она обнолвяется. 
            #дальше работаю только с ней
            cv2.destroyWindow('Main')
            game_area = screen[y:y+h, x:x+w]
            cv2.imshow('Game', game_area)
        else: cv2.imshow('Main', screen)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('й') or key == 27:
            break
        if key == ord('a') or key == ord('ф'): #ищем область игры
            x, y, w, h = cv2.selectROI('roi', screen)
            game_area = screen[y:y+h, x:x+w]
            cv2.imshow('Game', game_area)
            cv2.destroyWindow('roi')
        

cv2.destroyAllWindows()


