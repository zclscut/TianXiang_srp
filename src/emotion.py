import numpy as np
import cv2 as cv
import time
from tensorflow.keras import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array


model=Sequential()#创建神经网络模型，准备调用.h5文件
classifier=load_model('../lib/neuralnetwork.h5')#调用.h5文件,该神经网络能输出6类情绪

#神经网络输出数字标签，需查字典得到情绪类别
emotion_dic={0:'Angry',1:'Fear',2:'Happy',3:'Neutral',4:'Sad',5:'Surprise'}
classes=list(emotion_dic.values())

#所有函数公用对象，识别人脸分类器
face_detector = cv.CascadeClassifier('../lib/haarcascade_frontalface_alt.xml ')

#在框外用文字输出情绪
def text_on_detected_boxes(text,text_x,text_y,image,font_scale = 1,
                           font = cv.FONT_HERSHEY_SIMPLEX,
                           FONT_COLOR = (0, 0, 0),
                           FONT_THICKNESS = 2,
                           rectangle_bgr = (0, 255, 0)):
    # get the width and height of the text box
    (text_width, text_height) = cv.getTextSize(text, font, fontScale=font_scale, thickness=2)[0]
    # Set the Coordinates of the boxes
    box_coords = ((text_x-10, text_y+4), (text_x + text_width+10, text_y - text_height-5))
    # Draw the detected boxes and labels
    cv.rectangle(image, box_coords[0], box_coords[1], rectangle_bgr, cv.FILLED)
    cv.putText(image, text, (text_x, text_y), font, fontScale=font_scale, color=FONT_COLOR,thickness=FONT_THICKNESS)

def face_detector_image(frame):
    allfaces=[]
    rects=[]

    gray=cv.cvtColor(frame,code=cv.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10)
    #没检测到人脸
    if faces == ():
        return (0,0,0,0),np.zeros((48,48),np.uint8),frame
    #检测到人脸，用(0,0,255)红色方框框出来
    for (x, y, w, h) in faces:
        cv.rectangle(frame, pt1=(x, y),
                     pt2=(x + w, y + h),
                     color=[0, 0, 255],
                     thickness=2)
        #截取人脸，压缩后作为神经网络的输入，神经网络输出情绪标签
        roi_gray=gray[y:y+h,x:x+w]
        # 降维，压缩图片，神经网络输入为48*48像素
        roi_gray=cv.resize('roi_gray',(48,48),interpolation=cv.INTER_AREA)
        allfaces.append(roi_gray)#多个人脸的压缩灰度图数组
        rects.append((x,y,w,h))#元素为元组，储存人脸的坐标和长宽
    return rects,allfaces,frame
    #返回人脸矩形参数，压缩人脸灰度图，原图
def emotion_image(image_path):
    img=cv.imread(image_path)
    rects,faces,image=face_detector_image(img)
    i = 0
    for face in faces:
        roi = face.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)#把灰度图转化为narray数组，作为神经网络的输入

        # 调用神经网络预测，用输出的数字标签查询字典，得到情绪的称呼
        preds = classifier.predict(roi)[0]
        label = emotion_dic[preds.argmax()]
        label_position = (rects[i][0] + int((rects[i][1] / 2)), abs(rects[i][2] - 10))
        i = + 1

        # 将情绪文字标注在方框外，对image进行修饰
        text_on_detected_boxes(label, label_position[0], label_position[1], image)

    cv.imshow("Emotion Detector", image)
    cv.waitKey(0)
    cv.destroyAllWindows()
def face_detector_video(img):
    # Convert image to grayscale
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    t = time.time()#测试执行时间
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10)
    #caleFactor=1.1, minNeighbors=10执行时间110ms
    #caleFactor=1.3, minNeighbors=10执行时间40ms
    print(time.time() - t)#测试执行时间
    # 没检测到人脸
    if faces == ():
        return (0, 0, 0, 0), np.zeros((48, 48), np.uint8), img
    # 检测到人脸，用(0,0,255)红色方框框出来
    for (x, y, w, h) in faces:
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)
        roi_gray = gray[y:y + h, x:x + w]#截取人脸，压缩后作为神经网络的输入，神经网络输出情绪标签

    roi_gray = cv.resize(roi_gray, (48, 48), interpolation=cv.INTER_AREA)

    return (x, w, y, h), roi_gray, img
    # 返回人脸矩形参数，压缩人脸灰度图，原图

def emotion_video(cap):
    while True:
        ret, frame = cap.read()

        rect, face, image = face_detector_video(frame)

        if np.sum([face]) != 0.0:
            #t = time.time()#测试调用神经网络模型预测时间平均60ms
            roi = face.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)#把灰度图转化为narray数组，作为神经网络的输入

            # 调用神经网络预测，用输出的数字标签查询字典，得到情绪的称呼

            preds = classifier.predict(roi)[0]

            label = emotion_dic[preds.argmax()]
            label_position = (rect[0] + rect[1]//50, rect[2] + rect[3]//50)
            text_on_detected_boxes(label, label_position[0], label_position[1], image) # 将情绪文字标注在方框外，对image进行修饰
            fps = cap.get(cv.CAP_PROP_FPS)#获取视频帧率
            cv.putText(image, str(fps),(5, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            #print(1.0 / (time.time() - t))#测试调用神经网络模型预测时间平均60ms
        else:
            cv.putText(image, "No Face Found", (5, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        cv.imshow('all', image)
        if cv.waitKey(1) == 27 or cv.getWindowProperty("all",cv.WND_PROP_AUTOSIZE) != 1:#ESC的ASCII码
            break

    cap.release()
    cv.destroyAllWindows()


def emotionFrameDetect(frame,photo):
    #t = time.time()#测试执行时间
    rect, face, image = face_detector_video(frame)
    #tt = time.time()#测试执行时间
    emoFlag=0
    if np.sum([face]) != 0.0:
        roi = face.astype("float") / 255.0#归一化
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)  # 把灰度图转化为narray数组，作为神经网络的输入

        # 调用神经网络预测，用输出的数字标签查询字典，得到情绪的称呼
        preds = classifier.predict(roi)[0]
        emoFlag=preds.argmax()
        label = emotion_dic[emoFlag]
        label_position = (rect[0] + rect[1] // 50, rect[2] + rect[3] // 50)
        text_on_detected_boxes(label, label_position[0], label_position[1], image)  # 将情绪文字标注在方框外，对image进行修饰
        #fps = cap.get(cv.CAP_PROP_FPS)
        fps=30
        # 获取视频帧率
        cv.putText(image, str(fps), (5, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        cv.putText(image, "No Face Found", (5, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    return emoFlag, image

if __name__ =='__main__':
    camera=cv.VideoCapture(0)#打开摄像头
    emotion_video(camera)#识别人脸并识别情绪