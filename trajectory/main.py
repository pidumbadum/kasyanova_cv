import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label
from pathlib import Path
import re

def distance(p1, p2):
    return ((p2[1] - p1[1]) **2 + (p2[0] - p1[0]) **2)** 0.5

def find_min_distance(point1, array):
    min_dist = 2 ** 10
    ind = 0
    for a in range(len(array)):
        dist = distance(point1, array[a])
        if min_dist > dist:
            min_dist = dist
            ind = a
    return ind

def centroid(labeled, lab=1):
    ys, xs = np.where(labeled == lab)
    cy = np.mean(ys)
    cx = np.mean(xs)
    return cy,cx

folder = Path('./out')
files = []
for file in folder.iterdir():
    if file.is_file():
        files.append(file)

files.sort(key=lambda x: int(re.findall(r'\d+', x.name)[0]))
#Точно забуду, поэтому:
#lambda x: - lambda(безымянная функция) которая получает x, после : идет то, что должна вернуть эта фуцнкция
# re.findall(r'\d+', x.name)[0]) - поиск по маске всех чисел, взятие первого числа(в дан сл не надо, но на всякий)
# sort выполняется по результату функции после key=, которая в свою очередь достает первое число из названия файла

all_centers = []
centers_before = []
centers_now = [(0, 0), (0, 0), (0, 0)]
labeled_i1 = label(np.load(files[0]))
for i in range(1, np.max(labeled_i1) + 1):
    centers_before.append(centroid(labeled_i1, i))

for file in files:
    labeled_imNow = label(np.load(file))
    for i in range(1, np.max(labeled_imNow) + 1):
        center = centroid(labeled_imNow, i)
        index = find_min_distance(center, centers_before)
        centers_now[index] = center
    centers_before = centers_now.copy()
    all_centers.append(centers_now.copy())

for i in range(len(all_centers)):
    print(all_centers[i])



#посомотреть последовательный вывод изображений:
# for file in files:
#     img = np.load(file)
#
#     plt.clf() #очисточка
#
#     plt.imshow(img)
#     plt.axis('off')
#     plt.title(f'Показ: {file}')
#
#     plt.pause(0.03)
#
# plt.show()
