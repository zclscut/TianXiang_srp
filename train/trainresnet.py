from time import *
import os
import cv2
import keras.utils.np_utils

os.environ["TF_CPP_MIN_LOG_LEVEL"]='3'
import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from resnet import resnet18
from tensorflow.keras import datasets,layers,optimizers,Sequential,metrics


#from IPython.display import SVG
#from keras.utils.vis_utils import model_to_dot
#from keras.utils import plot_model


os.environ["TF_CPP_MIN_LOG_LEVEL"]='3'
tf.random.set_seed(2345)
def preprocess(x,y):    #转换数据格式 
    x=2*tf.cast(x,dtype=tf.float32)/255.-1
    y=tf.cast(y,dtype=tf.int32)
    return x,y
def timechange(t):   #把时间改成时分秒制
    d=t//(24*3600)
    h=t%(24*3600)//3600
    m=t%3600//60
    s=t%60
    ss=t%1*100
    blank=' '
    if t>=3600*24:
        print('\n运行时间为:{:0>2.0f}天{:0>2.0f}时{:0>2.0f}分{:0>2.0f}秒{:0>2.0f}'.format(d,h,m,s,ss))
    elif t>=3600:
        print('\n运行时间为:'+blank*4+'{:0>2.0f}时{:0>2.0f}分{:0>2.0f}秒{:0>2.0f}'.format(h,m,s,ss))
    elif t>=60:
        print('\n运行时间为:'+blank*8+'{:0>2.0f}分{:0>2.0f}秒{:0>2.0f}'.format(m,s,ss))
    else:
        print('\n运行时间为:'+blank*12+'{:0>2.0f}秒{:0>2.0f}'.format(s,ss))

data=pd.read_csv('../lib/fer2013.csv')
emotion=data['emotion']
pixels=data['pixels']
usage=data['Usage']

x_train,y_train,x_test,y_test,x_val,y_val=[],[],[],[],[],[]
for i in range(len(data)):
    face=list(map(int,pixels[i].split(' ')))
    face=np.array(face).reshape(48,48,1)#单个训练样本必须是三维的
    label=keras.utils.np_utils.to_categorical(emotion[i],7)#把一个情绪标签转为，7维的one-hot编码,匹配损失函数categorical_crossentropy
    if usage[i]=='Training':
        x_train.append(face)
        y_train.append(label)
    elif usage[i]=='PrivateTest':
        x_val.append(face)
        y_val.append(label)
    elif usage[i]=='PublicTest':
        x_test.append(face)
        y_test.append(label)
#把列表转化为array，神经网络输入必须为array
x_train=np.array(x_train)
y_train=np.array(y_train)
print(y_train)
y_train=y_train.reshape(-1,7)
print(y_train)
x_val=np.array(x_val)
y_val=np.array(y_val)
x_test=np.array(x_test)
y_test=np.array(y_test)

def train():
    model=resnet18()
    model.build(input_shape=(None,48,48,1))#子类resnet18继承了父类keras.Model的方法
    #model.summary()

    #画出神经网络架构
    #SVG(model_to_dot(model, show_shapes=True, dpi=60).create(prog='dot', format='svg'))
    #plot_model(model, show_shapes=True, to_file='model.png')


    epoch_times=eval(input('\n请输入训练次数:'))
    start=time()

    adam=optimizers.Adam(learning_rate=1e-3)
    model.compile(optimizer=adam,loss='categorical_crossentropy',metrics=['accuracy'])#设置损失函数
    his=model.fit(x_train,y_train,batch_size=128,epochs=epoch_times,validation_data=(x_val,y_val))#开始训练
    print('\n模型测试中......')
    test_loss, test_acc = model.evaluate(x_test, y_test)
    end=time()
    timechange(end-start)
    x=np.arange(1,epoch_times+1,1)
    y=np.array(his.history["loss"])
    z=np.array(his.history["accuracy"])
    '''
    plt.figure()
    plt.plot(x,y,color='r',linewidth=1)
    plt.xlabel('epochs')
    plt.ylabel('loss')
    plt.title('loss-epochs')
    '''
    plt.figure()
    plt.plot(x,z,color='r',linewidth=1)
    plt.title('accuracy-epochs')
    plt.xlabel('epochs')
    plt.ylabel('accuracy')
    plt.show()


    issave=eval(input('输入1保存模型，输入0跳过：'))
    if issave:
        percent = str(100 * test_acc)[0:5]  # 98.54333取98.54
        model.save('fer2013_' + percent + '%_resnet.h5')
        #调用类的训练只可以保存参数，不可以保存模型，预测时可以用load_weights载入已训练模型
        #https://blog.csdn.net/yeziand01/article/details/106403780
        #导出tf格式教程
        #https://www.codenong.com/cs105357938/

def fer2013image(i):
    #print(type(pixels[0]))#是单个字符串，用空格分割每个数据
    #map()函数的原型是map(function, iterable,……)，它的结果是返回一个列表，
    #这个函数的意义是将function应用于iterable的每一个元素，结果以列表的形式返回
    image=list(map(int,pixels[i].split(' ')))#把一个长字符分割后转化为int列表
    image=np.array(image).reshape(48,48)
    print(image.shape)
    plt.imshow(image)#图像化处理
    plt.show()#显示图像

run=1
while run:    
    if __name__ == '__main__':
        #train()
        fer2013image(5)
    run=eval(input('请输入1以继续，输入0以终止程序：'))
