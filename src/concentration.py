'''
一次检测就是一帧
detect_times为检测一轮的总次数(帧数):可在主程序中设定
detect_cost_time为检测一轮消耗总时长
'''
import time
import cv2
import numpy as np
from ConcentrationAnalysis.head_pose_functions import estimate_head_pose

# 模型初始化
# t0=time.time()
from lib.head_pose_model.FaceDetection.FaceBoxes_ONNX import FaceBoxes_ONNX  # 人脸检测
from lib.head_pose_model.FaceAlignment3D.TDDFA_ONNX import TDDFA_ONNX  # 人脸的3D标志点检测

face_boxes = FaceBoxes_ONNX()
tddfa = TDDFA_ONNX()


# t1=time.time()
# print(f'模型初始化时间:{round((t1-t0)*1000,2)}ms')


def draw_pose(img, directions_lst, bound_box_lst, landmarks_lst, show_bbox=False, show_landmarks=False):
    if show_bbox:
        for bound_box in bound_box_lst:
            x_min, y_min, x_max, y_max = bound_box[:4]
            x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)
            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 1)

    if show_landmarks:
        for landmarks in landmarks_lst:
            for point in landmarks[:, :2]:
                cv2.circle(img, tuple(np.abs(point).astype(int)), 1, (0, 255, 0), -1)

    for bound_box, directions in zip(bound_box_lst, directions_lst):
        tdx, tdy = (bound_box[:2] + bound_box[2:4]) / 2
        size = bound_box[2] - bound_box[0]
        # X-Axis drawn in red
        x1 = size * directions[0][0] + tdx
        y1 = -size * directions[0][1] + tdy

        # Y-Axis drawn in green
        x2 = -size * directions[1][0] + tdx
        y2 = size * directions[1][1] + tdy

        # Z-Axis drawn in blue
        x3 = size * directions[2][0] + tdx
        y3 = -size * directions[2][1] + tdy

        cv2.line(img, (int(tdx), int(tdy)), (int(x1), int(y1)), (0, 0, 255), 2)
        cv2.line(img, (int(tdx), int(tdy)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.line(img, (int(tdx), int(tdy)), (int(x3), int(y3)), (255, 0, 0), 2)

    return img


def get_euler_angle(frame):
    # 没有检测到人脸时,默认pitch,yaw,yaw参数均大于阈值
    is_pitch = 1
    is_yaw = 1
    is_roll = 1
    try:
        t0 = time.time()
        bboxes = face_boxes(frame)  # 每一帧中脸部数据构成的ndarry
        # print(f'检测到{len(bboxes)}张脸 ')

        # 计算欧拉角
        param_lst, roi_box_lst = tddfa(frame, np.array([bboxes[-1]]))  # 只计算左边第一张脸
        landmarks_lst = tddfa.recon_vers(param_lst, roi_box_lst)  # landmarks_lst为所有人脸的68点3D坐标
        euler_angle_lst, directions_lst, landmarks_lst = estimate_head_pose(landmarks_lst, True)

        t1 = time.time()

        roll, yaw, pitch = euler_angle_lst[-1]  # 选取左边第一张脸
        is_pitch = 0
        is_yaw = 0
        is_roll = 0
        if abs(pitch)>20:
            is_pitch=1
        if abs(yaw)>20:
            is_yaw=1
        if abs(roll)>20:
            is_roll=1
        # print(f'roll: {roll}, yaw: {yaw}, pitch: {round(pitch)} cost time: {round((t1 - t0) * 1000, 2)}ms')
        # cv2.putText(frame, f'pitch: {round(pitch, 2)}', (80, 100), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        #             fontScale=0.8, color=(0, 0, 255), thickness=2)
        # cv2.putText(frame, f'yaw: {round(yaw, 2)}', (80, 130), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        #             fontScale=0.8, color=(0, 0, 255), thickness=2)
        # cv2.putText(frame, f'roll: {round(roll, 2)}', (80, 160), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        #             fontScale=0.8, color=(0, 0, 255), thickness=2)
        # 添加轴
        modified_frame = draw_pose(
            frame,
            directions_lst,
            np.array([bboxes[-1]]),
            landmarks_lst, )

    except:  # 未检测到人脸时候返回原始图片
        pitch, yaw, roll = 100, 100, 100
        is_pitch,is_yaw,is_roll=1,1,1
        return pitch, yaw, roll, is_pitch, is_yaw, is_roll, frame
    else:
        return pitch, yaw, roll, is_pitch, is_yaw, is_roll, modified_frame

#输入各种情绪频次检测表
def get_emotion_score(emotion_times_dict):
    down_dict = sorted(emotion_times_dict.items(), key=lambda x: x[1], reverse=True)  # 在多帧检测中，根据各种情绪检测频次降序
    print(f'emotion_times_lst:{down_dict}')
    emotion_sort_dict = {'optimistic': 0, 'neutral': 0, 'negative': 0}#三类情绪的频次统计表
    for key, value in emotion_times_dict.items():  # 转换为三类情绪
        if key == 'Happy':
            emotion_sort_dict['optimistic'] = value
        elif key == 'Surprise' or key == 'Neutral':
            emotion_sort_dict['neutral'] = emotion_sort_dict['neutral'] + value
        else:
            emotion_sort_dict['negative'] = emotion_sort_dict['negative'] + value
    times_lst = [value for key, value in emotion_sort_dict.items()]#列表的样子示例：[503,401,96]

    # 以一个周期内出现情绪次数类别最多组划分情绪类别
    down_emotion_sort_lst = sorted(emotion_sort_dict.items(), key=lambda x: x[1], reverse=True)
    emotion_sort = down_emotion_sort_lst[0][0]#消极，积极，中性三种情绪之中，频次最高的情绪名称
    try:
        for key, value in emotion_sort_dict.items():  # 归一化
            # emotion_sort_dict{'optimistic': 503, 'neutral': 401, 'negative': 96}
            # 转化为{'optimistic': 0.503, 'neutral': 0.401, 'negative': 0.096}
            emotion_sort_dict[key] = value / sum(times_lst)
    except:
        emotion_score = 0  # 一个周期内均没检测到人脸
        emotion_sort = 'negative'  # 情绪划分视为消极？
    else:
        emotion_score = emotion_sort_dict['optimistic'] * 0.5 + emotion_sort_dict['neutral'] * 0.3 + \
                        emotion_sort_dict['negative'] * 0.2
    return round(emotion_score / 0.5, 2), emotion_sort


def get_head_pose_score(pitch_lst, yaw_lst, roll_lst):
    # 头部姿态角取三者最大值
    head_pose_score = 0
    try:
        pitch_ave = sum(pitch_lst) / len(pitch_lst)
        yaw_ave = sum(yaw_lst) / len(yaw_lst)
        roll_ave = sum(roll_lst) / len(roll_lst)

        if max(pitch_ave,yaw_ave,roll_ave)<=10:
            head_pose_score = 0.9
        if 10<max(pitch_ave,yaw_ave,roll_ave)<=15:
            head_pose_score = 0.7
        if 15<max(pitch_ave,yaw_ave,roll_ave)<=20:
            head_pose_score = 0.4
        if max(pitch_ave,yaw_ave,roll_ave)>20:
            head_pose_score=0.2
    except:
        head_pose_score = 0  # 一周期没有检测到人脸
        pitch_ave = 20
        roll_ave = 20
        yaw_ave = 20
    else:
       pass

    return round(head_pose_score, 2), round(pitch_ave, 2), round(yaw_ave, 2), round(roll_ave, 2)  # 头部姿态评分权重


def get_fatigue_score(fatigue):
    # 确定疲劳等级提示:小于0.15为清醒，0.15-0.35临界状态，0.35-0.5轻度疲劳，0.5-0.6中度疲劳，大于0.6重度疲劳
    fatigue_score = 1 - fatigue
    if fatigue > 1:
        fatigue_score = 0
    return round(fatigue_score, 2)

def get_focus_score(head_pose_score, emotion_score, fatigue_score):
    focus_score = head_pose_score * 0.3 + emotion_score * 0.2 + fatigue_score * 0.4

    if focus_score < 0.45:
        focus_grade = 4
    elif 0.45 <= focus_score < 0.6:
        focus_grade = 3
    elif 0.6 <= focus_score < 0.7:
        focus_grade = 2
    else:
        focus_grade = 1

    return round(focus_score, 2),focus_grade

def concentrationFrameDetect(photo,emotion_times_dict,fatigue_lst,fatigue_grade_lst,pitch_lst,yaw_lst,roll_lst):
    # 头部得分
    head_pose_score, pitch_ave, yaw_ave, roll_ave = get_head_pose_score(pitch_lst, yaw_lst, roll_lst)
    # 疲劳得分
    '''一个周期都没有检测到人脸,疲劳度？'''
    if fatigue_lst:
        fatigue_score = get_fatigue_score(fatigue_lst[-1])  # 最后一次的fatigue代表一个周期的疲劳度
        fatigue_grade = fatigue_grade_lst[-1]
    else:
        if pitch_ave < 15:  # 低头/抬头检测不到人脸的临界角
            fatigue = 1  # 严重疲劳状态
            fatigue_grade = 5
        else:
            fatigue = 0.5  # 人已经不在镜头视线范围,默认中度疲劳
            fatigue_grade = 4
        fatigue_score = 1 - fatigue  # 疲劳分数正向化

    # 表情得分
    emotion_score, emotion_sort = get_emotion_score(emotion_times_dict)
    emotion_sort_dict = {'optimistic': 1, 'neutral': 2, 'negative': 3}
    emotion_grade = emotion_sort_dict[emotion_sort]  # 情绪等级

    # 专注度得分
    focus_score, focus_grade = get_focus_score(head_pose_score, emotion_score, fatigue_score)

    # --------周期数据写入数据库study_state------------
    # values中参数依次为student_id,state_key,state_value,record_time


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

    return photo

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            pitch, yaw, roll, is_pitch, is_yaw, is_roll, frame = get_euler_angle(frame)
            print(pitch, yaw, roll, is_pitch, is_yaw, is_roll)
        cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) == 27 or cv2.getWindowProperty("Frame",cv2.WND_PROP_AUTOSIZE) != 1:  # ESC的ASCII码，或按交叉退出
            cv2.destroyAllWindows()
            break
