import Tired as td
import cv2


def main():

    # cv2.VideoCapture(0) cv2.VideoCapture("Trainer/1.mp4")
    cap = cv2.VideoCapture(0)
    pTime = 0
    while True:

        success, img = cap.read()
        # img = cv2.imread("Trainer/right2.jpg")
        img = cv2.resize(img, (1024, 768))
        img, pTime = td.Posture_analysis(img, pTime)


if __name__ == "__main__":
    main()

