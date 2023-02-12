import cv2
import dlib
import time
import datetime
import numpy as np
from scipy import stats
from emotion import emotionFrameDetect as emotion_detect
from posture import postureFrameDetectCopy as posture_detect
from concentration import get_euler_angle, get_emotion_score, get_head_pose_score, get_fatigue_score,get_focus_score
from fatigue import ear_mar, eye_params, mouth_params, get_fatigue, get_fatigue_grade, add_text
from database import doSql,original_event_counter,study_state_counter,original_event_insert_all,study_state_insert_all # 数据库操作类的库

# 表情组人脸识别模型加载
face_detector = cv2.CascadeClassifier('../lib/haarcascade_frontalface_alt.xml ')

# 疲劳度模型加载
detector = dlib.get_frontal_face_detector()  # 人脸识别
predictor = dlib.shape_predictor('../lib/shape_predictor_68_face_landmarks.dat')  # 关键点预测

# 定义常数
# emotion_detect函数输出数字标签，需查字典得到情绪类别
'''没有检测到人脸,专注度检测当做厌恶情绪,情绪等级划分？'''
emotion_dic = {0: 'Angry', 1: 'Fear', 2: 'Happy', 3: 'Neutral', 4: 'Sad', 5: 'Surprise', 6: 'Hate'}

#在一个多帧检测循环中，统计各种情绪的频次
emotion_times_dict = {'Angry': 0, 'Hate': 0, 'Fear': 0, 'Happy': 0, 'Sad': 0, 'Surprise': 0, 'Neutral': 0, }


# 身体姿态参数
posture_grade_dict = {1: 'Normal', 2: 'Head_Up', 3: 'Head_Ahead', 4: 'Body_Lean'}
posture_grade_lst=[] # 存储一个周期疲劳等级

# 疲劳度的参数初始化
period_frames = 100  # 1000帧为一个周期
step_frames = 8  # 10帧为一个检测步长
frame_counter = 0  # 帧计数器
# 初始化帧计数器和眨眼总数、闭眼总次数、perclose
eye_conti_frames = 0  # 眼睛长宽比小于阈值的连续帧数
blink_times = 0  # 周期内眨眼总次数
eye_close_times = 0  # 闭眼总次数
perclose = 0
# 初始化帧计数器和打哈欠总数
mouth_conti_frames = 0  # 嘴巴纵横比大于阈值的连续帧数
yawn_times = 0  # 周期内打哈欠总数
# 初始化闭眼时长、眨眼频率、和打哈欠频率
eye_close_frames = 0  # 周期内连续闭眼总帧数
blink_freq = 0  # 眨眼频率
yawn_freq = 0  # 打哈欠频率
fatigue = 0  # 初始化疲劳评分
fatigue_grade = 1  # 疲劳等级初始化默认1级别
fatigue_grade_dict = {1: "Clear", 2: "Critical state", 3: 'Mild fatigue', 4: 'Moderate fatigue', 5: 'Severe fatigue'}
fatigue_grade_lst=[] # 存储一个周期疲劳等级
fatigue_lst = []  # 存储一个周期疲劳度

# 专注度参数
pitch_lst = []  # 存放每帧数据的pitch绝对值
yaw_lst = []  # 存放每帧数据的yaw绝对值
roll_lst = [] # 存放每帧数据的yaw绝对值
focus_grade_dict = {1: 'extreme_more_focus', 2: 'more_focus', 3: 'less_focus', 4: 'extreme_less_focus'}
i = 0 # 运行周期计数
t_1s=0 # 一秒定时


def faceDetectorVideo(img):
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # t = time.time()#测试执行时间
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10)
    # caleFactor=1.1, minNeighbors=10执行时间110ms
    # caleFactor=1.3, minNeighbors=10执行时间40ms
    # print(time.time() - t)#测试执行时间
    # 没检测到人脸
    if faces == ():
        return (0, 0, 0, 0), np.zeros((48, 48), np.uint8), img
    # 检测到人脸，用(0,0,255)红色方框框出来
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)
        roi_gray = gray[y:y + h, x:x + w]  # 截取人脸，压缩后作为神经网络的输入，神经网络输出情绪标签

    roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

    return (x, w, y, h), roi_gray, gray
    # 返回人脸矩形参数，压缩人脸灰度图




