import numpy as np
import cv2 as cv
import dlib
import time
from emotion import emotionFrameDetect as emotion_detect
from posture import postureFrameDetect as posture_detect
from concentration import concentrationFrameDetect as concentration_detect
from fatigue import fatigueFrameDetect as fatigue_detect

# 定义常数
# 初始化帧计数器和眨眼总数
eyeCounter = 0
eyeTotal = 0
# 初始化帧计数器和打哈欠总数
mouthCounter = 0
mouthTotal = 0
# 初始化帧计数器和点头总数
headCounter = 0
headTotal = 0
#情绪标签0~5
emoFlag=0
#emotion_detect函数输出数字标签，需查字典得到情绪类别
emotion_dic={0:'Angry',1:'Fear',2:'Happy',3:'Neutral',4:'Sad',5:'Surprise'}
#头部姿势标签
headPosture=0
posture_dic={0:'focus',1:'up',2:'down',3:'right',4:'left'}
#是否疲劳
isFatigue=0
#是否专注
isFocus=0
#学习姿势是否正确
isPosture=0

face_detector = cv.CascadeClassifier('../lib/haarcascade_frontalface_alt.xml ')


def faceDetectorVideo(img):
    # Convert image to grayscale
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    #t = time.time()#测试执行时间
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10)
    #caleFactor=1.1, minNeighbors=10执行时间110ms
    #caleFactor=1.3, minNeighbors=10执行时间40ms
    #print(time.time() - t)#测试执行时间
    # 没检测到人脸
    if faces == ():
        return (0, 0, 0, 0), np.zeros((48, 48), np.uint8), img
    # 检测到人脸，用(0,0,255)红色方框框出来
    for (x, y, w, h) in faces:
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)
        roi_gray = gray[y:y + h, x:x + w]#截取人脸，压缩后作为神经网络的输入，神经网络输出情绪标签

    roi_gray = cv.resize(roi_gray, (48, 48), interpolation=cv.INTER_AREA)

    return (x, w, y, h), roi_gray, gray
    # 返回人脸矩形参数，压缩人脸灰度图

if __name__ =='__main__':
    camera=cv.VideoCapture(0)#打开摄像头
    while True:

        ret, frame = camera.read()
        rect, roi_gray, gray = faceDetectorVideo(frame)# 输出人脸矩形坐标，压缩人脸灰度图
        t = time.time()#测试模块执行时间
        emoFlag, photo = emotion_detect(rect,roi_gray,frame,frame)#输入灰度图，输出情绪类别标签emoFlag，并输出情绪识别后用文字标签后的图片frame

        #print(emoFlag)
        rect_dlib=[]
        (x,w,y,h)=rect
        rect_dlib.append(dlib.rectangle(x,y,x+w,y+h))
        isFocus, photo = concentration_detect(rect_dlib,gray, photo)


        isFatigue, photo = fatigue_detect(frame, photo)
        isPosture, photo = posture_detect(frame, photo)


        #print(camera.get(cv.CAP_PROP_FPS))
        print('处理一帧所需时间:{:.5f}ms'.format(1000*(time.time() - t)))#测试模块执行时间
        cv.imshow('all', photo)
        if cv.waitKey(1) == 27 or cv.getWindowProperty("all",cv.WND_PROP_AUTOSIZE) != 1:  # ESC的ASCII码
            break
    camera.release()
    cv.destroyAllWindows()