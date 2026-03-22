import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from skimage.morphology import (opening, dilation, closing, erosion)

image = np.load("./wires6.npy")
processed = np.zeros_like(image)

labeled = label(image)
print(f"{labeled.max()} wires was found")

for n in range(1, labeled.max() + 1):
    #проблема: провода бывают разной ширины, поэтому не всем подходит одинаковая маска. итог: маску считать надо отдельно.
    #Решение:
    wire = (labeled == n)
    widths = np.unique(np.sum(wire, axis=0))
    wire_width = np.max(widths)
    struct = np.ones((wire_width, 1), dtype = "int")
    #Деление на куски:
    wires_cutted = opening((labeled == n), footprint=struct)
    processed += wires_cutted #<-- Добавление на график
    labeled_cutted_wires = label(wires_cutted)
    print(f"Wire = {n}, parts = {labeled_cutted_wires.max()}")

plt.subplot(121)
plt.imshow(image)
plt.subplot(122)
plt.imshow(processed)
plt.show()