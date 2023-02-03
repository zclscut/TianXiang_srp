# -*- coding: utf-8 -*-
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import cv2 as cv
import numpy as np
import datetime
import logging
from emotion import emotionFrameDetect as emotion_detect
from posture import postureFrameDetect as posture_detect
from fatigue_ui import fatigueFrameDetectDraw as fatigue_detect
from concentration import concentrationFrameDetect as concentration_detect
from database import original_event_counter,doSql,event_insert



face_detector = cv.CascadeClassifier('../lib/haarcascade_frontalface_alt.xml ')
def faceDetectorVideo(img):
    # Convert image to grayscale
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    #t = time.time()#测试执行时间
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10)
    #caleFactor=1.1, minNeighbors=10执行时间110ms
    #caleFactor=1.3, minNeighbors=10执行时间40ms
    #print(time.time() - t)#测试执行时间
    # 没检测到人脸
    if faces == ():
        return (0, 0, 0, 0), np.zeros((48, 48), np.uint8), img
    # 检测到人脸，用(0,0,255)红色方框框出来
    for (x, y, w, h) in faces:
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)
        roi_gray = gray[y:y + h, x:x + w]#截取人脸，压缩后作为神经网络的输入，神经网络输出情绪标签

    roi_gray = cv.resize(roi_gray, (48, 48), interpolation=cv.INTER_AREA)

    return (x, w, y, h), roi_gray, gray
    # 返回人脸矩形参数，压缩人脸灰度图


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(634, 492)
        self.actionFile = QAction(MainWindow)
        self.actionFile.setObjectName(u"actionFile")
        self.actionCamera = QAction(MainWindow)
        self.actionCamera.setObjectName(u"actionCamera")
        self.actionContact_Us = QAction(MainWindow)
        self.actionContact_Us.setObjectName(u"actionContact_Us")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.pushButton_3, 0, Qt.AlignHCenter)

        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.pushButton_4, 0, Qt.AlignHCenter)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.pushButton_2, 0, Qt.AlignHCenter)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.pushButton, 0, Qt.AlignHCenter)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.img_label = QLabel(self.centralwidget)
        #self.img_label.setGeometry(QRect(0, 0, 640, 480))
        self.img_label.setObjectName("img_label")



        self.horizontalLayout_2.addWidget(self.img_label)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setEnabled(True)

        self.verticalLayout_3.addWidget(self.label_2, 0, Qt.AlignVCenter)

        self.checkBox_3 = QCheckBox(self.centralwidget)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.verticalLayout_3.addWidget(self.checkBox_3)

        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(u"checkBox")

        self.verticalLayout_3.addWidget(self.checkBox)

        self.checkBox_2 = QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.verticalLayout_3.addWidget(self.checkBox_2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label, 0, Qt.AlignVCenter)

        self.checkBox_6 = QCheckBox(self.centralwidget)
        self.checkBox_6.setObjectName(u"checkBox_6")

        self.verticalLayout_3.addWidget(self.checkBox_6)

        self.checkBox_5 = QCheckBox(self.centralwidget)
        self.checkBox_5.setObjectName(u"checkBox_5")

        self.verticalLayout_3.addWidget(self.checkBox_5)

        self.checkBox_4 = QCheckBox(self.centralwidget)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.verticalLayout_3.addWidget(self.checkBox_4)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 634, 22))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menu.addAction(self.actionFile)
        self.menu.addAction(self.actionCamera)
        self.menu_2.addAction(self.actionContact_Us)

        self.retranslateUi(MainWindow)



        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u5728\u7ebf\u5b66\u4e60\u5206\u6790\u7cfb\u7edf", None))
        self.actionFile.setText(QCoreApplication.translate("MainWindow", u"File", None))
        self.actionCamera.setText(QCoreApplication.translate("MainWindow", u"Camera", None))
        self.actionContact_Us.setText(QCoreApplication.translate("MainWindow", u"Contact Us", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u75b2\u52b3\u5206\u6790", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u59ff\u52bf\u5206\u6790", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u4e13\u6ce8\u5ea6\u5206\u6790", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u60c5\u7eea\u5206\u6790", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u4eba\u8138\u8bc6\u522b", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"\u5173\u952e\u70b9", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"\u6807\u53f7", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"\u4eba\u8138\u8bc6\u522b", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u5b66\u4e60\u72b6\u6001\u5206\u6790", None))
        self.checkBox_6.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u5e27\u6570", None))
        self.checkBox_5.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u6982\u7387", None))
        self.checkBox_4.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u53c2\u6570", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9", None))
    # retranslateUi

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()#调用父类QMainWindow的初始化函数
        # 使用ui文件导入定义界面类
        self.ui = Ui_MainWindow()
        # 初始化界面
        self.ui.setupUi(self)


