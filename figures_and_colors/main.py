import cv2
import numpy as np
from skimage.measure import label

colors = [[0, 9, 'red'], [160, 180, 'red'], [10, 24, 'orange'], [25, 39, 'yellow'],
          [40, 84, 'green'], [85, 100, 'cyan'], [101, 129, 'blue'], [130, 160, 'purple']]

def rectangle_counter(labeled):
    rectangle_count = 0
    for i in range(1, labeled.max() + 1):
        peace = (labeled == i)
        h = np.sum(peace, axis=0).max()
        w = np.sum(peace, axis=1).max()
        if np.sum(peace) == h * w:
            rectangle_count += 1
    return rectangle_count

#Загружаем изображение
image = cv2.imread('./balls_and_rects.png', cv2.IMREAD_COLOR_RGB)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
count_figures = label(binary).max()
all_rect = rectangle_counter(label(binary))
print(f'all fig = {count_figures}, rect = {all_rect}, circ = {count_figures - all_rect} ')
check_count = 0

# атут ищем все фигуры нужного цвета
for color in colors:
    #оставляем только нужный цвет
    lower = np.array([color[0], 0, 20])
    upper = np.array([color[1], 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(image, image, mask=mask)
    result = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)
    _, result = cv2.threshold(result, 1, 255, cv2.THRESH_BINARY)
    result = label(result)
    #Считаем результат
    if result.max() != 0:
        rectangles_count = rectangle_counter(result)
        print(f'Count of {color[2]} figures = {result.max()}: '
              f'{rectangles_count} - rectangles, {result.max() - rectangles_count} - circus')

    check_count += result.max()

print(f'Difference between figure count and check count = {count_figures - check_count}')