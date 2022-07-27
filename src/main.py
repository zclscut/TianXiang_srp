import numpy as np
import cv2 as cv
from emotion import emotionFrameDetect as efd

class_labels={0:'Angry',1:'Fear',2:'Happy',3:'Neutral',4:'Sad',5:'Surprise'}
classes=list(class_labels.values())

if __name__ =='__main__':
    camera=cv.VideoCapture(0)#打开摄像头
    while True:
        ret, frame = camera.read()
        frame=efd(frame)
        cv.imshow('all', frame)
        if cv.waitKey(1) == 27 or cv.getWindowProperty("all",cv.WND_PROP_AUTOSIZE) != 1:  # ESC的ASCII码
            break
    camera.release()
    cv.destroyAllWindows()