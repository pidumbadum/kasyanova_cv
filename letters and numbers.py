import numpy as np
import matplotlib.pyplot as plt
from pyexpat import features
from skimage.measure import label, regionprops
from skimage.io import imread
from pathlib import Path

from money.object_prop import perimeter

save_path = Path(__file__).parent

def count_holes(region):
    shape = region.image.shape
    new_region = np.zeros((shape[0]+2, shape[1]+2))
    new_region[1:-1, 1:-1] = region.image
    new_region = np.logical_not(new_region)
    labeled = label(new_region)
    return np.max(labeled)-1

def count_lines(region):
    shape = region.image.shape
    image = region.image
    vlines = (np.sum(image, 0) / shape[0] == 1).sum()
    hlines = (np.sum(image, 1) / shape[1] == 1).sum()
    return vlines, hlines

def extraxtor(region):
    cy, cx = region.centroid_local
    cy /= region.image.shape[0]
    cx /= region.image.shape[1]
    perimeter = region.perimeter / region.image.size
    holes = count_holes(region)
    vlines, hlines = count_lines(region)
    vlines /= region.image.shape[1]
    hlines /= region.image.shape[0]
    eccentricity = region.eccentricity
    aspect = region.image.shape[0] / region.image.shape[1]
    return np.array([region.area/region.image.size, cx, cy, holes, vlines, hlines, eccentricity, aspect])

def classificator(region, templates):
    features = extraxtor(region)
    result = ""
    min_d = 10 ** 16
    for symbol, t in templates.items():
        d = ((t-features)**2).sum() ** 0.5
        if d < min_d:
            result = symbol
            min_d = d
    return result

template = imread("alphabet-small.png")[:, :, :-1]
print(template.shape)
template = template.sum(2)
binary = template != 765

labeled = label(binary)
props = regionprops(labeled)

templates = {}

for region, symbol in zip(props, ["8", "0", "A", "B", "1", "W", "X", "*", "/", "-"]):

    templates[symbol] = extraxtor(region)

print(templates)

#print(classificator(props[2], templates))

image = imread("alphabet.png")[:, :, :-1]
abinary = image.mean(2)>0
alabeled = label(abinary)
print(np.max(alabeled))

aprops = regionprops(alabeled)
result= {}
image_path = save_path / "out"
image_path.mkdir(parents=True, exist_ok=True)

#plt.ion()
plt.figure(figsize=[5,7])
for region in aprops:
    symbol = classificator(region, templates)
    if symbol not in result:
        result[symbol] = 0
    result[symbol] += 1
    plt.cla()
    plt.title(f"Class {symbol}")
    plt.imshow(region.image, cmap=plt.cm.gray)
    plt.savefig(image_path / f"image{region.label}.png")
print(result)

# print(type(props[0]))
# print(props[0].area, props[0].centroid)
plt.imshow(abinary)
plt.show()
