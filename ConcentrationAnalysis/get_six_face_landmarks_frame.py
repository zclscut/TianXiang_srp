import cv2
import dlib
import matplotlib.pyplot as plt
import numpy as np


def get_six_points(frame):
    '''
    @function 获取头部姿态6个关键点
    @input 输入视频的帧
    @output 以数组形式输出头部姿态的6个关键点坐标
    '''

    # 读取图片并灰度化处理
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 调用人脸检测器
    detector = dlib.get_frontal_face_detector()

    # 预测关键点模型（68个关键点）
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    # 人脸检测
    faces = detector(gray, 1)  # 1:将图片放大一倍，便于识别人脸; 0 原始图像

    for face in faces:
        # 绘制矩形框
        face_diag_points = [(face.left(), face.top()), (face.right(), face.bottom())]
        # print('左上角和右下角坐标:'+str(face_diag_points))
        cv2.rectangle(frame, (face.left(), face.top()),  # 左上顶点
                      (face.right(), face.bottom()),  # 右下顶点
                      color=(0, 255, 0),  # 绿色
                      thickness=2)

        points_lst = []  # 存放68个点
        # landmarks 为二维数组
        landmarks = np.matrix([[point.x, point.y] for point in predictor(frame, face).parts()])
        for index, point in enumerate(landmarks):
            coord = (point[0, 0], point[0, 1])  # 获取每个point的坐标
            points_lst.append(coord)
            # 利用cv2.circle给每个特征点画一个圈，共68个
            # cv2.circle(frame, coord, 2, color=(0, 255, 255))

            # 利用cv2.putText输出1-68
            cv2.putText(frame, str(index + 1), coord, fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.4, color=(0, 0, 255), thickness=1)
            # print(f"第{index+1}点,x={coord[0]},y={coord[1]}")
        # print(points_lst)

        six_points_lst = [
            points_lst[36],  # 左眼角
            points_lst[45],  # 右眼角
            points_lst[30],  # 鼻尖
            points_lst[48],  # 左嘴角
            points_lst[54],  # 右嘴角
            points_lst[8],  # 下巴
        ]
        six_landmarks_array=np.array([(points_lst[30][0],points_lst[30][1]),
                                 (points_lst[8][0],points_lst[8][1]),
                                 (points_lst[36][0],points_lst[36][1]),
                                 (points_lst[45][0],points_lst[45][1]),
                                 (points_lst[48][0],points_lst[48][1]),
                                 (points_lst[54][0],points_lst[54][1])])

        model_points = np.array([
            (0.0, 0.0, 0.0),  # Nose tip
            (0.0, -330.0, -65.0),  # Chin
            (-165.0, 170.0, -135.0),  # Left eye left corner
            (165.0, 170.0, -135.0),  # Right eye right corne
            (-150.0, -150.0, -125.0),  # Left Mouth corner
            (150.0, -150.0, -125.0)  # Right mouth corner
        ])
        # print('model_points', model_points)
    # 图片显示
    plt.imshow(frame[:, :, ::-1])
    plt.title("68_face_landmarks")
    plt.axis("off")
    plt.show()
    return six_landmarks_array


if __name__ == '__main__':
    frame = cv2.imread('./16.png', 1)
    print(get_six_points(frame))
