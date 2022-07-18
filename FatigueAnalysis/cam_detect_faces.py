import numpy as np
import cv2 as cv




if __name__ =='__main__':
    cv.namedWindow('face',cv.WINDOW_NORMAL)
    cv.resizeWindow('face',800,500)

    cap=cv.VideoCapture(0)
    face_detector=cv.CascadeClassifier('haarcascade_frontalface_alt.xml ')
    while True:
        flag,frame=cap.read()
        if not flag:
            break
        gray = cv.cvtColor(frame, code=cv.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10)
        # 检测到人脸，用(0,0,255)红色方框框出来
        for x, y, w, h in faces:
            cv.rectangle(frame, pt1=(x, y),
                pt2=(x + w, y + h),
                color=[0, 0, 255],
                thickness=2)
        cv.imshow('face',frame)
        key=cv.waitKey(1000//24)
        if key==27:#ESC的ASCII码
            break
    cv.destroyAllWindows()
    cap.release()