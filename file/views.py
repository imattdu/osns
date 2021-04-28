import os

from flask import Blueprint, jsonify, request, flash, redirect, app, url_for
from flask_cors import cross_origin
from werkzeug.utils import secure_filename

from models import Note, db

file = Blueprint('file', __name__)

UPLOAD_PATH = os.path.join(os.path.dirname(__file__),'../static/')


@file.route('/', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def remove_note_by_id():
    return 'hello word'



@file.route('/upload', methods=['POST'])
@cross_origin(origins='*', supports_credentials=True)
def process():
    desc = request.form.get('desc')
    # 获取pichead文件对象
    pichead = request.files.get('pichead')
    print(desc)
    # 保存到服务器
    # save方法传完整的路径和文件名
    pichead.save(os.path.join(UPLOAD_PATH,pichead.filename))
    # 上行可以进行优化,下行是对pichead文件名进行包装，保证文件名更安全。
    # filename = secure_filename(pichead.filename)
    # pichead.save(os.path.join(UPLOAD_PATH, filename))
    return '文件上传成功'
