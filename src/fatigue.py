import dlib
import cv2
from imutils import face_utils
import numpy as np
import imutils
import time


# 第一步：使用dlib.get_frontal_face_detector() 获得脸部位置检测器
detector = dlib.get_frontal_face_detector()
# 第二步：使用dlib.shape_predictor获得脸部特征位置检测器
predictor = dlib.shape_predictor('../lib/shape_predictor_68_face_landmarks.dat')

def eye_aspect_ratio(eye):
    # 垂直眼标志（X，Y）坐标
    A = np.linalg.norm(eye[1] - eye[5])  # 计算两个集合之间的欧式距离
    B = np.linalg.norm(eye[2] - eye[4])
    # 计算水平之间的欧几里得距离
    # 水平眼标志（X，Y）坐标
    C = np.linalg.norm(eye[0] - eye[3])
    # 眼睛长宽比的计算
    ear = (A + B) / (2.0 * C)
    # 返回眼睛的长宽比
    return ear

def mouth_aspect_ratio(mouth):  # 嘴部
    A = np.linalg.norm(mouth[2] - mouth[9])  # 51, 59
    B = np.linalg.norm(mouth[4] - mouth[7])  # 53, 57
    C = np.linalg.norm(mouth[0] - mouth[6])  # 49, 55
    mar = (A + B) / (2.0 * C)
    return mar

def ear_mar(gray, rect):
    shape = predictor(gray, rect)
    # 第八步：将脸部特征信息转换为数组array的格式
    shape = face_utils.shape_to_np(shape)

    # 第九步：提取左眼和右眼坐标
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
    leftEye = shape[lStart:lEnd]
    rightEye = shape[rStart:rEnd]
    # 嘴巴坐标
    mouth = shape[mStart:mEnd]

    # 第十步：构造函数计算左右眼的EAR值，使用平均值作为最终的EAR
    leftEAR = eye_aspect_ratio(leftEye)
    rightEAR = eye_aspect_ratio(rightEye)
    ear = (leftEAR + rightEAR) / 2.0
    # 打哈欠
    mar = mouth_aspect_ratio(mouth)

    # 第十一步：使用cv2.convexHull获得凸包位置，使用drawContours画出轮廓位置进行画图操作
    # leftEyeHull = cv2.convexHull(leftEye)
    # rightEyeHull = cv2.convexHull(rightEye)
    # cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
    # cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
    # mouthHull = cv2.convexHull(mouth)
    # cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)

    # 第十二步：进行画图操作，用矩形框标注人脸
    left = rect.left()
    top = rect.top()
    right = rect.right()
    bottom = rect.bottom()
    # cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 1)
    return ear, mar

# 眼部参数
def eye_params(ear, eye_conti_frames, step_frames, blink_times, eye_close_times, eye_close_frames):
    if ear < 0.22:  # 眼睛长宽比：0.22
        eye_conti_frames += 1
    else:
        # 如果小于阈值，则表示进行了一次眨眼活动
        if 1 <= eye_conti_frames < step_frames:  # 阈值：1-10,眨眼
            blink_times += 1

        # 如果连续10次都小于阈值，则表示进行了一次闭眼活动
        if eye_conti_frames >= step_frames:  # 阈值：10，闭眼
            eye_close_times += 1  # 周期内闭眼总次数
            # 周期内连续闭眼总帧数
            eye_close_frames += eye_conti_frames

        # ear大于阈值,重置眼帧计数器
        eye_conti_frames = 0
    return ear, eye_conti_frames, step_frames, blink_times, eye_close_times, eye_close_frames

# 嘴部参数
def mouth_params(mar, mouth_conti_frames, step_frames, yawn_times):
    '''
        计算张嘴评分，如果小于阈值，则加1，如果连续3次都小于阈值，则表示打了一次哈欠，同一次哈欠大约在3帧
    '''
    if mar > 0.6:  # 张嘴阈值0.6
        mouth_conti_frames += 1
        # cv2.putText(frame, "Yawning!", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    else:
        # 如果连续10次都小于阈值，则表示打了一次哈欠
        if mouth_conti_frames >= step_frames:  # 阈值：10
            yawn_times += 1
        # 嘴巴mar大于阈值,重置嘴帧计数器
        mouth_conti_frames = 0
    return mar, mouth_conti_frames, step_frames, yawn_times

# 获取疲劳度
def get_fatigue(blink_freq, yawn_freq, perclose, eye_close_times):
    '''
        综合眨眼评分和张嘴评分，由眨眼频率、打哈欠频率、闭眼时长和闭眼次数计算疲劳程度评分
    '''
    fatigue = 1/2.6 * float((0.3 * (2 * abs(float(blink_freq) - 0.5)) + 0.5 * float(yawn_freq) +
                               float(perclose) + 0.8 * float(eye_close_times)))
    return round(fatigue,2)

# 获取疲劳等级
def get_fatigue_grade(fatigue):
    # 确定疲劳等级提示:小于0.15为清醒，0.15-0.35临界状态，0.35-0.5轻度疲劳，0.5-0.6中度疲劳，大于0.6重度疲劳
    if fatigue < 0.15:
        fatigue_grade = 1
    elif fatigue >= 0.15 and fatigue < 0.35:
        fatigue_grade = 2
    elif fatigue >= 0.35 and fatigue < 0.5:
        fatigue_grade =3
    elif fatigue >= 0.5 and fatigue < 0.6:
        fatigue_grade =4
    else:  # elif fatigue >= 0.6:
        fatigue_grade =5
    return fatigue_grade

