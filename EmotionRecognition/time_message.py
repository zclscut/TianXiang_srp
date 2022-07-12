from pynput.keyboard import *
from datetime import *
from time import *
def run(string):
    keyboard=Controller()
    keyboard.type(string)
    with keyboard.pressed(Key.ctrl):
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

s="刘莎莎+15348486075+430421200003135147+九价第一针"
t=datetime.now().strftime('%H:%M:%S.%f')

print('程序开始....')
#while t<'12:15:57.800000':
while t<'07:59:57.900000':
    t=datetime.now().strftime('%H:%M:%S.%f')
run(s)
print(datetime.now().strftime('%H:%M:%S.%f'))
print('程序结束。')

'''        
        
print('程序开始....')


while t<'23:14:57.800000':
    t=datetime.now().strftime('%H:%M:%S.%f')
run(s)
print(datetime.now().strftime('%H:%M:%S.%f'))
print('等待再次触发......')

while t<'23:19:57.800000':
    t=datetime.now().strftime('%H:%M:%S.%f')
run(s)
print(datetime.now().strftime('%H:%M:%S.%f'))
print('等待再次触发......')

while t<'23:24:57.800000':
    t=datetime.now().strftime('%H:%M:%S.%f')
run(s)
print(datetime.now().strftime('%H:%M:%S.%f'))
print('等待再次触发......')

while t<'23:29:57.800000':
    t=datetime.now().strftime('%H:%M:%S.%f')
run(s)
print(datetime.now().strftime('%H:%M:%S.%f'))

print('程序结束。')   
    
'''    

        
    
        
        
    
    
    
    
        
    
