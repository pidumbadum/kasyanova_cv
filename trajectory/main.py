import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import re

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

fig = plt.figure()

for file in files:
    img = np.load(file)

    plt.clf() #очисточка

    plt.imshow(img)
    plt.axis('off')
    plt.title(f'Показ: {file}')

    plt.pause(0.05)

plt.show()
