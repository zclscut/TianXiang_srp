import pymysql
from configparser import ConfigParser
import logging
from database import original_event_counter,doSql
import datetime


# log = logging.getLogger()
# log.setLevel(logging.DEBUG)
# # create formatter and add it to the handlers
# fmt = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s"
# datefmt="%a, %d %b %Y %H:%M:%S"
# formatter = logging.Formatter(fmt,datefmt)
# # create file handler which logs even debug messages
# fh = logging.FileHandler('student.log')
# fh.setLevel(logging.DEBUG)
# fh.setFormatter(formatter)
# log.addHandler(fh)
# log.info('在tensorflow下测试')

counter = original_event_counter()  # 查询original_event表中现有数据行数
print('数据表长度为:{}行'.format(counter))
emoFlag=3
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
emotion_sql = f'''
                use online_learning;
                insert into original_event values({counter + 1},1538484710,1,{emoFlag},'{now}');
                '''
doSql(emotion_sql, option='others')


