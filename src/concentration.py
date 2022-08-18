'''
一次检测就是一帧
detect_times为检测一轮的总次数(帧数):可在主程序中设定
detect_cost_time为检测一轮消耗总时长
'''
import time
import cv2
import numpy as np
from ConcentrationAnalysis.head_pose_functions import  estimate_head_pose


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
        pitch, yaw, roll=100,100,100
        return pitch,yaw,roll, frame
    else:
        return pitch,yaw,roll, modified_frame


def get_emotion_score(emotion_times_dict):
    down_dict = sorted(emotion_times_dict.items(), key=lambda x: x[1], reverse=True)  # 降序
    print(f'emotion_times_lst:{down_dict}')
    emotion_sort_dict = {'optimistic': 0, 'neutral': 0, 'negative': 0}
    for key, value in emotion_times_dict.items():  # 转换为三类情绪
        if key == 'Happy':
            emotion_sort_dict['optimistic'] = value
        elif key == 'Surprise' or key == 'Neutral':
            emotion_sort_dict['neutral'] = emotion_sort_dict['neutral'] + value
        else:
            emotion_sort_dict['negative'] = emotion_sort_dict['negative'] + value
    times_lst = [value for key, value in emotion_sort_dict.items()]

    # 以一个周期内出现情绪次数类别最多组划分情绪类别
    down_emotion_sort_lst = sorted(emotion_sort_dict.items(), key=lambda x: x[1], reverse=True)
    emotion_sort = down_emotion_sort_lst[0][0]
    try:
        for key, value in emotion_sort_dict.items():  # 归一化
            emotion_sort_dict[key] = value / sum(times_lst)
    except:
        emotion_score = 0  # 一个周期内均没检测到人脸
        emotion_sort = 'negative'  # 情绪划分视为消极？
    else:
        emotion_score = emotion_sort_dict['optimistic'] * 0.5 + emotion_sort_dict['neutral'] * 0.3 + \
                        emotion_sort_dict['negative'] * 0.2
    return round(emotion_score / 0.5, 2), emotion_sort


def get_head_pose_score(pitch_lst,yaw_lst,roll_lst):
    # 头部姿态角取三者最大值
    try:
        pitch_ave = sum(pitch_lst) / len(pitch_lst)
        yaw_ave = sum(yaw_lst) / len(yaw_lst)
        roll_ave = sum(roll_lst) / len(roll_lst)
    except:
        head_pose_score = 0  # 没有检测到人脸
        pitch_ave=20
        roll_ave=40
        yaw_ave=20
    else:
        if pitch_ave > 15:  # 抬头/低头角度大于15度,权重视为0,得分为0
            pitch_weight = 0
        else:
            pitch_weight = 1 - pitch_ave/15
        if yaw_ave > 40:  # 左/右转头角度大于40度,权重视为0,得分为0
            yaw_weight = 0
        else:
            yaw_weight = 1 - yaw_ave/40
        if roll_ave > 20:
            roll_weight =0
        else:
            roll_weight = 1 - roll_ave/20
        head_pose_score=min(pitch_weight,yaw_weight,roll_weight)
    return  round(head_pose_score,2),round(pitch_ave,2),round(yaw_ave,2),round(roll_ave,2) # 头部姿态评分权重


def get_fatigue_score(fatigue):
    # 确定疲劳等级提示:小于0.15为清醒，0.15-0.35临界状态，0.35-0.5轻度疲劳，0.5-0.6中度疲劳，大于0.6重度疲劳
    fatigue_score=1-fatigue
    if fatigue>1:
        fatigue_score=0
    return round(fatigue_score,2)


def concentrationFrameDetect(faces,gray, photo):#frame为摄像头原图，photo是绘制过的图片，在别的模块绘制的基础上再次绘制输出
    frame=photo
    pitch,yaw,roll,photo=get_euler_angle(frame)
    return pitch,yaw,roll,photo

if __name__ == '__main__':
    cap=cv2.VideoCapture(0)
    while cap.isOpened():
        ret,frame=cap.read()
        if ret:
            pitch, yaw, roll, frame = get_euler_angle(frame)
        cv2.namedWindow('Frame',cv2.WINDOW_NORMAL)
        cv2.imshow('Frame',frame)
        if cv2.waitKey(1)==27:
            cv2.destroyAllWindows()
            break



