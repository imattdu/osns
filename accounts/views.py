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
    User.save_user(user)
    return make_response(jsonify(user.serialize()), 200)


@accounts.route('/update',methods=['POST'])
@cross_origin(origins='*', supports_credentials=True)
def update_nickname():
    param_user = request.get_json(silent=True)
    # 字典不可以使用param_user.id
    data_user = User.get_user_by_id(id=param_user.get('id'));
    data_user.nickname = param_user['nickname'];
    User.save_user(user=data_user)
    return make_response(jsonify(data_user.serialize()), 200)

@accounts.route('/login', methods=['POST'])
@cross_origin(origins='*', supports_credentials=True)
def login():
    param_user = request.get_json(silent=True)
    username = param_user.get('username')
    password = param_user.get('password')
    print(username)
    user = User.get_user(username, password)

    if user != None:
        session.setdefault("LOGIN", user.id)
        user_dict = user.serialize()
        user_dict.setdefault('res', 'success')
        print(session)
        return make_response(jsonify(user_dict), 200)
    res = {'res': 'error'}
    return make_response(res, 200)


@accounts.route('/quit', methods=['POST'])
@cross_origin(origins='*', supports_credentials=True)
def quit():
    param_user = request.get_json(silent=True)
    session.pop('LOGIN', None)
    res = {'res': 'success'}
    return make_response(res, 200)

@accounts.route('/user/list', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def list_user():
    param_user_id = request.args.get('uid')
    user_list = User.list_user()
    res_user_list = []

    for user in user_list:
        if int(user.id) != int(param_user_id):
            res_user = user.serialize()
            res_user_list.append(res_user)

    return jsonify(user_list=[i for i in res_user_list])