class MainCode(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.camera=cv.VideoCapture(0)
        self.painter = QPainter(self)
        self.buttonFlag = 0  # 没有按钮按下
        print('reset')
        self.pushButton.clicked.connect(self.xflag)
        self.pushButton_2.clicked.connect(self.xflag_2)
        self.pushButton_3.clicked.connect(self.xflag_3)
        self.pushButton_4.clicked.connect(self.xflag_4)
        self.framecounter=0
        self.framecountermax=100#连续检测1000帧
        self.fatiguedatatuple =(0,0,0,0,0,0,0,0,0,0,0)
        self.scoretuple=(0,0,0,0,0)
        self.concentrationdatatuple=({'Angry': 0, 'Hate': 0, 'Fear': 0, 'Happy': 0, 'Sad': 0, 'Surprise': 0, 'Neutral': 0, },
                                     [],[],[],[],[])
    def xflag(self):
        self.framecounter = 0
        self.fatiguedatatuple = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        print(self.buttonFlag)
        if self.buttonFlag==0:
            self.buttonFlag=1
            #self.pushButton.setText('open1')
        else:
            self.buttonFlag=0
            #self.pushButton.setText('close')
    def xflag_2(self):
        self.framecounter = 0
        self.fatiguedatatuple = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        print(self.buttonFlag)
        if self.buttonFlag==0:
            self.buttonFlag=2
            #self.pushButton_2.setText('open2')
        else:
            self.buttonFlag=0
            #self.pushButton_2.setText('close')
    def xflag_3(self):
        self.framecounter = 0
        self.fatiguedatatuple = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        print(self.buttonFlag)
        if self.buttonFlag==0:
            self.buttonFlag=3
            #self.pushButton_3.setText('open3')
        else:
            self.buttonFlag=0
            #self.pushButton_3.setText('close')
    def xflag_4(self):
        self.framecounter = 0
        self.fatiguedatatuple = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        print(self.buttonFlag)
        if self.buttonFlag==0:
            self.buttonFlag=4
            #self.pushButton_4.setText('open4')


        else:
            self.buttonFlag=0
            #self.pushButton_4.setText('close')

    def paintEvent(self, a0: QPaintEvent):
        ret,frame=self.camera.read()
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.framecounter+=1
        # 疲劳分析需要连续分析1000帧,计算1000帧以内的闭眼时长、眨眼频率、打哈欠频率
        if self.framecounter==self.framecountermax:
            self.framecounter=0
            self.fatiguedatatuple = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            self.concentrationdatatuple=({'Angry': 0, 'Hate': 0, 'Fear': 0, 'Happy': 0, 'Sad': 0, 'Surprise': 0, 'Neutral': 0, },
                                     [],[],[],[],[])
        # 按下情绪识别按钮
        if self.buttonFlag==1:
            rect, roi_gray, gray = faceDetectorVideo(frame)  # 输出人脸矩形坐标，压缩人脸灰度图
            emoFlag, photo = emotion_detect(rect, roi_gray, frame)  # 输入灰度图，输出情绪类别标签emoFlag，并输出情绪识别后用文字标签后的图片
            self.QImage=QImage(photo.data, photo.shape[1], photo.shape[0], photo.shape[1] * 3, QImage.Format_RGB888)
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # counter = original_event_counter()  # 查询original_event表中现有数据行数
            # emotion_sql = f'''
            #             use online_learning;
            #             insert into original_event values({counter + 1},1538484710,2,{emoFlag},'{now}');
            #             '''
            # doSql(emotion_sql, option='others')
            event_insert('13423', 1, emoFlag, 0)

            #log.info("The user zcl write to the database sucessfully")
            #logging.info("the original_event=emotion,original_value={}".format(emoFlag))




        # 按下姿势识别按钮
        elif self.buttonFlag==4:
            headPosture,photo=posture_detect(frame,frame)
            self.QImage = QImage(photo.data, photo.shape[1], photo.shape[0], photo.shape[1] * 3, QImage.Format_RGB888)

            event_insert('13423', 1, headPosture, 0)
            # log.info("The user zcl write to the database successfully")
            #logging.info("the original_event=posture,original_value={}".format(3))

        # 按下疲劳分析按钮
        elif self.buttonFlag==3:
            self.fatiguedatatuple,photo=fatigue_detect(self.fatiguedatatuple,self.framecounter,frame)
            self.QImage = QImage(photo.data, photo.shape[1], photo.shape[0], photo.shape[1] * 3, QImage.Format_RGB888)
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # 查询最近一次的疲劳检测写数据库的值
            sql = f'''select * from online_learning.original_event where event_key=4 order by record_time desc limit 1;'''
            data = doSql(sql, option='query')
            if data:
                value = data[0][0][3]
            else:
                value = []
            if value == [] or (value != '4'):#疲劳检测event_key=4
                counter = original_event_counter()  # 查询original_event表中现有数据行数
                emotion_sql = f'''
                            use online_learning;
                            insert into original_event values({counter + 1},1538484710,2,{headPosture},'{now}');
                            '''
                doSql(emotion_sql, option='others')
                # log.info("The user zcl write to the database successfully")
                # logging.info("the original_event=fatigue,original_value={}".format(3))
        # 按下专注度分析按钮
        elif self.buttonFlag==2:
            self.scoretuple,self.fatiguedatatuple,photo=\
                concentration_detect(self.concentrationdatatuple,self.scoretuple,
                                     self.fatiguedatatuple,self.framecounter,
                                     self.framecountermax,frame)
            self.QImage = QImage(photo.data, photo.shape[1], photo.shape[0], photo.shape[1] * 3, QImage.Format_RGB888)
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            counter = original_event_counter()  # 查询original_event表中现有数据行数
            emotion_sql = f'''
                        use online_learning;
                        insert into original_event values({counter + 1},1538484710,2,{headPosture},'{now}');
                        '''
            doSql(emotion_sql, option='others')
            # log.info("The user zcl write to the database successfully")
            # logging.info("the original_event=concentration,original_value={}".format(3))
        else:
            self.QImage = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)
        self.img_label.setPixmap(QPixmap.fromImage(self.QImage))
        self.update()

app = QApplication([])
mainw = MainCode()
mainw.show()
app.exec_()