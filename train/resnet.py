import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers,Sequential
#搭建BasicBlock
class BasicBlock(layers.Layer):#括号中是派生的其它基类,类继承用法
    def __init__(self,filter_num,stride=1):
        super(BasicBlock, self).__init__()
        self.conv1=layers.Conv2D(filter_num,(3,3),strides=stride,padding='same')
        self.bn1=layers.BatchNormalization()
        self.relu=layers.Activation('relu')

        self.conv2=layers.Conv2D(filter_num,(3,3),strides=1,padding='same')
        self.bn2 = layers.BatchNormalization()

        if stride!=1:
            self.downsample=Sequential()
            self.downsample.add(layers.Conv2D(filter_num,(1,1),strides=stride))
        else:
            self.downsample=lambda x:x
    def call(self,input,training=None):
        out=self.conv1(input)
        out=self.bn1(out)
        out=self.relu(out)

        out=self.conv2(out)
        out=self.bn2(out)

        identity=self.downsample(input)
        output=layers.add([out,identity])
        output=tf.nn.relu(output)
        return output
#搭建ResNet
class ResNet(keras.Model):#括号中是派生的其它基类,类继承用法
    def __init__(self,layer_dims,num_classes=10):#layer_dims是basicblock层数列表，layer_dims[0]，layer_dims[1]，...对应各层的basicblock数目
        super(ResNet, self).__init__()
        # 预处理层
        
        self.stem1=Sequential([
            layers.Conv2D(8,(5,5),activation=tf.nn.relu),
            layers.MaxPool2D((2,2)),
            layers.Conv2D(32,(5,5),strides=(1,1)),
            layers.Activation('relu'),
            layers.MaxPool2D(pool_size=(2,2),strides=(1,1),padding='same')
        ])
        
        self.stem2=Sequential([
            layers.Conv2D(16,(3,3),activation=tf.nn.relu),
            layers.MaxPool2D((2,2)),
            
        ])
        
        # resblock
        self.layer1=self.build_resblock(64,layer_dims[0],stride=2)
        self.layer2 = self.build_resblock(128, layer_dims[1],stride=2)
        self.layer3 = self.build_resblock(256, layer_dims[2], stride=2)
        self.layer4 = self.build_resblock(512, layer_dims[3], stride=2)

        # there are [b,512,h,w]
        # 自适应
        self.fla=layers.Flatten()
        self.fc1=layers.Dense(1024,activation=tf.nn.relu)
        self.dro=layers.Dropout(0.5)
        self.fc2=layers.Dense(num_classes,activation=tf.nn.softmax)
        self.avgpool=layers.GlobalAvgPool2D()


    def call(self,input,training=None):
        x=self.stem1(input)
        x=self.stem2(x)
        x=self.layer1(x)
        x=self.layer2(x)
        x=self.layer3(x)
        x=self.layer4(x)

        # [b,c]
        x=self.avgpool(x)
        x=self.fla(x)
        x=self.fc1(x)
        x=self.dro(x)
        x=self.fc2(x)
        return x

    def build_resblock(self,filter_num,blocks,stride=1):
        res_blocks= Sequential()
        # may down sample
        res_blocks.add(BasicBlock(filter_num,stride))
        # just down sample one time
        for pre in range(1,blocks):
            res_blocks.add(BasicBlock(filter_num,stride=1))
        return res_blocks
def resnet18():
    return  ResNet([2,2,2,2],num_classes=7)

if __name__ =='__main__':
    model=resnet18()
    print(model.layer1.trainable)
    print(model.stem1.trainable)