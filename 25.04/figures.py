import cv2
import numpy as np

cv2.namedWindow('image', cv2.WINDOW_FREERATIO)
image = cv2.imread("./25.04/contours/cubes_4.png")

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

cv2.namedWindow('image', cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow('mask', cv2.WINDOW_GUI_NORMAL)

pos =[0, 0]
click = False

def classify(contour):
    verts = -1
    soldidity = -1 #заполненность 
    approx = []
    figure = None
    perimeter = cv2.arcLength(contour, True)
    if perimeter == 0:
        return verts, soldidity, approx, figure
    eps = 0.1 * perimeter
    approx = cv2.approxPolyDP(contour, eps, True)
    verts = len(approx)
    _, radius = (cv2.minEnclosingCircle(contour))
    area = cv2.contourArea(contour)
    circle_area = np.pi * radius ** 2
    soldidity = area / circle_area

    if soldidity >= 0.8: 
        figure = "Sphere"
    elif verts == 3:
        figure = "Treangle"
    elif verts == 4:
        figure = "cube"   
    return verts, soldidity, approx, figure

def on_click(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'Clicked at {x}, {y}')
        global pos
        global click
        pos = [x,y]
        click = True


mask = np.zeros(image.shape[:-1], dtype = 'u1')
cv2.setMouseCallback('image', on_click)
while True:
    display_image = image.copy()

    key = cv2.waitKey(50) & 0xFF
    if key == ord('q'):
        break
    if key == ord('c'):
        mask[:] = 0
    if click:
        click = False
        color = hsv[pos[1], pos[0]]
        lower = np.clip(color * 0.9, 0, 255).astype('uint8')
        upper = np.clip(color * 1.1, 0, 255).astype('uint8')
        print(lower, upper)
        inr = cv2.inRange(hsv, lower, upper)
        inr = cv2.morphologyEx(inr, cv2.MORPH_CLOSE, np.ones((5,5), dtype='uint8'))

        mask = cv2.bitwise_or(mask, inr)
        cv2.imshow('mask', mask)
        print(color)

    counturs, _ = cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if (len(counturs) > 0):
        counturs = list(filter(lambda c: cv2.contourArea(c) > 2000, counturs)) #вроде штука чет хз
        for contour in counturs:
            (verts, solidity, approx, figure) = classify(contour)
            top_idx = np.argmin(contour[:, 0, 1])
            top_point = tuple(contour[top_idx, 0])
            thickness = 2
            font_scale = 1.5
            font = cv2.FONT_HERSHEY_SIMPLEX
            text = f'{figure}({verts}, {solidity:.1f})'
            (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
            text_x= max(10, top_point[0] - text_w//2)
            text_y= max(text_h + 10, top_point[1] - 15)
            cv2.rectangle(display_image, (text_x, text_y -  text_h - 4), (text_x + text_w, text_y + 4), (0, 0, 0), -1)
            cv2.putText(display_image, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
            if len(approx)> 0:
                for p in approx:
                    cv2.circle(display_image, p[0], 10, (255, 0, 255), -1)

    cv2.drawContours(display_image, counturs, -1, (0, 255, 0), 4)
    cv2.imshow('image', display_image)

cv2.destroyAllWindows()