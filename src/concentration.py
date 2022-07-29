import cv2
import dlib
import matplotlib.pyplot as plt
import numpy as np


# 预测关键点模型（68个关键点）
predictor = dlib.shape_predictor("../lib/shape_predictor_68_face_landmarks.dat")

def concentrationFrameDetect(faces,gray, photo):#frame为摄像头原图，photo是绘制过的图片，在别的模块绘制的基础上再次绘制输出


    #t = time.time()  # 测试执行时间
    for face in faces:
        #print(face)
        points_lst = []  # 存放68个点
        # landmarks 为二维数组
        landmarks = np.matrix([[point.x, point.y] for point in predictor(gray, face).parts()])
        for index, point in enumerate(landmarks):
            coord = (point[0, 0], point[0, 1])  # 获取每个point的坐标
            points_lst.append(coord)
            # 利用cv2.circle给每个特征点画一个圈，共68个
            # cv2.circle(photo, coord, 2, color=(0, 0, 255))

            # 利用cv2.putText输出1-68
            cv2.putText(photo, str(index + 1), coord, fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.3, color=(0, 0, 255), thickness=1)
            # print(f"第{index+1}点,x={coord[0]},y={coord[1]}")
        # print(points_lst)

        six_points_lst = [
            points_lst[36],  # 左眼角
            points_lst[45], # 右眼角
            points_lst[30],  # 鼻尖
            points_lst[48],  # 左嘴角
            points_lst[54],  # 右嘴角
            points_lst[8],  # 下巴
        ]
        six_points=np.array(six_points_lst,dtype="double")
        #print('six_points',six_points)
        model_points = np.array([
            (0.0, 0.0, 0.0),  # Nose tip
            (0.0, -330.0, -65.0),  # Chin
            (-165.0, 170.0, -135.0),  # Left eye left corner
            (165.0, 170.0, -135.0),  # Right eye right corner
            (-150.0, -150.0, -125.0),  # Left Mouth corner
            (150.0, -150.0, -125.0)  # Right mouth corner
        ])
        # print('model_points',model_points)
    #整个代码处理一帧360ms，几乎全部消耗于detector(gray, 1)，zcl注
    #print(time.time()-t)#测试执行时间
    cv2.imshow('all', photo)

    return 0, photo  # 输出识别标签，已经再绘制的图片

if __name__ == '__main__':
    pass