# 添加文字
def add_text(frame,eye_conti_frames,ear,blink_times,blink_freq,mouth_conti_frames,mar,yawn_times,
             yawn_freq,eye_close_times,perclose,rects,frame_counter,fatigue,fatigue_grade):
    cv2.putText(frame, "Press 'ESC': Quit", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (84, 255, 159), 2)
    cv2.putText(frame, "COUNTER: {}".format(eye_conti_frames), (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame, "EAR: {:.2f}".format(ear), (170, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame, "Blinks: {}".format(blink_times), (320, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    cv2.putText(frame, "eFre: {}".format(blink_freq), (470, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    cv2.putText(frame, "COUNTER: {}".format(mouth_conti_frames), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255),2)
    cv2.putText(frame, "MAR: {:.2f}".format(mar), (170, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame, "Yawning: {}".format(yawn_times), (320, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    cv2.putText(frame, "mFre: {}".format(yawn_freq), (470, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    cv2.putText(frame, "Close: {}".format(eye_close_times), (320, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    cv2.putText(frame, "Perclose: {}".format(perclose), (470, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    cv2.putText(frame, "Faces: {}".format(len(rects)), (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame, f"frame_counter:{frame_counter}", (170, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.putText(frame, "Fatigue: {}".format(fatigue), (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    fatigue_dict = {1: "Clear", 2: "Critical state", 3: 'Mild fatigue', 4: 'Moderate fatigue', 5: 'Severe fatigue'}
    cv2.putText(frame, f'{fatigue_dict[fatigue_grade]}', (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)




# 参数初始化
period_frames = 100  # 1000帧为一个周期
step_frames = 10  # 10帧为一个检测步长
frame_counter = 0  # 帧计数器
# 初始化疲劳评分
fatigue = 0
fatigue_grade = 1
# 初始化帧计数器和眨眼总数、闭眼总次数、perclose
eye_conti_frames = 0  # 眼睛长宽比小于阈值的连续帧数
blink_times = 0  # 周期内眨眼总次数
eye_close_times = 0  # 闭眼总次数
perclose = 0
# 初始化帧计数器和打哈欠总数
mouth_conti_frames = 0  # 嘴巴纵横比大于阈值的连续帧数
yawn_times = 0  # 周期内打哈欠总数
# 初始化闭眼时长、眨眼频率、和打哈欠频率
eye_close_frames = 0  # 周期内连续闭眼总帧数
blink_freq = 0  # 眨眼频率
yawn_freq = 0  # 打哈欠频率

if __name__ == '__main__':
    # 第四步：打开cv2 本地摄像头
    cap = cv2.VideoCapture(0)
    while True:
        frame_counter += 1
        # 第五步：进行循环，读取图片，并对图片做维度扩大，并进灰度化
        ret, frame = cap.read()
        # frame = imutils.resize(frame, width=720)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 第六步：使用detector(gray, 0) 进行脸部位置检测
        rects = detector(gray, 0)
        # 第七步：循环脸部位置信息，使用predictor(gray, rect)获得脸部特征位置的信息
        if rects:
            for rect in rects:
                # 计算ear,mar
                ear, mar = ear_mar(gray, rect)
                # 第十三步：循环，满足条件的，眨眼次数+1
                ear, eye_conti_frames, step_frames, blink_times, eye_close_times, eye_close_frames = eye_params(ear, \
                        eye_conti_frames, step_frames,  blink_times,eye_close_times,   eye_close_frames)

                # 眨眼频率
                blink_freq = blink_times / period_frames
                # perclose
                perclose = eye_close_frames / period_frames
                # 同理，判断是否打哈欠
                mar, mouth_conti_frames, step_frames, yawn_times = mouth_params(mar, mouth_conti_frames, step_frames,
                                                                                yawn_times)
                # 打哈欠频率
                yawn_freq = yawn_times / period_frames
                # 疲劳得分
                fatigue = get_fatigue(blink_freq, yawn_freq, perclose, eye_close_times)
                # 疲劳等级
                fatigue_grade = get_fatigue_grade(fatigue)
                # 添加文字
                add_text(frame, eye_conti_frames, ear, blink_times, blink_freq, mouth_conti_frames, mar, yawn_times,
                         yawn_freq, eye_close_times, perclose, rects, frame_counter, fatigue, fatigue_grade)


        if frame_counter == period_frames:  # 一个计数周期结束
            # 进入下一个周期,参数初始化
            period_frames = 100  # 1000帧为一个周期
            step_frames = 10  # 10帧为一个检测步长
            frame_counter = 0  # 帧计数器
            # 初始化疲劳评分
            fatigue = 0
            fatigue_grade = 'None'
            # 初始化帧计数器和眨眼总数、闭眼总次数、perclose
            eye_conti_frames = 0  # 眼睛长宽比小于阈值的连续帧数
            blink_times = 0  # 周期内眨眼总次数
            eye_close_times = 0  # 闭眼总次数
            perclose = 0
            # 初始化帧计数器和打哈欠总数
            mouth_conti_frames = 0  # 嘴巴纵横比大于阈值的连续帧数
            yawn_times = 0  # 周期内打哈欠总数
            # 初始化闭眼时长、眨眼频率、和打哈欠频率
            eye_close_frames = 0  # 周期内连续闭眼总帧数
            blink_freq = 0  # 眨眼频率
            yawn_freq = 0  # 打哈欠频率

        # 窗口显示 show with opencv
        cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
        cv2.imshow("Frame", frame)
        # if the `ESC` key was pressed, break from the loop
        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            cap.release()
            break















