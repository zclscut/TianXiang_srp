import cv2
import mediapipe as mp
import time

mpDraw = mp.solutions.drawing_utils
# 创建模型 参数Pose
mpPose = mp.solutions.pose
pose = mpPose.Pose()

cap = cv2.VideoCapture('PoseVideos/1.mp4')
pTime = 0


while True:
    success, img = cap.read()  # 读取视频文件
    # 检测姿势
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    # 绘制
    # print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        # 获取像素点
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            print(id, lm)
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)



    # 帧率
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # 位置 字体 大小 颜色 粗细
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)  # 延迟

