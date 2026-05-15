import cv2
import numpy as np
import time
import mss
import pyautogui
from pathlib import Path
from math import dist

save_path = Path(__file__).parent
trex_path = save_path/'trex.npy'
    

# cv2.namedWindow('Main', cv2.WINDOW_NORMAL)
cv2.namedWindow('test', cv2.WINDOW_NORMAL)
cv2.namedWindow('Game', cv2.WINDOW_NORMAL)
cv2.moveWindow('Game', 50, 50)
cv2.namedWindow('mask', cv2.WINDOW_NORMAL)
cv2.moveWindow('mask', 50, 350)

struct =  np.ones((5,5), dtype = 'u1')
game_area = None
danger_box = None
#попытка обрезать опасную зону до минимума
y_trex_min = 0
y_trex_max = 0
x_db = 0

last_jump_time = 0.0
JUMP_COOLDOWN = 0.69 

with mss.mss() as sct:
    monitor = sct.monitors[1]
    if trex_path.exists():
        trex_mask = np.load(trex_path)
    else:
        screen1 = np.array(sct.grab(monitor))[:, :, :-1]
        screen1 = cv2.cvtColor(screen1, cv2.COLOR_RGB2GRAY)

        #находим трекса впервые
        x1, y1, w1, h1 = cv2.selectROI('roi', screen1)
        if w1 > 0 and h1 > 0: 
            trex_mask = screen1[y1:y1+h1, x1:x1+w1]
            _, trex_mask = cv2.threshold(trex_mask, 120, 255, cv2.THRESH_BINARY_INV)
            trex_mask = cv2.morphologyEx(trex_mask, cv2.MORPH_OPEN, struct)
            coords = np.where(trex_mask > 0)     
        if len(coords[0]) != 0:
            y_min, y_max = coords[0].min(), coords[0].max()
            x_min, x_max = coords[1].min(), coords[1].max()
            trex_mask = trex_mask[y_min:y_max + 1, x_min:x_max + 1]       
        np.save(save_path/'trex.npy', trex_mask)
        cv2.destroyWindow('roi')

    prev_time = time.time()
    while True:
        screen = np.array(sct.grab(monitor))[:, :, :-1]
        screen = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
        if game_area is not None: 
            #если не пуста область игры, она обнолвяется. 
            #дальше работаю только с ней
            game_area = screen[y:y+h, x:x+w]
            _, binary_g = cv2.threshold(game_area, 120, 255, cv2.THRESH_BINARY_INV)
            binary_g = cv2.morphologyEx(binary_g, cv2.MORPH_OPEN, struct)

            #нахождение динозавра в процессе игры
            res = cv2.matchTemplate(binary_g, trex_mask, cv2.TM_CCOEFF_NORMED) # вот это двигает по изображению в поисках совпадений
            _, max_val, _, max_loc = cv2.minMaxLoc(res) #а это возвращает самое похожее
            if max_val > 0.5:
                x_trex, y_trex = max_loc #левые верхние координаты
                h_trex, w_trex = trex_mask.shape
                cv2.rectangle(game_area, (x_trex, y_trex), (x_trex + w_trex, y_trex + h_trex), 0, 2)
                # binary_g[:y_trex +h_trex + 1, :x_trex+ w_trex+ 1] = 0
                #Определяю пространство danger_box
                if y_trex > y_trex_min or x_trex + w_trex > x_db: 
                    y_trex_min = y_trex 
                    y_trex_max = y_trex + h_trex
                    x_db = x_trex + w_trex + 10
                    y_long_db = y_trex_min + int(h_trex * 0.25)
                    #срезы
                    common_db = binary_g[y_trex_min:y_trex_max, x_db:int(x_db * 2.7)].copy()
                    danger_box = binary_g[y_trex_min:y_trex_max, x_db: x_db + int(common_db.shape[1] * 0.75)].copy()
                    long_danger_box = binary_g[y_long_db:y_trex_max, x_db: x_db + common_db.shape[1]].copy()
                    #подсчет препятсвий 
                    near_count = np.count_nonzero(danger_box)
                    far_count  = np.count_nonzero(long_danger_box)
            
            #вторая версия прыжка
            if danger_box is not None:
                common_curr = np.count_nonzero(binary_g[y_trex_min:y_trex_max, x_db:int(x_db * 2.7)].copy())
                curr_nc = np.count_nonzero(binary_g[y_trex_min:y_trex_max, x_db: x_db + int(common_db.shape[1] * 0.75)].copy())
                curr_fc  = np.count_nonzero(binary_g[y_long_db:y_trex_max, x_db: x_db + common_db.shape[1]].copy())

                now = time.time()
                if near_count != curr_nc and now - last_jump_time > JUMP_COOLDOWN:
                    pyautogui.press('space')
                    near_count = curr_nc
                    last_jump_time = now
                elif far_count != curr_fc and curr_fc <= common_curr and now - last_jump_time > JUMP_COOLDOWN:
                    pyautogui.press('space')
                    far_count = curr_fc
                    last_jump_time = now
                cv2.imshow('test', long_danger_box)
                    
            #рисую danger box
            if danger_box is not None:
                cv2.rectangle(game_area, (x_db, y_trex_min), (x_db + common_db.shape[1], y_trex_min + common_db.shape[0]), 0, 2)
                cv2.rectangle(game_area, (x_db, y_trex_min), (x_db + danger_box.shape[1], y_trex_min + danger_box.shape[0]), 0, 2)
                cv2.rectangle(game_area, (x_db, y_long_db), (x_db + long_danger_box.shape[1], y_long_db + long_danger_box.shape[0]), 0, 2)
                        

            #cv2.rectangle(game_area, (x_trex, y_trex), (x_trex + w_trex, y_trex + h_trex), (0, 255, 0), 2)


            cv2.imshow('Game', game_area)
            cv2.imshow('mask', binary_g)


        #ТУТ НИЧЕ НЕ ТРОГАЙ ТУТ УЖЕ ГОТВО
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key ==27 or key == ord('1'):
            break
        if key == ord('a') or key == ord('2'): #ищем область игры
            x, y, w, h = cv2.selectROI('roi', screen)
            if w > 0 and h > 0:  
                game_area = screen[y:y+h, x:x+w]
                cv2.destroyWindow('roi')
                _, binary_g = cv2.threshold(game_area, 120, 255, cv2.THRESH_BINARY_INV)
                binary_g = cv2.morphologyEx(binary_g, cv2.MORPH_OPEN, struct)

        current_time = time.time()
        delta = current_time - prev_time
        prev_time = current_time
        print(f'{delta:.2f}')
        

cv2.destroyAllWindows()