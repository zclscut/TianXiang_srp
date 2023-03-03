import cv2
import numpy as np
import time
import mediapipe as mp

# OPENCV 初始化
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

# 获取关键点，绘制所有关键点与连线
def findPose(img, draw=True):

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    if results.pose_landmarks:
        if draw:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
    return img, results

# 获取坐标存入列表
def findPosition(img, results, draw=True):

    lmList = []
    if results.pose_landmarks:
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy, cz = int(lm.x * w), int(lm.y * h), int(lm.z * 100)
            lmList.append([id, cx, cy, cz])
            if draw:
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
    return lmList

# 获取坐标 鼻子 左肩 右肩，强调绘制
def findAngle(lmList, img, p1, p2, p3, p4, p5, draw=True):

    # 获取坐标 鼻子 左肩 右肩 左眼 左耳
    x1, y1, z1 = lmList[p1][1:]
    x2, y2, z2 = lmList[p2][1:]
    x3, y3, z3 = lmList[p3][1:]
    x4, y4, z4 = lmList[p4][1:]
    x5, y5, z5 = lmList[p5][1:]
    # 绘制
    if draw:
        cv2.line(img, (x2, y2), (x3, y3), (255, 255, 255), 3)
        cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
        cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
        cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
        cv2.circle(img, (x4, y4), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x4, y4), 15, (0, 0, 255), 2)
        cv2.circle(img, (x5, y5), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x5, y5), 15, (0, 0, 255), 2)
        cv2.putText(img, f'{int(x1), int(y1), int(z1)}', (x1 - 50, y1 - 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
        cv2.putText(img, f'{int(x2), int(y2), int(z2)}', (x2 - 50, y2 - 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
        cv2.putText(img, f'{int(x3), int(y3), int(z3)}', (x3 - 50, y3 - 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
        cv2.putText(img, f'{int(x4), int(y4), int(z4)}', (x4 - 50, y4 - 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
        cv2.putText(img, f'{int(x5), int(y5), int(z5)}', (x5 - 50, y5 - 50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)

    return y1, y2, y3, z1, z2, z3, y4, y5


# 主函数 分析姿势并打印
def postureFrameDetect(frame, photo):

    photo, results = findPose(photo, False)
    lmList = findPosition(photo, results, False)
    isPosture = 0

    if len(lmList) != 0:

        # 检查前倾
        # 鼻子 左肩 右肩 左眼 左耳
        y1, y2, y3, z1, z2, z3, y4, y5 = findAngle(lmList, photo, 0, 11, 12, 1, 7)
        y_avg = (y2 + y3) / 2
        y_gap = y_avg - y1
        per = np.interp(y_gap, (110, 180), (100, 0))
        z_avg = (z2 + z3)/2
        z_gap = z_avg - z1
        y_head_gap = y4 - y5
        # 判断头部是否往前
        if z_gap > 40:
            # 判断是否低头
            if per == 100:
                # 脸部朝前
                if y_head_gap < 30:
                    cv2.putText(photo, f'Head_Up', (50, 100), cv2.FONT_HERSHEY_PLAIN, 3,
                                (255, 0, 0), 3)
                    isPosture = 1
                # 脸部朝下
                else:
                    cv2.putText(photo, f'Head_Ahead', (50, 100), cv2.FONT_HERSHEY_PLAIN, 3,
                                (255, 0, 0), 3)
                    isPosture = 1

        # 检查左右倾斜
        y_gap_sh = y2 - y3
        y_gap_sh = abs(y_gap_sh)
        if y_gap_sh > 25:
            cv2.putText(photo, f'Body_Lean', (50, 150), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 0), 3)
            isPosture = 1

    # 显示图像
    return isPosture, photo

# 增加posture_grade参数
def postureFrameDetectCopy(frame,photo):
    photo, results = findPose(photo, False)
    lmList = findPosition(photo, results, False)
    isPosture = 0
    posture_grade=1 # 没有检测到身体坐标,默认坐姿正常

    # is_参数为0表示没有超过阈值,为1表示超过阈值
    # 没有检测到身体坐标时候默认为没有超过阈值
    is_z_gap=0
    is_y_head_gap=0
    is_y_gap_sh = 0

    is_per = 0  # 为100表明没有超过阈值,不为100则超过阈值

    if len(lmList) != 0:

        # 检查前倾
        # 鼻子 左肩 右肩 左眼 左耳
        y1, y2, y3, z1, z2, z3, y4, y5 = findAngle(lmList, photo, 0, 11, 12, 1, 7)
        y_avg = (y2 + y3) / 2
        y_gap = y_avg - y1
        per = np.interp(y_gap, (110, 180), (100, 0))
        z_avg = (z2 + z3)/2
        z_gap = z_avg - z1
        y_head_gap = y4 - y5
        # 判断头部是否往前
        is_z_gap = 0
        if z_gap > 40:
            is_z_gap=1
            # 判断是否低头
            is_per = 1
            if per == 100:
                is_per=0
                # 脸部朝前
                if y_head_gap < 30:
                    cv2.putText(photo, f'Head_Up', (50, 100), cv2.FONT_HERSHEY_PLAIN, 3,
                                (255, 0, 0), 3)
                    isPosture = 1
                    posture_grade = 2 # Head_Up脸部朝前
                    is_y_head_gap=0
                # 脸部朝下
                else:
                    cv2.putText(photo, f'Head_Ahead', (50, 100), cv2.FONT_HERSHEY_PLAIN, 3,
                                (255, 0, 0), 3)
                    isPosture = 1
                    posture_grade=3 # Head_Ahead脸部朝下
                    is_y_head_gap=1

        # 检查左右倾斜
        y_gap_sh = y2 - y3
        y_gap_sh = abs(y_gap_sh)
        is_y_gap_sh = 0
        if y_gap_sh > 25:
            cv2.putText(photo, f'Body_Lean', (50, 150), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 0), 3)
            isPosture = 1
            posture_grade = 4  # Body_Lean身体倾斜
            is_y_gap_sh=1 # 超出阈值

    # 显示图像
    return is_z_gap,is_y_gap_sh,is_y_head_gap,is_per,isPosture,posture_grade,photo

def run():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            is_z_gap, is_y_gap_sh, is_y_head_gap, is_per, isPosture, posture_grade, photo =\
                postureFrameDetectCopy(frame,frame)
            print(is_z_gap, is_y_gap_sh, is_y_head_gap, is_per, isPosture, posture_grade)
            cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
            cv2.imshow('Frame', photo)
            if cv2.waitKey(1) == 27:
                break
if __name__ =='__main__':
    run()
    pass