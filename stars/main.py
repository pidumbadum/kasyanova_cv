import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label

image = np.load("./stars.npy")
count_stars = 0

def find_4neighbours(y, x):
    return ((y-1, x), (y, x+1), (y-1,x), (y,x-1))

def find_4Xneighbours(y, x):
    return ((y-1, x+1), (y+1, x+1), (y+1,x -1), (y-1,x-1))

def find_star(y, x):
    if np.all(find_4neighbours(y,x) == 1) or np.all(find_4Xneighbours(y,x) == 1):
        count_stars += 1
    return count_stars

plt.imshow(image)
plt.show()