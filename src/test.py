import pymysql
from configparser import ConfigParser
import logging

#该方法参考博客https://blog.csdn.net/weixin_45896213/article/details/125600170
class MyConf(ConfigParser):
    def __init__(self,  filename):
        #初始化父类对象
        super().__init__()
        #读取配置文件，自定义类的构造函数
        self.read(filename, encoding="utf-8")


if __name__ == '__main__':
    db=MyConf("db.ini")#实例化配置文件对象，读取配置文件


    # 参考博客https://www.cnblogs.com/oktokeep/p/16596457.html
    #设置日志格式
    #filemode: 和file函数意义相同，指定日志文件的打开模式，'w'或'a'
    fmt = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s"
    logging.basicConfig(
        level=logging.DEBUG,
        format=fmt,
        filename="student.log",
        filemode="a",
        datefmt="%a, %d %b %Y %H:%M:%S"
    )
    # logging.debug("this is debug logger")
    # logging.info("this is info logger")
    # logging.warning("this is warn logger")
    # logging.error("this is error logger")
    # logging.critical("this is critical logger")

    try:
    # db.get获取字符串，getint获取整形，getboolean获取布尔类型
        connect = pymysql.connect(host=db.get("mysql", "host"),
            port = db.getint("mysql", "port"),
            user = db.get("mysql", "user"),  # 用户user
            # 连接数据库报错https://blog.csdn.net/weixin_45579026/article/details/123148756
            password = db.get("mysql", "password"),  # 密码
            database = db.get("mysql", "database"),  # 数据库名称
            charset = db.get("mysql", "charset")  # 编码方式
                              )
    except:
        print('数据库连接失败！')
        logging.error("数据库连接失败！")
    else:
        print('数据库连接成功！')
        print(connect)
        logging.info("数据库连接成功！")
        logging.info("{}".format(connect))




