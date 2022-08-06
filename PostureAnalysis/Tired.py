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
def findAngle(lmList, img, p1, p2, p3, draw=True):

    # 获取坐标 鼻子 左肩 右肩
    x1, y1, z1 = lmList[p1][1:]
    x2, y2, z2 = lmList[p2][1:]
    x3, y3, z3 = lmList[p3][1:]

    # 绘制
    if draw:
        cv2.line(img, (x2, y2), (x3, y3), (255, 255, 255), 3)
        cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
        cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
        cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
        cv2.putText(img, f'{int(x1), int(y1), int(z1)}', (x1 - 50, y1 - 50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
        cv2.putText(img, f'{int(x2), int(y2), int(z2)}', (x2 - 50, y2 - 50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
        cv2.putText(img, f'{int(x3), int(y3), int(z3)}', (x3 - 50, y3 - 50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)

    return y1, y2, y3, z1, z2, z3


# 主函数 分析姿势并打印
def Posture_analysis(img, pTime):

    # 运行时间评估
    # t = time.time()
    img, results = findPose(img, False)
    # print(time.time() - t)

    lmList = findPosition(img, results, False)
    # print(lmList)

    if len(lmList) != 0:

        # 检查前倾
        # 鼻子 左肩 右肩
        y1, y2, y3, z1, z2, z3= findAngle(lmList, img, 0, 11, 12)
        y_avg = (y2 + y3) / 2
        y_gap = y_avg - y1
        per = np.interp(y_gap, (110, 180), (100, 0))
        # print(y_gap, per)
        z_avg = (z2 + z3)/2
        z_gap = z_avg - z1
        # print(z_gap)
        if z_gap > 40:
            if per == 100:
                cv2.putText(img, f'Head_Ahead', (50, 100), cv2.FONT_HERSHEY_PLAIN, 3,
                            (255, 0, 0), 3)

        # 检查左右倾斜
        y_gap_sh = y2 - y3
        y_gap_sh = abs(y_gap_sh)
        if y_gap_sh > 25:
            cv2.putText(img, f'Body_Lean', (50, 150), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 0), 3)

    # 获取帧率
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'fps:{str(int(fps))}', (50, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)

    # 显示图像
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    return img, pTime


# def main():
#     # cv2.VideoCapture(0) cv2.VideoCapture("Trainer/1.mp4")
#     cap = cv2.VideoCapture(0)
#     pTime = 0
#     while True:
#
#         success, img = cap.read()
#         # img = cv2.imread("Trainer/right2.jpg")
#         img = cv2.resize(img, (1024, 768))
#         img, pTime = Posture_analysis(img, pTime)
#
#
# if __name__ == "__main__":
#     main()
