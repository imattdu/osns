import os


class Config(object):
    """ 项目的配置文件 """
    # 数据库连接URI
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/osns'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # flash, form wtf
    SECRET_KEY = 'abcdsacb12312'
    # 文件上传的根路径
    MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'medias')
