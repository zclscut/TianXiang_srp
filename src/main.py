import numpy as np
import cv2 as cv
import dlib
import time
from emotion import emotionFrameDetect as emotion_detect
from posture import postureFrameDetect as posture_detect
from concentration import concentrationFrameDetect as concentration_detect
from concentration import get_overall_emotion_score,get_head_pose_score,get_fatigue_score,get_focus_grade
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

    # 专注度检测初始化
    detect_times = 12 # 设定一个周期处理帧数
    counter=0 # 帧计数(一周期清零一次)
    emotion_times_dict={'Angry':0,'Hate':0,'Fear':0,'Happy':0,'Sad':0,'Surprise':0,'Neutral':0,}
    pitch_lst=[] # 存放每帧数据的pitch
    yaw_lst=[] # 存放每帧数据的yaw
    yaw_times=0 # 打哈欠次数
    blink_times=0 # 眨眼次数
    eye_close_time_lst=[] # 一个周期中闭眼时长列表(从检测到闭眼开始计算时间,到检测到没有闭眼结束)
    mouth_open_time_lst=[] # 一个周期中张嘴时长列表(从检测到打哈欠开始计算时间,到检测到没有打哈欠结束)
    detect_time=0 # 一个检测周期所消耗的总时长
    focus_score = 0 # 初始专注度得分
    focus_grade = None # 初始专注度等级

    while True:

        ret, frame = camera.read()
        rect, roi_gray, gray = faceDetectorVideo(frame)# 输出人脸矩形坐标，压缩人脸灰度图
        frame_start_time = time.time() # 帧计时开始,测试模块执行时间
        emoFlag, photo = emotion_detect(rect,roi_gray,frame,frame)#输入灰度图，输出情绪类别标签emoFlag，并输出情绪识别后用文字标签后的图片frame

        # 需要的参数：yaw_times,blink_times,eye_close_time_lst,mouth_open_time_lst
        isFatigue, photo = fatigue_detect(frame, photo)
        isPosture, photo = posture_detect(frame, photo)

        # --------专注度模块------------
        rect_dlib=[]
        (x,w,y,h)=rect
        rect_dlib.append(dlib.rectangle(x,y,x+w,y+h))
        pitch,yaw,roll, photo = concentration_detect(rect_dlib,gray, photo)

        counter+=1 # 计数+1帧
        emotion_times_dict[emotion_dic[emoFlag]]=emotion_times_dict[emotion_dic[emoFlag]]+1
        pitch_lst.append(pitch)
        yaw_lst.append(yaw)
        detect_time += (time.time() -frame_start_time)

        if counter==detect_times: # 一个周期检测结束
            # 处理数据
            head_pose_score=get_head_pose_score(pitch_lst,yaw_lst)
            overall_emotion_score=get_overall_emotion_score(detect_times,emotion_times_dict)
            fatigue_score=get_fatigue_score(detect_times,eye_close_time_lst,yaw_times,
                                            mouth_open_time_lst,blink_times,detect_time)
            focus_score = 0.07192743 * overall_emotion_score + 0.27895457 * fatigue_score \
                          + 0.649118 * head_pose_score
            focus_grade=get_focus_grade(focus_score)
            print(f'专注度得分为:{round(focus_score,2)}')
            print(f'检测了{counter}帧,消耗了{round(detect_time,2)}s,平均每帧消耗{round(1000*detect_time/counter,2)}ms')

            # 变量清零
            counter = 0  # 帧计数(一周期清零一次)
            emotion_times_dict = {'Angry': 0, 'Hate': 0, 'Fear': 0, 'Happy': 0, 'Sad': 0, 'Surprise': 0, 'Neutral': 0, }
            pitch_lst = []  # 存放每帧数据的pitch
            yaw_lst = []  # 存放每帧数据的yaw
            yaw_times = 0  # 打哈欠次数
            blink_times = 0  # 眨眼次数
            eye_close_time_lst = []  # 一个周期中闭眼时长列表(从检测到闭眼开始计算时间,到检测到没有闭眼结束)
            mouth_open_time_lst = []  # 一个周期中张嘴时长列表(从检测到打哈欠开始计算时间,到检测到没有打哈欠结束)
            detect_time = 0  # 一个检测周期所消耗的总时长


        cv.putText(photo, f'focus_score:{round(focus_score, 2)}', (20, 190), fontFace=cv.FONT_HERSHEY_SIMPLEX,
                   fontScale=0.8, color=(0, 0, 255), thickness=2)
        cv.putText(photo, f'focus_grade:{str(focus_grade)}', (20, 220), fontFace=cv.FONT_HERSHEY_SIMPLEX,
                   fontScale=0.8, color=(0, 0, 255), thickness=2)
        #print(camera.get(cv.CAP_PROP_FPS))
        print('处理一帧所需时间:{:.5f}ms'.format(1000*(time.time() -frame_start_time)))#测试模块执行时间
        cv.imshow('all', photo)
        if cv.waitKey(1) == 27 or cv.getWindowProperty("all",cv.WND_PROP_AUTOSIZE) != 1:  # ESC的ASCII码
            break
    camera.release()
    cv.destroyAllWindows()