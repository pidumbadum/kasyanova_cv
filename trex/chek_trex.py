import cv2
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

save_path = Path(__file__).parent
trex_path = save_path/'trex.npy'

trex_mask = np.load(trex_path)

plt.imshow(trex_mask)
plt.show()