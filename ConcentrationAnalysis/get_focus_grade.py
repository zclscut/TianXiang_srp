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
    '''
    function: 绘制头部姿态图
    :param img:
    :param directions_lst:
    :param bound_box_lst:
    :param landmarks_lst:
    :param show_bbox:
    :param show_landmarks:
    :return: img
    '''
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
        cv2.putText(frame, f'pitch: {round(pitch, 2)}', (20, 100), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.8, color=(0, 0, 255), thickness=2)
        cv2.putText(frame, f'yaw: {round(yaw, 2)}', (20, 130), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.8, color=(0, 0, 255), thickness=2)
        cv2.putText(frame, f'roll: {round(roll, 2)}', (20, 160), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.8, color=(0, 0, 255), thickness=2)
        # 添加轴
        modified_frame = draw_pose(
            frame,
            directions_lst,
            np.array([bboxes[-1]]),
            landmarks_lst, )

    except:  # 未检测到人脸时候返回原始图片
        pitch, yaw, roll=60,70,70
        return pitch,yaw,roll, frame
    else:
        return pitch,yaw,roll, modified_frame


def get_overall_emotion_score(detect_times,emotion_times_dict):
    '''
    根据一个周期内的表情次数(emotion_times_dict)计算表情综合评分(overall_emotion_score)
    :param detect_times:
    :param emotion_times_dict:
    :return:
    '''
    # 根据AHP获取的每个表情所占的二级权重
    emotion_weight_dict={'Angry':0.06312521,'Hate':0.02693035,'Fear':0.03981097,'Happy':0.36753161,
                 'Sad':0.05957265,'Surprise':0.25979793,'Neutral':0.18323128,}
    overall_emotion_score=0
    for key,value in emotion_weight_dict.items():
        overall_emotion_score+=100*(emotion_times_dict[key]/detect_times)*value
    print(f'表情综合得分:{round(overall_emotion_score,2)}')
    return overall_emotion_score # 表情综合评分


def get_fatigue_score(detect_times,eye_close_time_lst,yawn_times,mouth_open_time_lst,blink_times,detect_time):
    '''
    根据一个周期中眨眼次数、打哈欠次数和总闭眼时间确定疲劳度得分
    :param eye_close_time_lst:一个周期中闭眼时长列表
    :param mouth_open_time_lst:一个周期中闭眼时长列表
    :param detect_time:一个周期检测消耗时长
    :param yawn_times: 一个周期中打哈欠次数(连续3帧检测)
    :param blink_times: 一个周期中眨眼次数(连续3帧检测)
    :param detect_times:
    :return:
    '''
    if eye_close_time_lst==[]:
        eye_close_time_lst.append(0)
    if mouth_open_time_lst==[]:
        mouth_open_time_lst.append(0)
    eye_close_time_ratio=sum(eye_close_time_lst)/detect_time
    mouth_open_time_ratio=sum(mouth_open_time_lst)/detect_time
    blink_freq=blink_times/detect_times # 眨眼频率
    yawn_fraq=yawn_times/detect_times # 打哈欠频率

    # 一般情况得分
    fatigue_score=100*min([0.4*(1-blink_freq),0.6*(1-yawn_fraq)])

    # 疲劳状态得分为0
    # 闭眼时长大于2s
    # 嘴巴张大时长大于2s
    if (max(eye_close_time_lst)>2) or (max(mouth_open_time_lst)>2):
        fatigue_score=0
    print(f'疲劳度得分{round(fatigue_score,2)}')

    return fatigue_score



def get_head_pose_score(pitch_lst,yaw_lst):
    '''
    根据一个周期内的抬头/低头(pitch)或转头(yaw)角度的均值计算头部姿态的评分
    :param pitch_lst:
    :param yaw_lst:
    :return:
    '''
    # 绝对值求和并计算平均值
    pitch_sum,yaw_sum=0,0
    for p,y in zip(pitch_lst,yaw_lst):
        pitch_sum+=abs(p)
        yaw_sum+=abs(y)
    pitch_ave=pitch_sum/len(pitch_lst)
    yaw_ave=yaw_sum/len(yaw_lst)

    # 计算权重
    if pitch_ave>60: # 抬头/低头角度大于60度,权重视为0,得分为0
        pitch_weight=0
    else:
        pitch_weight=1-pitch_ave/60
    if yaw_ave>70: # 左/右转头角度大于70度,权重视为0,得分为0
        yaw_weight=0
    else:
        yaw_weight=1-yaw_ave/70
    # pitch和yaw的都同等重要表征不专注
    head_pose_score=100*(min(pitch_weight,yaw_weight))
    print(f'头部姿态得分{round(head_pose_score,2)}')
    return  head_pose_score # 头部姿态评分权重


def get_focus_grade(focus_score):
    '''
    根据专注度评分得到专注度等级
    :param focus_score:
    :return:
    '''
    focus_grade=None
    return focus_grade


def concentrationFrameDetect(faces,gray, photo):#frame为摄像头原图，photo是绘制过的图片，在别的模块绘制的基础上再次绘制输出
    frame=photo
    pitch,yaw,roll,modified_frame=get_euler_angle(frame)
    return pitch,yaw,roll,modified_frame

if __name__ == '__main__':
    pass