''''
is为前缀的参数取值0或1,1代表超过对应参数阈值,为原始数据记录的参数
在运行时,为减少每帧的处理时间,默认不写入原始数据(写入原始数据:可将original_event_insert()函数对应的部分取消注释即可),只写入周期数据
原始数据和周期数据记录：只记录参数变化后的值,未变化不记录
周期运行结束，在images中会生成对应的周期处理图像及对应的专注度相关参数,若需要添加其他参数,在对应位置添加即可
'''

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)  # 打开摄像头
    while True:
        frame_start=time.time() # 1帧计时开始
        cv2.ocl.setUseOpenCL(False)  # 避免opencl与tensorflow冲突

        ret, frame = cap.read()
        rect, roi_gray, gray = faceDetectorVideo(frame)  # 输出人脸矩形坐标，压缩人脸灰度图
        emoFlag, photo = emotion_detect(rect, roi_gray, frame)  # 输入灰度图，输出情绪类别标签emoFlag，并输出情绪识别后用文字标签后的图片frame
        ''' emoFlag没有检测到人脸时候返回0'''
        # print(f'emoFlag:{emoFlag}')

        frame_counter += 1
        # --------表情模块模块-----------
        #emotion_dic[emoFlag]为识别的情绪名称，
        # emotion_times_dict[emotion_dic[emoFlag]]为对应的名称的识别频次
        emotion_times_dict[emotion_dic[emoFlag]] += 1

        # --------身体姿态模块-----------
        # posture_grade分为1-4等级,is为前缀的疲劳组参数取值为0或1
        is_z_gap,is_y_gap_sh,is_y_head_gap,is_per,isPosture,posture_grade,photo=posture_detect(frame,photo)
        posture_grade_lst.append(posture_grade)

        # --------疲劳度模块------------
        rects = detector(gray, 0)  # 这个地方重复,但换成前面的rects会出错
        # 未检测到人脸,pitch/yaw/roll默认超过阈值;默认没有眨眼/打哈欠/闭眼
        # is为前缀的参数取值为0或1
        is_pitch=1
        is_yaw=1
        is_roll=1
        is_blink=0
        is_yawn=0
        is_close=0
        for rect in rects:
            # 计算ear,mar
            ear, mar = ear_mar(gray, rect)

            # 循环，满足条件的，眨眼次数+1
            ear, eye_conti_frames, step_frames, blink_times, eye_close_times, eye_close_frames,is_blink,is_close = \
                eye_params(ear, eye_conti_frames,step_frames,blink_times,eye_close_times, eye_close_frames)

            # 眨眼频率
            blink_freq = blink_times / period_frames
            # perclose
            perclose = eye_close_frames / period_frames
            # 同理，判断是否打哈欠
            mar, mouth_conti_frames, step_frames, yawn_times,is_yawn = mouth_params(mar, mouth_conti_frames, step_frames,
                                                                            yawn_times)
            # 打哈欠频率
            yawn_freq = yawn_times / period_frames
            # 疲劳得分,fatigue为疲劳组所计算的疲劳度,取值为正数
            fatigue = get_fatigue(blink_freq, yawn_freq, perclose, eye_close_times)
            fatigue_lst.append(fatigue)

            # 疲劳等级
            fatigue_grade = get_fatigue_grade(fatigue)
            fatigue_grade_lst.append(fatigue_grade)

            # 实时显示帧添加文字
            if frame_counter != period_frames:
                add_text(frame, eye_conti_frames, ear, blink_times, blink_freq, mouth_conti_frames, mar, yawn_times,
                         yawn_freq, eye_close_times, perclose, rects, frame_counter, fatigue, fatigue_grade)

            # --------专注度模块-----------
            # pitch,yaw,roll为角度,is为前缀的参数取值为0或1
            pitch, yaw, roll, is_pitch, is_yaw, is_roll, photo = get_euler_angle(photo)
            pitch_lst.append(abs(pitch))
            yaw_lst.append(abs(yaw))
            roll_lst.append(abs(roll))

        delt_time = 1000 * (time.time() - frame_start) # 以毫秒为单位
        print(f'一帧处理需要:{delt_time}ms')
        t_1s += delt_time
        # 1s计时结束,数据库写入一次原始数据
        if t_1s >= 1000:
            # --------1s写一次原始数据---------
            # now 是待插入数据库的record_time字段
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            t_1s=0
            student_id=1
            emotion_sort=emoFlag

            # 插入原始数据
            # original_event_insert_all(student_id, emotion_sort, is_pitch, is_yaw, is_roll, is_z_gap, is_y_gap_sh,
            #                       is_y_head_gap, is_per, is_blink,is_yawn,is_close)

        if frame_counter == period_frames:  # 一个计数周期结束
            i += 1

            # 头部得分,head_pose_score取值分为0.2、0.4、0.7和0.9,依次对应0~10,10~15,15~20和20以上的头部角度周期最大平均值
            head_pose_score,pitch_ave,yaw_ave,roll_ave = get_head_pose_score(pitch_lst, yaw_lst, roll_lst)

            # 疲劳得分,fatigue_score在0~1之间,fatigue_grade分为1-5等级
            if fatigue_lst:
                fatigue_score = get_fatigue_score(fatigue_lst[-1])  # 最后一次的fatigue代表一个周期的疲劳度
                fatigue_grade=fatigue_grade_lst[-1]
            else:
                if pitch_ave<15: # 低头/抬头检测不到人脸的临界角
                    fatigue=1 # 严重疲劳状态
                    fatigue_grade=5
                else:
                    fatigue=0.5 # 人已经不在镜头视线范围,默认中度疲劳
                    fatigue_grade=4
                fatigue_score=1-fatigue # 疲劳分数正向化

            # 表情得分,emotion_score取值为0~1之间,emotion_sort分为积极(optimistic)、中性(neutral)和消极(negative)
            emotion_score,emotion_sort = get_emotion_score(emotion_times_dict)
            emotion_sort_dict = {'optimistic': 1, 'neutral': 2, 'negative': 3}
            emotion_grade=emotion_sort_dict[emotion_sort] # 情绪等级,emotion_grade分为1-3等级

            # 专注度得分,focus_score在0~1之间,focus_grade分为1-4等级
            focus_score,focus_grade = get_focus_score(head_pose_score, emotion_score, fatigue_score)

            # --------周期数据写入数据库study_state------------
            # values中参数依次为student_id,state_key,state_value,record_time

            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            student_id=1  # 暂默认为1

            # 每个周期插入数据
            study_state_insert_all(student_id,emotion_grade,fatigue_grade,posture_grade,focus_grade)

            print(f'pitch_ave:{pitch_ave},yaw_ave:{yaw_ave},roll_ave:{roll_ave}')
            print(f'head_pose_score:{head_pose_score}')
            print(f'emotion_score:{emotion_score}')
            print(f'fatigue_score:{fatigue_score}')
            print(f'focus_score:{focus_score}')
            print(f'focus_grade:{focus_grade}')

            cv2.putText(photo, f'head_pose_score:{head_pose_score}', (20, 200), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1, color=(0, 0, 255), thickness=3)
            cv2.putText(photo, f'emotion_score:{emotion_score}', (20, 240), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1, color=(0, 0, 255), thickness=3)
            cv2.putText(photo, f'fatigue_score:{fatigue_score}', (20, 280), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1, color=(0, 0, 255), thickness=3)
            cv2.putText(photo, f'focus_score:{focus_score}', (20, 320),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1, color=(0, 0, 255), thickness=3)
            cv2.putText(photo, f'focus_grade:{focus_grade}', (20, 360),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1, color=(0, 0, 255), thickness=3)
            cv2.imwrite('../images/out{}.png'.format(i), photo) # 每周期写入一次数据,便于测试


            ######################################################################################################
            # 进入下一个周期,参数初始化
            period_frames = 100  # 100帧为一个周期
            step_frames = 8  # 8帧为一个检测步长
            frame_counter = 0  # 帧计数器
            # 初始化疲劳评分
            fatigue = 0
            fatigue_grade = 1
            # 初始化帧计数器和眨眼总数、闭眼总次数、perclose
            eye_conti_frames = 0  # 眼睛长宽比小于阈值的连续帧数
            blink_times = 0  # 周期内眨眼总次数
            eye_close_times = 0  # 闭眼总次数
            perclose = 0
            # 初始化帧计数器和打哈欠总数
            mouth_conti_frames = 0  # 嘴巴纵横比大于阈值的连续帧数
            yawn_times = 0  # 周期内打哈欠总数
            # 初始化闭眼时长、眨眼频率、和打哈欠频率
            eye_close_frames = 0  # 周期内连续闭眼总帧数
            blink_freq = 0  # 眨眼频率
            yawn_freq = 0  # 打哈欠频率
            fatigue_lst = []
            fatigue_grade_lst=[]

            # 身体姿态
            posture_grade_lst=[]
            # 表情
            emotion_times_dict = {'Angry': 0, 'Hate': 0, 'Fear': 0, 'Happy': 0,
                                  'Sad': 0, 'Surprise': 0, 'Neutral': 0}

            # 专注度
            pitch_lst = []  # 存放每帧数据的pitch
            yaw_lst = []  # 存放每帧数据的yaw
            roll_lst = []
            focus_grade = 5  # 初始专注度等级unknown


        cv2.namedWindow('all_window', cv2.WINDOW_NORMAL)


        cv2.imshow('all', photo)
        if cv2.waitKey(1) == 27 or cv2.getWindowProperty("all_window",cv2.WND_PROP_AUTOSIZE) != 1:  # ESC的ASCII码，或按交叉退出
            break
    cap.release()
    cv2.destroyAllWindows()
