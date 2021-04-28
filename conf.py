import os


class Config(object):
    """ 项目的配置文件 """
    # 数据库连接URI
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/osns'
    SQLALCHEMY_TRACK_MODIFICATIONS = True



