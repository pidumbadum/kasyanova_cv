import cv2
import time
import numpy as np
import matplotlib.pyplot as plt

cat = cv2.imread('./18.04/imjs/cat.png')
cat1 = cv2.cvtColor(cat, cv2.COLOR_BGR2GRAY)
cat2 = cv2.imread('./18.04/imjs/cat2.png',  cv2.IMREAD_GRAYSCALE)

diff = cv2.absdiff(cat1, cat2)
ret, mask = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
mask = cv2.dilate(mask, None, iterations=2)

countours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
print(len(countours))

for contours in countours:
    x,y,w,h = cv2.boundingRect(contours)
    cv2.rectangle(cat, (x, y), (x+w, y + h), (0, 255, 0), 2)

cv2.putText(cat, f'Diffs = {len(countours)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0)) 

cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
cv2.namedWindow('Difference', cv2.WINDOW_NORMAL)

cv2.imshow("Original", cat)
cv2.imshow('Difference', mask)
cv2.waitKey(0)
cv2.destroyAllWindows()