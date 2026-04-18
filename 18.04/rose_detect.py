import cv2
import matplotlib.pyplot as plt
import numpy as np

image = cv2.imread('./18.04/rose.jpg', cv2.IMREAD_COLOR_RGB) 
hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

lower = np.array([0, 0, 95])
upper = np.array([0, 255, 255])
mask = cv2.inRange(hsv, lower, upper)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((21, 21)))

result = cv2.bitwise_and(image, image, mask = mask)


plt.imshow(result)
plt.clim(0, 255)
plt.show()   