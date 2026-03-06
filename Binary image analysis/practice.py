import numpy as np
import matplotlib.pyplot as plt
import sys



msk_out_c = np.array([[0, 0],
                            [0, 1]], 'uint8')
masks_external = np.array([
    msk_out_c,
    np.fliplr(msk_out_c),
    np.flipud(msk_out_c),
    np.flipud(np.fliplr(msk_out_c))
])
masks_2X = np.array([[[1, 0],
                             [0, 1]],

                            [[0, 1],
                            [1, 0]]], 'uint8')
masks_internal = np.array([np.where(mask == 0, 1, 0) for mask in masks_external])

data = np.load('../numpy_images/ex6.npy')

# здесь проверяется, является ли изображение бинарным или нет
unique = np.unique(data).tolist()
if unique not in [[0,1],[0],[1]] or data.ndim != 2:
    sys.exit ("Not binary")


external = 0
internal = 0

for lines in range(np.shape(data)[0] - 1):
    for pix in range(np.shape(data)[1] - 1):
        area = data[lines:lines+2, pix:pix+2]
        if any(np.array_equal(area, mask) for mask in masks_external):
            external += 1
        if any(np.array_equal(area, mask) for mask in masks_internal):
            internal += 1
        if any(np.array_equal(area, mask) for mask in masks_2X):
            external += 2


print((external - internal)/4)

plt.figure()
plt.imshow(data)
plt.show()
