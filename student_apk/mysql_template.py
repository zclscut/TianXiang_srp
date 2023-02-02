import pymysql

def doSQL(sql):
    cursor.execute(sql)
    conn.commit()

conn = pymysql.connect(host='127.0.0.1',
                       user='root',
                       password='123456',
                       database='mysql',
                       charset='UTF8MB4')
cursor = conn.cursor()
# 删除数据库
doSQL('DROP DATABASE IF EXISTS online_learning;')
# 创建数据库
doSQL('CREATE DATABASE IF NOT EXISTS online_learning;')
# 关闭游标和连接
cursor.close()
conn.close()

conn = pymysql.connect(host='127.0.0.1',
                       user='root',
                       password='123456',
                       database='online_learning',
                       charset='UTF8MB4')
cursor = conn.cursor()
# 删除数据表
doSQL('DROP TABLE IF EXISTS questions')
# 创建数据表
sql = '''
CREATE TABLE IF NOT EXISTS questions(
id INT auto_increment PRIMARY KEY,
wenti CHAR(200) NOT NULL UNIQUE,
daan CHAR(50) NOT NULL,
shijian TimeStamp
) ENGINE=innodb DEFAULT CHARSET=UTF8MB4;
'''
doSQL(sql)
# 删除所有数据
doSQL('DELETE FROM questions;')

# 插入数据
for i in range(10):
    sql = 'INSERT INTO questions(wenti,daan) VALUES("测试问题{0}","答案{0}");'.format(i)
    cursor.execute(sql)
conn.commit()

# 修改数据
doSQL('UPDATE questions set daan="被修改了" WHERE wenti="测试问题6";')
# 删除指定的数据
doSQL('DELETE FROM questions WHERE daan="答案8";')
# 查询并输出数据
sql = 'SELECT * FROM questions'
cursor.execute(sql)
for row in cursor.fetchall():
    print(row)

# 关闭游标和连接
cursor.close()
conn.close()
