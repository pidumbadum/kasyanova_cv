import cv2

cv2.namedWindow("Camera", cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("template", cv2.WINDOW_GUI_NORMAL)
cam = cv2.VideoCapture(0+cv2.CAP_DSHOW)#для винды 0+cv2.CAP_DSHOW

roi = None
while cam.isOpened():
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7,7), 0)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord('r'):
        x, y, w, h = cv2.selectROI('roi', gray)
        roi = gray[y:y+h, x:x + w]
        cv2.imshow('template', roi)
        cv2.destroyWindow('roi')
    if roi is not None:
        result = cv2.matchTemplate(gray, roi, cv2.TM_CCORR_NORMED)
        # cv2.imshow("CORR", result)
        (min_val, max_val, min_loc, max_loc) = cv2.minMaxLoc(result)
        top_left = max_loc
        bottom_right =(top_left[0] + roi.shape[1], top_left[1] + roi.shape[0])
        cv2.rectangle(frame, top_left, bottom_right, (0,255,0), 4)
        cv2.putText(frame, f'Diffs = {max_val:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0)) 

    cv2.imshow("Camera", frame)

cam.release()
cv2.destroyAllWindows()