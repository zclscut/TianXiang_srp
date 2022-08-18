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
    '''
    数据库操作
    :param sql: 一行或多行以;结尾的sql语句
    :param option: ’query'为查询,'others'包含增加、删除、修改
    :return:
    '''
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

# 插入指令
now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # datetime类型
# for i in range(1,11):
#     sql = f'''
#     use online_learning;
#     insert into study_state values(1,{i},1,'{now}');
#     '''
#     excute(sql, option='others')

# 删除
# sql='''
# use online_learning;
# delete from study_state where state_key>=1;
# '''
# doSql(sql,option='others')

# 插入数据
# sql = f'''
# use online_learning;
# insert into study_state values(1,1,1,'{now}');
# '''
# doSql(sql, option='others')
