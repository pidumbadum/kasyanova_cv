import cv2
import numpy as np
import time
import mss
from math import dist

cv2.namedWindow('Main', cv2.WINDOW_NORMAL)
cv2.namedWindow('Game', cv2.WINDOW_NORMAL)
cv2.moveWindow('Game', 50, 50)
cv2.namedWindow('mask', cv2.WINDOW_NORMAL)
cv2.moveWindow('mask', 250, 100)
cv2.moveWindow('Main', 50, 50)

struct =  np.ones((5,5), dtype = 'u1')
game_area = None

with mss.mss() as sct:
    monitor = sct.monitors[1]
    prev_time = time.time()
    while True:
        screen = np.array(sct.grab(monitor))[:, :, :-1]
        screen = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
        if game_area is None: 
             cv2.imshow('Main', screen)
        else:
            #если не пуста область игры, она обнолвяется. 
            #дальше работаю только с ней
            game_area = screen[y:y+h, x:x+w]
            cv2.imshow('Game', game_area)
            _, binary_g = cv2.threshold(game_area, 120, 255, cv2.THRESH_BINARY_INV)
            binary_g = cv2.morphologyEx(binary_g, cv2.MORPH_OPEN, struct)
            cv2.imshow('mask', binary_g)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key ==27 or key == ord('1'):
            break
        if key == ord('a') or key == ord('2'): #ищем область игры
            x, y, w, h = cv2.selectROI('roi', screen)
            if w > 0 and h > 0:  
                game_area = screen[y:y+h, x:x+w]
                cv2.destroyWindow('Main')
                cv2.destroyWindow('roi')

        current_time = time.time()
        delta = current_time - prev_time
        prev_time = current_time
        print(f'{delta:.2f}')
        

        
cv2.destroyAllWindows()