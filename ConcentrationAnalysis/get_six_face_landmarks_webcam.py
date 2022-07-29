import dlib
import time
import numpy as np
import cv2


def get_six_points():
    # 调用人脸检测器
    detector = dlib.get_frontal_face_detector()

    # 预测关键点模型（68个关键点）
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    captureFrame = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 创建一个captureFrame对象
    while True:
        return_value, frame = captureFrame.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 灰度处理

        # 人脸检测

        faces = detector(gray, 1)  # 1:将图片放大一倍，便于识别人脸; 0 原始图像
        #t = time.time()  # 测试执行时间
        for face in faces:
            points_lst = []  # 存放68个点
            # landmarks 为二维数组
            landmarks = np.matrix([[point.x, point.y] for point in predictor(gray, face).parts()])
            for index, point in enumerate(landmarks):
                coord = (point[0, 0], point[0, 1])  # 获取每个point的坐标
                points_lst.append(coord)
                # 利用cv2.circle给每个特征点画一个圈，共68个
                # cv2.circle(frame, coord, 2, color=(0, 0, 255))

                # 利用cv2.putText输出1-68
                cv2.putText(frame, str(index + 1), coord, fontFace=cv2.FONT_HERSHEY_SIMPLEX,
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
                (165.0, 170.0, -135.0),  # Right eye right corne
                (-150.0, -150.0, -125.0),  # Left Mouth corner
                (150.0, -150.0, -125.0)  # Right mouth corner
            ])
            # print('model_points',model_points)
        #整个代码处理一帧360ms，几乎全部消耗于detector(gray, 1)，zcl注
        #print(time.time()-t)#测试执行时间
        cv2.imshow('all', frame)
        k = cv2.waitKey(5)
        if k == 27 or cv2.getWindowProperty("all",cv2.WND_PROP_AUTOSIZE) != 1:  # ESC的ASCII码，或者×关闭窗口,zcl改
            break

if __name__ == '__main__':
    get_six_points()