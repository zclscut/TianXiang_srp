# 测试本地数据库online_learning
# ip:127.0.0.1或localhost
# user:root
# password:123456
# charset:utf8
import time

import pymysql
import re
import datetime

# 获取与mysql数据库的连接
# 创建连接对象
def connect():
    '''
    获取数据库连接
    :return:
    '''
    try:
     connect = pymysql.connect(
        host='127.0.0.1', # localhost
        user='root', # 用户user
        password='123456', # 密码
        database='online_learning',  # 数据库名称
        charset='utf8',)  # 注意编码方式
    except:
        print('数据库链接失败！')
    else:
        # print('数据库链接成功！')
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


# original_event插入数据
def original_event_insert(student_id,emotion_sort,is_pitch, is_yaw, is_roll,is_z_gap,is_y_gap_sh,is_y_head_gap,is_per,\
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
def study_state_insert(student_id,emotion_grade,fatigue_grade,posture_grade,focus_grade):
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
now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # datetime类型
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






