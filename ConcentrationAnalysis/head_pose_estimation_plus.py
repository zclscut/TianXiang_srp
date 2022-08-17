'''
pitch最大值:18.63,最小值:-35.37
yaw最大值:47.05,最小值:-49.59
roll最大值:176.38,最小值:-179.37
'''

import time
import cv2 as cv
import numpy as np
import dlib
from imutils import face_utils # 人脸数据处理

t0 = time.time()
# 人脸检测模型
detector = dlib.get_frontal_face_detector()
# 人脸关键点预测
predictor = dlib.shape_predictor('../lib/shape_predictor_68_face_landmarks.dat')
t1 = time.time()
print(f'模型加载时间: {round((t1 - t0) * 1000, 2)}ms')


def get_image_points(shape):
    landmarks = face_utils.shape_to_np(shape) # landmarks从0开始,与实际脸部标号差1
    image_points = np.float32([landmarks[17], # 左眉左上角
                               landmarks[21], # 左眉右上角
                               landmarks[22], # 右眉左上角
                               landmarks[26], # 右眉右上角
                               landmarks[36], # 左眼左上角
                               landmarks[39], # 左眼右上角
                               landmarks[42], # 右眼左上角
                               landmarks[45], # 右眼右上角
                               landmarks[31], # 鼻子左上角
                               landmarks[35], # 鼻子右上角
                               landmarks[48], # 嘴左上角
                               landmarks[54], # 嘴右上角
                               landmarks[57], # 嘴中央下角
                               landmarks[8]]) # 下巴角
    return image_points


# 根据2d点,3d点,相机内参,畸变参数,获得euler_angle
def get_euler_angle(img_size, image_points):
    # 3d模型坐标,参照https://github.com/by-sabbir/HeadPoseEstimation/blob/master/Visualize3DModel.py
    object_points = np.float32([[6.825897, 6.760612, 4.402142],  # 左眉左上角
                                [1.330353, 7.122144, 6.903745],  # 左眉右上角
                                [-1.330353, 7.122144, 6.903745],  # 右眉左上角
                                [-6.825897, 6.760612, 4.402142],  # 右眉右上角
                                [5.311432, 5.485328, 3.987654],  # 左眼左上角
                                [1.789930, 5.393625, 4.413414],  # 左眼右上角
                                [-1.789930, 5.393625, 4.413414],  # 右眼左上角
                                [-5.311432, 5.485328, 3.987654],  # 右眼右上角
                                [2.005628, 1.409845, 6.165652],  # 鼻子左上角
                                [-2.005628, 1.409845, 6.165652],  # 鼻子右上角
                                [2.774015, -2.080775, 5.048531],  # 嘴左上角
                                [-2.774015, -2.080775, 5.048531],  # 嘴右上角
                                [0.000000, -3.116408, 6.097667],  # 嘴中央下角
                                [0.000000, -7.415691, 4.070434]])  # 下巴角

    # 焦距focal_length(相机坐标系与图像坐标系之间的距离为焦距f，也即图像坐标系原点与焦点重合)
    focal_length = img_size[1]
    center = (img_size[1] / 2, img_size[0] / 2)
    camera_matrix = np.array(
        [[focal_length, 0, center[0]],
         [0, focal_length, center[1]],
         [0, 0, 1]], dtype="double"
    )

    # 相机外参假设为0
    dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion

    _, rotation_vector, translation_vector = cv.solvePnP(objectPoints=object_points, imagePoints=image_points,
                                                         cameraMatrix=camera_matrix, distCoeffs=dist_coeffs,
                                                         flags=cv.SOLVEPNP_ITERATIVE)
    rotation_mat, _ = cv.Rodrigues(rotation_vector)  # 将旋转矩阵向量转换为旋转矩阵
    pose_mat = cv.hconcat((rotation_mat, translation_vector))  # 水平拼接
    # eulerAngles –可选的三元素矢量，包含三个以度为单位的欧拉旋转角度
    _, _, _, _, _, _, euler_angle = cv.decomposeProjectionMatrix(pose_mat)  # 计算euler_angle

    return euler_angle


# 将旋转矩阵转为欧拉角
def trans_euler_angle(euler_angle):
    pitch = euler_angle[0, 0]
    yaw = euler_angle[1, 0]
    roll = euler_angle[2, 0]

    return pitch, yaw, roll


def get_head_pose_estimate_frame(frame):
    frame_size = frame.shape # 获取每帧的尺寸
    # print(f'frame_size:{size},类型:{type(size)}')

    gray=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    faces = detector(gray, 0)  # 检测人脸,运行消耗时间平均80ms
    if faces: # 检测到人脸
        for face in faces:
            shape = predictor(frame, face)

            image_points = get_image_points(shape)  # 获取面部2d关键点
            euler_angle = get_euler_angle(img_size=frame_size, image_points=image_points)
            pitch, yaw, roll = trans_euler_angle(euler_angle)
            # print('pitch:{}, yaw:{}, roll:{}'.format(pitch, yaw, roll))

            # cv.putText(frame, f'pitch: {round(pitch, 2)}', (30, 150), fontFace=cv.FONT_HERSHEY_SIMPLEX,
            #            fontScale=1, color=(0, 0, 255), thickness=2)
            # cv.putText(frame, f'yaw: {round(yaw, 2)}', (30, 180), fontFace=cv.FONT_HERSHEY_SIMPLEX,
            #            fontScale=1, color=(0, 0, 255), thickness=2)
            # cv.putText(frame, f'roll: {round(roll, 2)}', (30, 210), fontFace=cv.FONT_HERSHEY_SIMPLEX,
            #            fontScale=1, color=(0, 0, 255), thickness=2)

            return round(pitch,2),round(yaw,2),round(roll,2),frame

    else: # 未检测到人脸
        pitch, yaw, roll = 100, 100, 100
        return pitch,yaw,roll,frame




def webcam_test():  # 摄像头获取帧数据测试
    cap = cv.VideoCapture(0)
    pitch_lst=[]
    yaw_lst=[]
    roll_lst=[]
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            pitch,yaw,roll,modified_frame = get_head_pose_estimate_frame(frame)
            pitch_lst.append(pitch)
            yaw_lst.append(yaw)
            roll_lst.append(roll)
            # 显示
            cv.namedWindow('Frame', cv.WINDOW_NORMAL)
            cv.imshow('Frame', modified_frame)
            if cv.waitKey(1) == 27:
                print(f'pitch最大值:{max(pitch_lst)},最小值:{min(pitch_lst)}')
                print(f'yaw最大值:{max(yaw_lst)},最小值:{min(yaw_lst)}')
                print(f'roll最大值:{max(roll_lst)},最小值:{min(roll_lst)}')
                cv.destroyAllWindows()
                break


if __name__ == '__main__':
    webcam_test()
