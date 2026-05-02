import cv2
import numpy as np

cv2.namedWindow('image', cv2.WINDOW_GUI_NORMAL)
image = cv2.imread("./25.04/contours/defects.png")

gray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #CHAIN_APPROX_SIMPLE - уменьщение точек
cv2.drawContours(image, contours, 0, (255, 0,0), 3)

rect= contours[0]
hull = cv2.convexHull(rect)
cv2.drawContours(image, [hull], 0, (0, 255, 0), 6)

indexes = cv2.convexHull(rect, returnPoints=False)
defects = cv2.convexityDefects(rect, indexes)

for p in defects:
    s,e,f,d = p[0]
    cv2.circle(image, tuple(*rect[s]), 6, (0, 0, 255), 5)
    cv2.circle(image, tuple(*rect[e]), 6, (0, 255, 255), 5)
    cv2.circle(image, tuple(*rect[f]), 6, (255, 0, 255), 5)

cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()