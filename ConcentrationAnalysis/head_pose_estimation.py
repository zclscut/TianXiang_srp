import time
import cv2
import numpy as np
from head_pose_functions import estimate_head_pose


# 模型初始化
t0=time.time()
from lib.head_pose_model.FaceDetection.FaceBoxes_ONNX import FaceBoxes_ONNX  # 人脸检测
from lib.head_pose_model.FaceAlignment3D.TDDFA_ONNX import TDDFA_ONNX  # 人脸的3D标志点检测
face_boxes = FaceBoxes_ONNX()
tddfa = TDDFA_ONNX()
t1=time.time()
print(f'模型初始化时间:{round((t1-t0)*1000,2)}ms')


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


def main(frame):
    try:
        t0 = time.time()
        bboxes = face_boxes(frame)  # 每一帧中脸部数据构成的ndarry
        # print(f'检测到{len(bboxes)}张脸 ')

        # 计算欧拉角
        param_lst, roi_box_lst = tddfa(frame, np.array([bboxes[-1]]))  # 只计算左边第一张脸
        landmarks_lst = tddfa.recon_vers(param_lst, roi_box_lst) # landmarks_lst为所有人脸的68点3D坐标
        euler_angle_lst, directions_lst, landmarks_lst = estimate_head_pose(landmarks_lst, True)

        t1 = time.time()

        roll, yaw, pitch = euler_angle_lst[-1]  # 选取左边第一张脸
        print(f'roll: {round(roll, 2)}, yaw: {round(yaw, 2)}, pitch: {round(pitch, 2)} cost time: {round((t1 - t0) * 1000, 2)}ms')

        # 添加文字信息
        cv2.putText(frame, f'{len(bboxes)}face(s) detected ', (20, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.8, color=(255, 0, 0), thickness=2)
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

    except:    # 没有检测到人脸时候返回原始图片
        pitch, yaw, roll=0, 0, 0
        return frame,pitch, yaw,roll
    else:
        return modified_frame, pitch, yaw,roll



if __name__ == "__main__":
    t3=time.time()
    frame=cv2.imread('../images/euler_angle_test.png')
    modified_frame, pitch, yaw,roll=main(frame)

    #显示
    cv2.namedWindow('Frame',cv2.WINDOW_NORMAL)
    cv2.imshow('Frame',modified_frame)
    t4=time.time()
    print(f'total_cost_time: {round((t4-t3)*1000,2)}ms')
    if cv2.waitKey(0)==27:
        cv2.destroyAllWindows()


