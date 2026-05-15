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

struct =  np.ones((3,3), dtype = 'u1')
game_area = None
common_db = None
#попытка обрезать опасную зону до минимума
y_trex_min = 0
y_trex_max = 0
x_db = 0

last_jump_time = 0.0
JUMP_COOLDOWN = 0.69 

prev_objs = None

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

                #Определяю пространство danger_box
                if y_trex > y_trex_min or x_trex + w_trex > x_db: 
                    y_trex_min = y_trex #Верх бошки
                    y_trex_max = y_trex + h_trex #низ тирекса
                    x_db = x_trex + w_trex + 10 #низ тирекса по иксу
                    #срезы
                    common_db = binary_g[y_trex_min:y_trex_max, x_db:int(x_db * 3)].copy()
                    #а тут выделяю пространство за для слежки за кактусами
                    cactus_vier = binary_g[:, x_db + common_db.shape[1]:].copy()
                    cactus_vier = cv2.morphologyEx(cactus_vier, cv2.MORPH_CLOSE, struct)
                    smesh = x_db + common_db.shape[1]
            if common_db is not None:
                #Анализ и поиск кактусов
                curr_cactv =  binary_g[:, x_db + common_db.shape[1]:].copy()
                cactus_vier = curr_cactv.copy()
                #ищуконтуры
                cactus_vier = cv2.dilate(cactus_vier, struct, iterations=2)
                cv2.imshow('test', common_db)
                #А где контур? а тут он
                contours, _ = cv2.findContours(cactus_vier, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                current_objs = []
                speed = 0.0

                for cnt in contours: # сначала нашли, теперь перебираем, я уже вижу просивший фпс
                    xcont, ycont, wcont, hcont = cv2.boundingRect(cnt)
                    cv2.rectangle(game_area, (smesh + xcont, ycont), (smesh + xcont + wcont, ycont +hcont), 0, 2)

                    if prev_objs:
                        closest_obj = min(prev_objs, key=lambda p: abs(p[0] - xcont)) #опять чудо функция нас спасает 
                        
                    current_objs.append([xcont, ycont, wcont, hcont])
                    prev_objs = current_objs

                # if current_objs:
                #     nearest_obj = min(current_objs, key=lambda obj: obj[0])
                #     width_obj = nearest_obj[2] - nearest_obj[0]
                #     heigth_obj = nearest_obj[3] - nearest_obj[1]
                #     if 

                    

            #вторая версия прыжка
            if common_db is not None:
                common_curr = binary_g[y_trex_min:y_trex_max, x_db:int(x_db * 3)].copy()
                diff = cv2.bitwise_xor(common_db, common_curr)
                change_ratio = np.count_nonzero(diff) / diff.size
                
                now = time.time()
                if change_ratio > 0.01 and now - last_jump_time > JUMP_COOLDOWN:
                    pyautogui.press('space')
                    last_jump_time = now
                
                common_db = common_curr.copy()


                    
            #рисую danger box
            if common_db is not None:
                # cv2.rectangle(game_area, (x_db, y_trex_min), (x_db + common_db.shape[1], y_trex_min + common_db.shape[0]), 0, 2)
                cv2.rectangle(game_area, (x_db + common_db.shape[1], 0), (game_area.shape[1], game_area.shape[0]), 0, 2)
                cv2.imshow('test', cactus_vier)
                        

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