import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from skimage.morphology import (opening, dilation, closing, erosion)

image = np.load("./stars.npy")
mask =np.ones((3, 2))

clened_image = opening(image, mask)
image_only_star = np.logical_xor(image, clened_image)

print(f"Count of stars = {label(image_only_star).max()}")

plt.subplot(121)
plt.imshow(image)
plt.subplot(122)
plt.imshow(image_only_star)
plt.show()