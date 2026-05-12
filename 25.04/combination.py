import cv2
import numpy as np
import time
from math import dist
import json
from pathlib import Path

save_path = Path(__file__).parent

cv2.namedWindow('Image', cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow('Mask', cv2.WINDOW_GUI_NORMAL)

position=[0, 0]
clicked = False
def on_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"clicked at {x}, {y}")
        global position
        global clicked
        position = [x, y]
        clicked = True

cv2.setMouseCallback('Image', on_click)
capture = cv2.VideoCapture(0)
lower = None
upper = None
# config_path = save_path/"config.json"
# if config_path.exists():
#     with config_path.open('r') as f:
#         js = json.load(f)
#         if js['lower'] is not None:
#             print('aaaaa')
#             lower = np.array(js['lower'], dtype="u1")
#             upper = np.array(js['upper'], dtype="u1")
# positions =[]

speed = 0
prev_count = time.time()
curr_count = time.time()
d = 6.36 #cm
print(lower, upper)
while True:
    ret, frame = capture.read()
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    key = cv2.waitKey(55) & 0xFF
    if key == ord('q'):
        break
    if clicked:
        clicked = False
        color = hsv[position[1],position[0]]
        if lower is not None:
            lower = np.clip(color*0.85, 0,255).astype("u1")
            upper = np.clip(color*1.15, 0,255).astype("u1")
        upper[1] = 255
        upper[2] = 255
    if lower is not None:
        # if inr is not None:
        #     new_inr = cv2.inRange(hsv, lower, upper)
        #     inr = cv2.bitwise_or(inr, new_inr)
        # else:
        inr = cv2.inRange(hsv, lower, upper)
        mask = cv2.morphologyEx(inr, cv2.MORPH_CLOSE, np.ones((5, 5), dtype="uint8"))
        cv2.imshow('Mask', mask)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            contours = max(contours, key=cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(contours)
            if radius > 20:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)
    frame = cv2.flip(frame, 1)

    print(inr)
    cv2.imshow('Image', frame)
cv2.destroyAllWindows()


with (save_path/ "config.json").open('w') as f:
    json.dump({'lower': None if lower is None else lower.tolist(),
               'upper': None if upper is None else upper.tolist()}, f)