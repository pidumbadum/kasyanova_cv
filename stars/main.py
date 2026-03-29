import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from skimage.morphology import (opening, dilation, closing, erosion)

image = np.load("./stars.npy")

# image_test = np.array([[1, 0, 1, 0, 0, 0, 0],
#        [0, 1, 0, 0, 0, 0, 0],
#        [1, 0, 1, 0, 0, 0, 0],
#        [0, 0, 0, 0, 1, 1, 1],
#        [0, 1, 0, 0, 1, 1, 1],
#        [1, 1, 1, 0, 0, 0, 0],
#        [0, 1, 0, 0, 0, 0, 0]], dtype='uint8')

count_stars = 0
mask =np.ones((2, 2))
clened_image = closing(image_test, mask)

# def find_4neighbours(y, x):
#     return ((y-1, x), (y, x+1), (y-1,x), (y,x-1))
#
# def find_4Xneighbours(y, x):
#     return ((y-1, x+1), (y+1, x+1), (y+1,x -1), (y-1,x-1))
#
# def find_star(y, x):
#     if np.all(find_4neighbours(y,x) == 1) or np.all(find_4Xneighbours(y,x) == 1):
#         count_stars += 1
#     return count_stars

plt.subplot(121)
plt.imshow(image_test)
plt.subplot(122)
plt.imshow(clened_image)
plt.show()