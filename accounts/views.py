import json
import pickle

from flask import Blueprint, request, make_response, session, jsonify
from flask_cors import *
from models import User
from app import db
accounts = Blueprint('accounts', __name__)


@accounts.route('/reg',methods=['POST'])
@cross_origin(origins='*', supports_credentials=True)
def reg():
    param_user = request.get_json(silent=True)
    user = User()
    user.username = param_user.get('username')
    user.nickname = param_user.get('nickname')
    user.password = param_user.get('password')
    print(user)
    db.session.add(user)
    db.session.commit()
    s = ['张三', '年龄', '姓名']
    res = user.get_objects()
    return make_response(res, 200)


@accounts.route('/login', methods=['POST'])
@cross_origin(origins='*', supports_credentials=True)
def login():
    param_user = request.get_json(silent=True)
    username = param_user.get('username')
    password = param_user.get('password')
    print(username)
    user = User.query.filter_by(username=username, password=password).first()

    if user != None:
        print(user.get_objects())
        res_data = {
            'id': user.id,
            'nickname': user.nickname,
            'username': user.username,
            'res': 'success'
        }

        session.setdefault("LOGIN", user.id)
        return make_response(jsonify(res_data), 200)
    res = {'res': 'error'}
    return make_response(res, 200)