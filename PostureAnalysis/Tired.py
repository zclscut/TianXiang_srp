import cv2
import numpy as np
import time
import mediapipe as mp

class poseDetector():

    def __init__(self, mode=False, complexity=1,  smooth=True,
                 enable_seg=False, smooth_seg=True, detection_confidence=0.5,
                 tracking_confidence=0.5):

        self.mode = mode
        self.complexity = complexity
        self.smooth = smooth
        self.enable_seg = enable_seg
        self.smooth_seg = smooth_seg
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smooth, self.enable_seg,
                                     self.smooth_seg, self.detection_confidence, self.tracking_confidence)

    def findPose(self, img, draw=True):

        # 检测姿势
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        # 获取坐标
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw=True):

        # 获取坐标 鼻子 左肩 右肩
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        # 绘制
        if draw:
            cv2.line(img, (x2, y2), (x3, y3), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(y1)), (x1 - 50, y1 - 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            cv2.putText(img, str(int(y2)), (x2 - 50, y2 - 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            cv2.putText(img, str(int(y3)), (x3 - 50, y3 - 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        return y1, y2, y3


# def main():
#     # cv2.VideoCapture(0) cv2.VideoCapture("Trainer/1.mp4")
#     cap = cv2.VideoCapture(0)
#
#     detector = poseDetector()
#     count = 0
#     dir = 0
#     pTime = 0
#
#     while True:
#         success, img = cap.read()
#         # img = cv2.imread("Trainer/test1.jpg")
#
#         t = time.time()
#         img = detector.findPose(img, False)
#         print(time.time() - t)
#
#         img = cv2.resize(img, (1080, 640))
#         lmList = detector.findPosition(img, False)
#         # print(lmList)
#         if len(lmList) != 0:
#             # 鼻子 左肩 右肩
#             # 检查低头
#             y1, y2, y3 = detector.findAngle(img, 0, 11, 12)
#             y_avg = (y2 + y3)/2
#             y_gap = y_avg - y1
#             per = np.interp(y_gap, (0, 10), (100, 0))
#             # print(y_gap, per)
#
#             if per == 100:
#                 if dir == 0:
#                     count += 1
#                     dir = 1
#             if per == 0:
#                 if dir == 1:
#                     dir = 0
#             # print(count)
#
#             cv2.putText(img, str(int(count)), (50, 300), cv2.FONT_HERSHEY_PLAIN, 5,
#                         (255, 0, 0), 5)
#             cv2.putText(img, f'{int(per)} %', (50, 200), cv2.FONT_HERSHEY_PLAIN, 5,
#                         (255, 0, 0), 5)
#         cTime = time.time()
#         fps = 1 / (cTime - pTime)
#         pTime = cTime
#         cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
#                     (255, 0, 0), 5)
#
#         cv2.imshow("Image", img)
#         cv2.waitKey(1)
#
#
# if __name__ == "__main__":
#     main()






def Posture_analysis(img, count, dir, pTime):

    detector = poseDetector()

    t = time.time()
    img = detector.findPose(img, False)
    print(time.time() - t)

    img = cv2.resize(img, (1080, 640))
    lmList = detector.findPosition(img, False)

    # print(lmList)
    if len(lmList) != 0:
        # 鼻子 左肩 右肩
        # 检查低头
        y1, y2, y3 = detector.findAngle(img, 0, 11, 12)
        y_avg = (y2 + y3) / 2
        y_gap = y_avg - y1
        per = np.interp(y_gap, (0, 10), (100, 0))
        # print(y_gap, per)

        if per == 100:
            if dir == 0:
                count += 1
                dir = 1
        if per == 0:
            if dir == 1:
                dir = 0
        # print(count)

        cv2.putText(img, str(int(count)), (50, 300), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)
        cv2.putText(img, f'{int(per)} %', (50, 200), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
    return (count, dir, pTime)


# def main():
#     # cv2.VideoCapture(0) cv2.VideoCapture("Trainer/1.mp4")
#     cap = cv2.VideoCapture(0)
#     count = 0
#     dir = 0
#     pTime = 0
#     while True:
#
#         success, img = cap.read()
#         # img = cv2.imread("Trainer/test1.jpg")
#         count, dir, pTime = Posture_analysis(img, count, dir, pTime)
#
# if __name__ == "__main__":
#     main()