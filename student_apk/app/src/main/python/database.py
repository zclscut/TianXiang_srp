import time
import pymysql
import re
import datetime
from configparser import ConfigParser
import logging

#该方法参考博客https://blog.csdn.net/weixin_45896213/article/details/125600170
class MyConf(ConfigParser):
    def __init__(self,  filename,encoding):
        #初始化父类对象
        super().__init__()
        #读取配置文件，自定义类的构造函数
        self.read(filename, encoding=encoding)



# 参考博客https://blog.csdn.net/u011159607/article/details/79985087
#参考教程https://zhuanlan.zhihu.com/p/425678081
# 设置日志格式
# filemode: 和file函数意义相同，指定日志文件的打开模式，'w'或'a'
log = logging.getLogger()
log.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
fmt = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s"
datefmt="%a, %d %b %Y %H:%M:%S"
formatter = logging.Formatter(fmt,datefmt)
# create file handler which logs even debug messages
fh = logging.FileHandler('student.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
log.addHandler(fh)
log.info('在tensorflow下测试')
# logging.debug("this is debug logger")
# logging.info("this is info logger")
# logging.warning("this is warn logger")
# logging.error("this is error logger")
# logging.critical("this is critical logger")

# 获取与mysql数据库的连接
# 创建连接对象
def connect():
    '''
    获取数据库连接
    :return:
    '''
    db = MyConf("db.ini","utf-8")  # 实例化配置文件对象，读取配置文件



    try:
        # db.get获取字符串，getint获取整形，getboolean获取布尔类型
        connect = pymysql.connect(host=db.get("mysql", "host"),
                    port=db.getint("mysql", "port"),
                    user=db.get("mysql", "user"),  # 用户user
                    # 连接数据库报错https://blog.csdn.net/weixin_45579026/article/details/123148756
                    password=db.get("mysql", "password"),  # 密码
                    database=db.get("mysql", "database"),  # 数据库名称
                    charset=db.get("mysql", "charset")  # 编码方式
                                  )
    except:
        print('数据库连接失败！')
        log.error("failed to connect to {}:{}".format(db.get("mysql", "host"), db.get("mysql", "port")))
    else:
        # print('数据库连接成功！')
        # print(connect)
        #log.info("connecting to the database {}:{} successfully".format(db.get("mysql", "host"), db.get("mysql", "port")))
        #log.info("{}".format(connect))
        return connect


def doSql(sql,option=('query','others')):
    sql_lst = re.findall('(.*?;)', sql) # 转换成多个单行sql
    # print(sql_lst)
    conn = connect()
    cursor = conn.cursor()  # 获取cursor方法
    data_lst=[]
    try:
        for sql in sql_lst:
            cursor.execute(sql)  # 执行sql语句
            conn.commit()  # 必须有此操作才会有结果

            if option == 'query':
                # print(f'查询结果:\n{cursor.fetchall()}')
                data = cursor.fetchall()  # 查询结果
                if data:
                    data_lst.append(data)
            if option == 'others':
                pass
    except:
        print('sql执行出错！')
        log.error('Operating database error!')
    else:
        pass
        # print('sql执行成功！')
        #log.info('Operating database successfully!')
    finally:
        conn.close()
        return data_lst

def original_event_counter(): # original_event的counter查询
    query_sql = f'''
    use online_learning;
    SELECT * FROM original_event ORDER BY counter DESC LIMIT 1;
    '''
    result = doSql(query_sql, option='query')
    if result:
        counter =result[0][0][0]
    else:
        counter = 0
    log.info('After querying,the length of data table equals {}'.format(counter))
    return counter

def study_state_counter(): # study_state的counter查询
    query_sql = f'''
    use online_learning;
    SELECT * FROM study_state ORDER BY counter DESC LIMIT 1;
    '''
    result = doSql(query_sql, option='query')
    if result:
        counter =result[0][0][0]
    else:
        counter = 0
    return counter


# original_event插入单项数据
# eg:event_insert('345', 'emotion', 'hate')
# eg:event_insert('345', 1, 2, 0)
# 如果string=1,则插入输入参数为字符串；如果string=0,则插入输入参数为数字
def event_insert(student_id,event_type,event_value_type,string=1):
    event_key,event_value=0,0
    if string==1:
        sql = f'''select event_key from online_learning.original_event_key where event_type='{event_type}';'''
        event_key = doSql(sql, option='query')#返回三维数组，eg:[(('1',),)]
        print(event_key)
        event_key=event_key[0][0][0]
        print(event_key)
        sql = f'''select event_value from online_learning.original_event_value where event_key={event_key} and event_value_type='{event_value_type}';'''
        event_value = doSql(sql, option='query')#返回三维数组，eg:[(('1',),)]
        print(event_value)
        event_value=event_value[0][0][0]
        print(event_value)
    elif string==0:
        event_key=event_type
        event_value=event_value_type

    # 查询最近一次的value值,防止插入的value值相等
    print('event_key={}'.format(event_key))
    sql = f'''select * from online_learning.original_event where event_key={event_key} order by record_time desc limit 1;'''
    print(sql)
    data = doSql(sql, option='query')
    print(data)
    if data:
        value = data[0][0][3]
        print('value={}'.format(value))
    else:
        value = []
    counter = original_event_counter()  # 查询original_event表中现有数据行数
    if value == [] or (value != str(event_value)):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        emotion_sql = f'''
                use online_learning;
                insert into original_event values({counter + 1},{student_id},{event_key},{event_value},'{now}');
                '''
        doSql(emotion_sql, option='others')


# original_event插入全部数据
def original_event_insert_all(student_id,emotion_sort,is_pitch, is_yaw, is_roll,is_z_gap,is_y_gap_sh,is_y_head_gap,is_per,\
                          is_blink,is_yawn,is_close):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    event_value_lst = [emotion_sort, is_pitch, is_yaw, is_roll, is_z_gap, is_y_gap_sh, is_y_head_gap, is_per,
                       is_blink, is_yawn, is_close]
    event_key_lst = [i for i in range(1, len(event_value_lst) + 1)]
    for event_key, event_value in zip(event_key_lst, event_value_lst):
        # 查询最近一次的value值
        sql = f'''select * from online_learning.original_event where event_key={event_key} order by record_time desc limit 1;'''
        data = doSql(sql, option='query')
        if data:
            value = data[0][0][3]
        else:
            value = []
        counter = original_event_counter()  # 查询original_event表中现有数据行数
        if value == [] or (value != str(event_value)):
            emotion_sql = f'''
            use online_learning;
            insert into original_event values({counter + 1},{student_id},{event_key},{event_value},'{now}');
            '''
            doSql(emotion_sql, option='others')


# study_state插入数据
def study_state_insert_all(student_id,emotion_grade,fatigue_grade,posture_grade,focus_grade):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    state_value_lst=[emotion_grade,fatigue_grade,posture_grade,focus_grade]
    state_key_lst = [i for i in range(1,len(state_value_lst)+1)]
    for state_key,state_value in zip(state_key_lst,state_value_lst):
        # 查询最近一周期的value值
        sql = f'''select * from online_learning.study_state where state_key={state_key} order by record_time desc limit 1;'''
        data = doSql(sql, option='query')
        if data:
            value = data[0][0][3]
        else:
            value = []
        counter = study_state_counter()  # 查询study_state表中现有数据行数
        if value == [] or (value != str(state_value)):
            emotion_sql = f'''
            use online_learning;
            insert into study_state values({counter + 1},{student_id},{state_key},{state_value},'{now}');
            '''
            doSql(emotion_sql, option='others')


# 三表查询指令格式
# 不同表若存在相同的列名,则需要加上表名避免混淆
'''
select 列名 from 表1,表2,表3
where 表1.列名=表2.列名 and 表1或表2.列名=表3.列名
'''

# sql='''
# USE online_learning;
# SELECT student_info.student_id,student_name,record_time FROM student_info,study_state
# WHERE student_info.student_id=1 and study_state.student_id=1;
# '''
# print(excute(sql,option='query'))

# 删除
# sql='''
# use online_learning;
# delete from study_state where state_key>=1;
# '''
# doSql(sql,option='others')

# 插入数据
#now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # datetime类型
# query_sql = f'''
# use online_learning;
# SELECT * FROM study_state ORDER BY counter DESC LIMIT 1;
# '''
# query_result = doSql(query_sql, option='query')
# if query_result:
#     counter = query_result[0][0][0]
#     value=query_result[0][0][3]
# else:
#     counter = 0
#     value=[]
# insert_sql = f'''
# use online_learning;
# INSERT INTO study_state values ({counter + 1}, '1', '1', '1', '{now}');
# '''
# doSql(insert_sql, option='query')




if __name__ == '__main__':
    # connect()
    event_insert('345', 2, 3, 0)
    #event_insert('345', 'emotion', 'hate')


