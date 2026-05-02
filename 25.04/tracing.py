import cv2
import numpy as np

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
        lower = np.clip(color*0.8, 0,255).astype("u1")
        upper = np.clip(color*1.2, 0,255).astype("u1")
        upper[1] = 255
        upper[2] = 255
    if lower is not None:
        inr = cv2.inRange(hsv, lower, upper)
        mask = cv2.morphologyEx(inr, cv2.MORPH_CLOSE, np.ones((5, 5), dtype="uint8"))
        counturs, _ = cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame, counturs, -1, (0, 255, 0), 4)
        # cv2.circle(frame, )
        cv2.imshow('Mask', mask)
    cv2.imshow('Image', frame)
cv2.destroyAllWindows()
