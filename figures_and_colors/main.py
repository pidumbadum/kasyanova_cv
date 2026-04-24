import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label

colors = [[0, 9, 'red'], [160, 180, 'red'], [10, 24, 'orange'], [25, 39, 'yellow'],
          [40, 84, 'green'], [85, 100, 'cyan'], [101, 140, 'blue'], [130, 160, 'purple']]

#Загружаем изображение
image = cv2.imread('./balls_and_rects.png', cv2.IMREAD_COLOR_RGB)
hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
count_figures = label(image).max()
check_count = 0

# атут ищем все фигуры нужного цвета
for color in colors:
    lower = np.array([color[0], 0, 20])
    upper = np.array([color[1], 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(image, image, mask=mask)
    print(f'Count of {color[2]} figures = {label(result).max()}')
    check_count += label(result).max()
    plt.imshow(result)
    plt.title(color[2])
    plt.pause(2)
    plt.close()

print(f'Difference between figure count and check count = {count_figures - check_count}')
# lower = np.array([120, 0, 20])
# upper = np.array([220, 255, 255])
# mask = cv2.inRange(hsv, lower, upper)
# result = cv2.bitwise_and(image, image, mask = mask)

#В принципе на этом можно было бы и продолжить, но хочу сделать поиск цвета автоматическим,
# либо как вариант, просто задать значения по умолчанию и пройтись по ним всем,
# это может сработать с любым изображенрием.
#Что касается поиска фигур, можно просто обрезать их по длине, ширине.
# Площадь не совпадает с обрезкой? - круг.
# Совпадает? - прямоугольник, третьего то не дано

# plt.subplot(121)
# plt.imshow(image)
# plt.subplot(122)
# plt.imshow(result)
# plt.show()