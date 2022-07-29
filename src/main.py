import numpy as np
import cv2 as cv
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


if __name__ =='__main__':
    camera=cv.VideoCapture(0)#打开摄像头
    while True:

        ret, frame = camera.read()
        #t = time.time()#测试模块执行时间
        emoFlag,photo=emotion_detect(frame,frame)#输入一帧原始图片，输出情绪类别标签emoFlag，并输出情绪识别后用文字标签后的图片frame
        #print(1.0 / (time.time() - t))  # 测试模块执行时间
        #print(emoFlag)
        isFatigue, photo = fatigue_detect(frame, photo)
        isPosture, photo = posture_detect(frame, photo)
        isFocus, photo = concentration_detect(frame, photo)

        #print(camera.get(cv.CAP_PROP_FPS))

        cv.imshow('all', photo)
        if cv.waitKey(1) == 27 or cv.getWindowProperty("all",cv.WND_PROP_AUTOSIZE) != 1:  # ESC的ASCII码
            break
    camera.release()
    cv.destroyAllWindows()