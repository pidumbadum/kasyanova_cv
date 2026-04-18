import cv2
import time
import numpy as np
import matplotlib.pyplot as plt

tv = cv2.imread('./18.04/imjs/news.jpg', cv2.IMREAD_COLOR_BGR) #image with tv
plts2 = np.array([[17, 24], [430, 56], [430, 266], [41, 294]], dtype= 'f4')

#Работа с камерой 
cv2.namedWindow("Camera", cv2.WINDOW_GUI_NORMAL)
cam = cv2.VideoCapture(0)
pref_time = time.perf_counter()
while cam.isOpened():
    reta, frame = cam.read()

    #Work with cameras frame form
    rows, calls, _ = frame.shape
    pts1 = np.array([[0,0], [calls, 0], [calls, rows], [0, rows]], dtype = "f4")
    m = cv2.getPerspectiveTransform(pts1, plts2)
    transformed = cv2.warpPerspective(frame, m, (tv.shape[1], tv.shape[0]))
    gray = cv2.cvtColor(transformed, cv2.COLOR_RGB2GRAY)
    reast, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    bg = cv2.bitwise_and(tv, tv, mask= cv2.bitwise_not(mask))
    fg = cv2.bitwise_and(transformed, transformed, mask= mask)
    result = cv2.add(bg, fg)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    current_t = time.perf_counter()
    print(f'FPS ={ 1/ (current_t - pref_time):.1f}')
    pref_time = current_t

    cv2.imshow("Camera", result)



# cam.release()

# cheb = cv2.imread('./18.04/imjs/cheburashka.jpg', cv2.IMREAD_COLOR_RGB) 
# plt.imshow(result)
# plt.show()