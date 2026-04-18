import cv2
import numpy as np
import matplotlib.pyplot as plt

cheb = cv2.imread('./18.04/imjs/cheburashka.jpg', cv2.IMREAD_COLOR_RGB) 
tv = cv2.imread('./18.04/imjs/news.jpg', cv2.IMREAD_COLOR_RGB)

rows, calls, _ = cheb.shape

pts1 = np.array([[0,0], [calls, 0], [calls, rows], [0, rows]], dtype = "f4")
plts2 = np.array([[17, 24], [430, 56], [430, 266], [41, 294]], dtype= 'f4')
m = cv2.getPerspectiveTransform(pts1, plts2)
print(m)
transformed = cv2.warpPerspective(cheb, m, (tv.shape[1], tv.shape[0]))
gray = cv2.cvtColor(transformed, cv2.COLOR_RGB2GRAY)
reast, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

bg = cv2.bitwise_and(tv, tv, mask= cv2.bitwise_not(mask))
fg = cv2.bitwise_and(transformed, transformed, mask= mask)
result = cv2.add(bg, fg)

plt.imshow(result)
plt.show()