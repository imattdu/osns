from flask import Flask

import pymysql
pymysql.install_as_MySQLdb()

from models import db
from accounts.views import accounts
from note.views import note
# 跨域
from flask_cors import *

app = Flask(__name__, static_folder='assets')
# 从配置文件加载配置
app.config.from_object('conf.Config')

# 数据库初始化
db.init_app(app)

# 注册蓝图
app.register_blueprint(accounts, url_prefix='/accounts')
app.register_blueprint(note, url_prefix='/note')







