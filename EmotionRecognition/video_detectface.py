import numpy as np
import cv2 as cv
#import time
#from tensorflow.keras import Sequential
#from tensorflow.keras.models import load_model
#from tensorflow.keras.preprocessing.image import img_to_array


#在框外用文字输出情绪
def text_on_detected_boxes(text,text_x,text_y,image,font_scale = 1,
                           font = cv.FONT_HERSHEY_SIMPLEX,
                           FONT_COLOR = (0, 0, 0),
                           FONT_THICKNESS = 2,
                           rectangle_bgr = (0, 255, 0)):
    # get the width and height of the text box
    (text_width, text_height) = cv.getTextSize(text, font, fontScale=font_scale, thickness=2)[0]
    # Set the Coordinates of the boxes
    box_coords = ((text_x-10, text_y+4), (text_x + text_width+10, text_y - text_height-5))
    # Draw the detected boxes and labels
    cv.rectangle(image, box_coords[0], box_coords[1], rectangle_bgr, cv.FILLED)
    cv.putText(image, text, (text_x, text_y), font, fontScale=font_scale, color=FONT_COLOR,thickness=FONT_THICKNESS)

def face_detector_image(frame):
    allfaces=[]
    rects=[]
    gray=cv.cvtColor(frame,code=cv.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10)
    #没检测到人脸
    if faces is ():
        return (0,0,0,0),np.zeros((48,48),np.uint8),frame
    #检测到人脸，用(0,0,255)红色方框框出来
    for x, y, w, h in faces:
        cv.rectangle(frame, pt1=(x, y),
                     pt2=(x + w, y + h),
                     color=[0, 0, 255],
                     thickness=2)


if __name__ =='__main__':
    cv.namedWindow('face',cv.WINDOW_NORMAL)
    cv.resizeWindow('face',800,600)
    cap=cv.VideoCapture(0)
    face_detector=cv.CascadeClassifier('haarcascade_frontalface_alt.xml ')
    while True:
        flag,frame=cap.read()
        if not flag:
            break
        cv.imshow('face',frame)
        key=cv.waitKey(1000//24)
        if key==27:#ESC的ASCII码
            break
        cv.destroyAllWindows()
    cap.release()