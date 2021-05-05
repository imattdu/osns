import os
import random
import time

from flask import Flask, jsonify, request

import pymysql
from werkzeug.utils import secure_filename

pymysql.install_as_MySQLdb()

from models import db
from accounts.views import accounts
from note.views import note
from file.views import file

# 跨域
from flask_cors import *

app = Flask(__name__, static_folder='static')
# 从配置文件加载配置
app.config.from_object('conf.Config')

# 数据库初始化
db.init_app(app)

# 注册蓝图
app.register_blueprint(accounts, url_prefix='/accounts')
app.register_blueprint(note, url_prefix='/note')
app.register_blueprint(file, url_prefix='/file')

app.config['SECRET_KEY'] = os.urandom(24)

app.config['UPLOAD_FOLDER'] = 'static'

for file in os.listdir(app.config['UPLOAD_FOLDER']):
    print(file)



@app.route('/upload', methods = ['GET', 'POST'])
@cross_origin(origins='*', supports_credentials=True)
def uploader():
   if request.method == 'POST':

        f = request.files['file']
        # print(f.filename)
        # print(secure_filename(f.filename))

        filename = f.filename
        filename_list = str(filename).split('.')
        filename = str(time.time()) + str(random.randint(1, 9)) + '.' + filename_list[1]
        # f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        url = 'http://192.168.96.7:9000/static/' + filename
        return url









