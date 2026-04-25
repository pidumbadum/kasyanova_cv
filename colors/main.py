import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from skimage.io import imread
from skimage.color import rgb2hsv

image = imread("./colors/balls.png")
print(image.shape)
hsv = rgb2hsv(image)
h = hsv[:,:,0]

colors =[]
for color in np.unique(h):
    binary = h == color
    labeled =label(binary)
    colors.extend([color] * int(np.max(labeled)))

print(len(colors))
groups = [[colors[1]]]
delta = 0.05
cgrp = 0
for i in range(2, len(colors) - 1):
    if len(groups[-1]) == 0:
        groups[-1].append(colors[i])
        continue
    if abs(colors[i-1]- colors[i]) < delta:
        groups[-1].append(colors[i])
    else:
        groups.append([colors[i]])

for grp in groups:
    print(np.mean(grp), len(grp))

plt.subplot(121)
plt.imshow(h)
plt.subplot(122)
plt.plot(np.unique(h), 'o-')
plt.show()