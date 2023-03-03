import cv2
from ConcentrationAnalysis.head_pose_estimation_plus import get_head_pose_estimate_frame


def concentrationFrameDetect(faces, gray, photo):  # frame为摄像头原图，photo是绘制过的图片，在别的模块绘制的基础上再次绘制输出
    frame = photo
    pitch, yaw, roll, modified_frame = get_head_pose_estimate_frame(frame)
    return pitch, yaw, roll, modified_frame


def concentration_test():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            pitch, yaw, roll, modified_frame = concentrationFrameDetect(faces=1, gray=frame, photo=frame)
            cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
            cv2.imshow('Frame', modified_frame)
            if cv2.waitKey(1) == 27:
                break


if __name__ == '__main__':
    concentration_test()
    pass
