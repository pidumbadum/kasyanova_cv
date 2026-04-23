import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label

image = cv2.imread('./balls_and_rects.png', cv2.IMREAD_COLOR_RGB)
hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
labeled = label(image)

lower = np.array([120, 0, 20])
upper = np.array([220, 255, 255])
mask = cv2.inRange(hsv, lower, upper)
result = cv2.bitwise_and(image, image, mask = mask)

#В принципе на этом можно было бы и продолжить, но хочу сделать поиск цвета автоматическим,
# либо как вариант, просто задать значения по умолчанию и пройтись по ним всем,
# это может сработать с любым изображенрием.
#Что касается поиска фигур, можно просто обрезать их по длине, ширине.
# Площадь не совпадает с обрезкой? - круг.
# Совпадает? - прямоугольник, третьего то не дано

plt.subplot(121)
plt.imshow(image)
plt.subplot(122)
plt.imshow(result)
plt.show()