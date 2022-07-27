import numpy as np
import cv2 as cv

if __name__ =='__main__':
    camera=cv.VideoCapture(0)#打开摄像头
    while True:
        ret, frame = camera.read()

        cv.imshow('all', frame)
        if cv.waitKey(1) == 27 or cv.getWindowProperty("all",cv.WND_PROP_AUTOSIZE) != 1:  # ESC的ASCII码
            break
    camera.release()
    cv.destroyAllWindows()