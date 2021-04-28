import json
import pickle

from flask import Blueprint, request, make_response, session, jsonify
from flask_cors import *
from models import User, UserProfile
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
    data_user = User.get_user_by_id(id=param_user.get('id'))
    data_user.nickname = param_user['nickname']
    data_user.avatar = param_user['avatar']
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


@accounts.route('/userprofile/<uid>', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def get_user_profile(uid):
    userprofile = UserProfile.get_user_profile_by_uid(uid=uid)
    if userprofile == None:
        return make_response({}, 200)
    return make_response(userprofile.serialize(), 200)

@accounts.route('/userprofile', methods=['PUT'])
@cross_origin(origins='*', supports_credentials=True)
def update_user_profile():
    param_userprofile = request.get_json(silent=True)
    data_userprofile = UserProfile.get_user_profile_by_uid(param_userprofile.get('user_id'))
    print(data_userprofile)
    res_userprofile = UserProfile(real_name=param_userprofile.get('real_name'),
                                  sex=param_userprofile.get('sex'),
                                  maxim=param_userprofile.get('maxim'),
                                  address=param_userprofile.get('address'),
                                  user_id=param_userprofile.get('user_id'))
    if data_userprofile == None:
        UserProfile.update_user_profile(res_userprofile)
    else:
        # print(data_userprofile)
        data_userprofile.real_name = param_userprofile.get('real_name'),
        data_userprofile.sex = param_userprofile.get('sex'),
        data_userprofile.maxim = param_userprofile.get('maxim'),
        data_userprofile.address = param_userprofile.get('address'),
        data_userprofile.user_id = param_userprofile.get('user_id')
        UserProfile.update_user_profile(data_userprofile)
    return make_response({}, 200)


