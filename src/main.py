import numpy as np
import cv2
import dlib
import time
from emotion import emotionFrameDetect as emotion_detect
from posture import postureFrameDetectCopy as posture_detect
from concentration import get_euler_angle, get_emotion_score, get_head_pose_score, get_fatigue_score
from fatigue import ear_mar, eye_params, mouth_params, get_fatigue, get_fatigue_grade, add_text
from ConcentrationAnalysis.head_pose_estimation_plus import get_head_pose_estimate_frame  # 获取pitch,yaw

# 表情组人脸识别模型加载
face_detector = cv2.CascadeClassifier('../lib/haarcascade_frontalface_alt.xml ')

# 疲劳度模型加载
detector = dlib.get_frontal_face_detector()  # 人脸识别
predictor = dlib.shape_predictor('../lib/shape_predictor_68_face_landmarks.dat')  # 关键点预测

# 定义常数
# emotion_detect函数输出数字标签，需查字典得到情绪类别
emotion_dic = {0: 'Angry', 1: 'Fear', 2: 'Happy', 3: 'Neutral', 4: 'Sad', 5: 'Surprise', 6: 'Hate'}
emotion_times_dict = {'Angry': 0, 'Hate': 0, 'Fear': 0, 'Happy': 0, 'Sad': 0, 'Surprise': 0, 'Neutral': 0, }
emotion_grade_dict = {1: 'optimistic', 2: 'neutral', 3: 'negative'}

# 身体姿态参数
posture_grade_dict = {1: 'Normal', 2: 'Head_Up', 3: 'Head_Ahead', 4: 'Body_Lean'}

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
fatigue_lst = []  # 存储一个周期疲劳度出现的次数

# 专注度参数
pitch_lst = []  # 存放每帧数据的pitch
yaw_lst = []  # 存放每帧数据的yaw
roll_lst = []
focus_grade = 5  # 初始专注度等级unknown
focus_grade_dict = {1: 'extreme_more_focus', 2: 'more_focus', 3: 'less_focus', 4: 'extreme_less_focus', 5: 'unknown'}
i = 0


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


def get_focus_score(head_pose_score, emotion_score, fatigue_score):
    focus_score = head_pose_score * 0.3 + emotion_score * 0.2 + fatigue_score * 0.4

    if focus_score < 0.45:
        focus_grade = 4
    elif 0.45 <= focus_score < 0.6:
        focus_grade = 2
    elif 0.6 <= focus_score < 0.75:
        focus_grade = 3
    else:
        focus_grade = 4

    return round(focus_score, 2),focus_grade


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)  # 打开摄像头
    while True:
        cv2.ocl.setUseOpenCL(False)  # 避免opencl与tensorflow冲突

        ret, frame = cap.read()
        rect, roi_gray, gray = faceDetectorVideo(frame)  # 输出人脸矩形坐标，压缩人脸灰度图
        frame_start_time = time.time()  # 帧计时开始,测试模块执行时间
        emoFlag, photo = emotion_detect(rect, roi_gray, frame, frame)  # 输入灰度图，输出情绪类别标签emoFlag，并输出情绪识别后用文字标签后的图片frame

        frame_counter += 1
        # --------表情模块模块-----------
        emotion_times_dict[emotion_dic[emoFlag]] = emotion_times_dict[emotion_dic[emoFlag]] + 1

        # --------身体姿态模块-----------
        # isPosture, posture_grade, photo=posture_detect(frame,photo)
        # print(f'posture_grade:{posture_grade}')

        # --------疲劳度模块------------
        rects = detector(gray, 0)  # 这个地方重复,但换成前面的rects会出错
        # 第七步：循环脸部位置信息，使用predictor(gray, rect)获得脸部特征位置的信息
        for rect in rects:
            # 计算ear,mar
            ear, mar = ear_mar(gray, rect)

            # 第十三步：循环，满足条件的，眨眼次数+1
            ear, eye_conti_frames, step_frames, blink_times, eye_close_times, eye_close_frames = eye_params(ear, \
                                                                                                            eye_conti_frames,
                                                                                                            step_frames,
                                                                                                            blink_times,
                                                                                                            eye_close_times,
                                                                                                            eye_close_frames)

            # 眨眼频率
            blink_freq = blink_times / period_frames
            # perclose
            perclose = eye_close_frames / period_frames
            # 同理，判断是否打哈欠
            mar, mouth_conti_frames, step_frames, yawn_times = mouth_params(mar, mouth_conti_frames, step_frames,
                                                                            yawn_times)
            # 打哈欠频率
            yawn_freq = yawn_times / period_frames
            # 疲劳得分
            fatigue = get_fatigue(blink_freq, yawn_freq, perclose, eye_close_times)
            fatigue_lst.append(fatigue)

            # 疲劳等级
            fatigue_grade = get_fatigue_grade(fatigue)

            # 添加文字
            if frame_counter != period_frames:
                add_text(frame, eye_conti_frames, ear, blink_times, blink_freq, mouth_conti_frames, mar, yawn_times,
                         yawn_freq, eye_close_times, perclose, rects, frame_counter, fatigue, fatigue_grade)

            # --------专注度模块-----------
            pitch, yaw, roll, photo = get_euler_angle(photo)
            pitch_lst.append(abs(pitch))
            yaw_lst.append(abs(yaw))
            roll_lst.append(abs(roll))

        if frame_counter == period_frames:  # 一个计数周期结束
            i += 1
            # 头部得分
            head_pose_score = get_head_pose_score(pitch_lst, yaw_lst, roll_lst)
            # 表情得分
            emotion_score = get_emotion_score(emotion_times_dict)
            # 疲劳得分
            fatigue_score = get_fatigue_score(max(fatigue_lst))
            # 专注度得分
            focus_score,focus_grade = get_focus_score(head_pose_score, emotion_score, fatigue_score)

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
            cv2.imwrite('../images/out{}.png'.format(i), photo)

            # 进入下一个周期,参数初始化
            period_frames = 100  # 1000帧为一个周期
            step_frames = 8  # 10帧为一个检测步长
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

            # 表情
            emotion_times_dict = {'Angry': 0, 'Hate': 0, 'Fear': 0, 'Happy': 0,
                                  'Sad': 0, 'Surprise': 0, 'Neutral': 0}

            # 专注度
            pitch_lst = []  # 存放每帧数据的pitch
            yaw_lst = []  # 存放每帧数据的yaw
            roll_lst = []
            focus_grade = 5  # 初始专注度等级unknown

        print('处理一帧所需时间:{:.5f}ms'.format(1000 * (time.time() - frame_start_time)))  # 测试模块执行时间
        cv2.namedWindow('all', cv2.WINDOW_NORMAL)
        cv2.imshow('all', photo)
        if cv2.waitKey(1) == 27:  # ESC的ASCII码
            break
    cap.release()
    cv2.destroyAllWindows()
