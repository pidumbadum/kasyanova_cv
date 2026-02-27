import numpy as np
import matplotlib.pyplot as plt
#комментарии себе на будущее

def lerp(v0, v1, t): #вот эта функция считает изменение цвета. хитро, я бы не додумалась
    return (1 - t) * v0 + t * v1 #суть: возвращается среднее значение двух цветов.
    # чтобы сделать градиент от одного цвета к другому с определенным значеинем,
    # надо постепенно привети цифровое значение этого цвета к другому
    #тут находится сколько осталось от обоих цветов и складывается. в начале один цвет будет чистым, в середине будет среднее, а в конце чистый второй цвет.



size = 100
image = np.zeros((size, size, 3), dtype="uint8") #просто нулевой массив, который будем красить. любопытно, что это трехмерных массив. это нужно, чтобы смешать все цвета по rgb
assert image.shape[0] == image.shape[1]

color1 = [255, 0, 128]
color2 = [128, 0, 255]


for i, v0 in enumerate(np.linspace(0, 1, image.shape[0]) ): #enumerate - возвращает массив элементов и их индексов
    for j, v1 in enumerate(np.linspace(0, 1, image.shape[1])): # np.linspace - продвинутый range
        v = (v0 + v1) / 2
        r = lerp(color1[0], color2[0], v)
        g = lerp(color1[1], color2[1], v)
        b = lerp(color1[2], color2[2], v)
        image[i, j, :] = [r, g, b] #срезу присваеваются значения цвета rgb

plt.figure()
plt.imshow(image)
plt.show()