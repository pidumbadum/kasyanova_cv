#pip install opencv-python
import cv2
import numpy as np

cv2.namedWindow("Camera", cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("background", cv2.WINDOW_GUI_NORMAL)
cam = cv2.VideoCapture(0+cv2.CAP_DSHOW)#для винды 0+cv2.CAP_DSHOW

background = None
prev_delta = None
while cam.isOpened():
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (51,51), 0)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord('b'):
        background = gray.copy()
    if background is not None:
        delta = cv2.absdiff(background, gray)
        if prev_delta is not None:
            changes = (np.abs(delta, prev_delta).sum() / 255 / delta.size)
            cv2.putText(frame, f'Diffs = {changes:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0)) 
            if changes < 0.1:
                background = gray.copy()

        prev_delta = delta
        ret, mask = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)
        mask = cv2.dilate(mask,None, iterations=3)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:
                x,y,w,h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y),(x+ w, y+ h), (0, 255, 0),3 )

        cv2.imshow('Backgroud', mask)

    cv2.imshow("Camera", frame)

cam.release()
cv2.destroyAllWindows()