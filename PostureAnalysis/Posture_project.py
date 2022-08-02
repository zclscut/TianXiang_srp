import Tired as td
import cv2

def main():
    # cv2.VideoCapture(0) cv2.VideoCapture("Trainer/1.mp4")
    cap = cv2.VideoCapture("Trainer/1.mp4")
    count = 0
    dir = 0
    pTime = 0

    while True:

        success, img = cap.read()
        # img = cv2.imread("Trainer/test1.jpg")
        count, dir, pTime = td.Posture_analysis(img, count, dir, pTime)


if __name__ == "__main__":
    main()