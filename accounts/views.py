import datetime
import json
import pickle

from flask import Blueprint, request, make_response, session, jsonify
from flask_cors import *
from models import User, UserProfile, UserLoginHistory
from app import db
from utils.constants import ResCode
from utils.res import Res

accounts = Blueprint('accounts', __name__)

"""用户注册"""
@accounts.route('/reg',methods=['POST'])
@cross_origin(origins='*', supports_credentials=True)
def reg():
    param_user = request.get_json(silent=True)

    if param_user == None:
        return jsonify(Res.error(ResCode.PARAM_ERROR.value, '参数错误',{}))
    username = param_user.get('username')
    user = User.get_user_by_username(param_user.get('username'))
    if user != None:
        return jsonify(Res.error(ResCode.USER_EXISTS.value, '用户已经存在',{}))
    user = User()
    user.username = param_user.get('username')
    user.nickname = param_user.get('nickname')
    user.password = param_user.get('password')
    User.save_user(user)
    return jsonify(Res.ok(ResCode.USER_SUCCESS.value, '注册成功',{}))

"""用户登录"""
@accounts.route('/login', methods=['POST'])
@cross_origin(origins='*', supports_credentials=True)
def login():
    param_user = request.get_json(silent=True)
    username = param_user.get('username')
    password = param_user.get('password')
    print(username)
    user = User.get_user(username, password)

    if user != None:
        session.pop('LOGIN', None)
        session.setdefault("LOGIN", user.id)
        user_dict = user.serialize()
        user_dict.pop('password')
        user_dict.setdefault('res', 'success')
        print(session)

        # 记录登录历史
        ip = request.remote_addr
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        ua = request.user_agent.string
        start = ua.find('(')
        end = ua.find(')')
        if start != -1 and end !=-1:
            ua = ua[start+1:end]
        user_login_history = UserLoginHistory(username=user.username,
                                                login_type='',
                                                ip=ip,
                                                ua=ua,
                                                user_id=user.id)

        UserLoginHistory.save_user_login_history(user_login_history)
        # .value 不然提示没有序列化
        return make_response(jsonify(Res.ok(ResCode.USER_SUCCESS.value, "登录成功", user_dict)), 200)
    res = {'res': 'error'}
    return make_response(jsonify(Res.error(ResCode.USER_USERNAME_PASSWORD_DISPATCH.value,
                                           "用户名密码不匹配", {})), 200)

"""用户退出"""
@accounts.route('/quit', methods=['POST'])
@cross_origin(origins='*', supports_credentials=True)
def quit():
    param_user = request.get_json(silent=True)
    session.pop('LOGIN', None)
    res = {'res': 'success'}
    return make_response(Res.ok(ResCode.USER_SUCCESS.value, '退出系统',{}), 200)

"""更新用户信息"""
@accounts.route('/update',methods=['POST'])
@cross_origin(origins='*', supports_credentials=True)
def update_nickname():
    param_user = request.get_json(silent=True)
    # 字典不可以使用param_user.id
    data_user = User.get_user_by_id(id=param_user.get('id'))
    data_user.nickname = param_user['nickname']
    data_user.avatar = param_user['avatar']
    data_user.is_super = param_user['is_super']
    User.save_user(user=data_user)
    res_user = data_user.serialize()
    return make_response(jsonify(Res.ok(ResCode.USER_SUCCESS.value, '', res_user)), 200)

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

"""根据uid获取用户信息"""
@accounts.route('/user/person',methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def get_person_by_uid():
    param_user_id = request.args.get('uid')
    user = User.get_user_by_id(param_user_id)
    user_profile = UserProfile.get_user_profile_by_uid(param_user_id)

    res_user = user.serialize()
    if user_profile != None:
        res_user.update(user_profile.serialize())

    return make_response(jsonify(Res.ok(ResCode.USER_SUCCESS.value,
                                        '',
                                        res_user)), 200)


"""获取用户详细信息"""
@accounts.route('/user/profile/<uid>', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def get_user_profile(uid):
    userprofile = UserProfile.get_user_profile_by_uid(uid=uid)
    if userprofile == None:
        return make_response(Res.ok(ResCode.USER_PROFILE_NOT_EXISTS.value,
                                       '用户属性不存在', {}), 200)
    return make_response(Res.ok(ResCode.USER_PROFILE_SUCCESS.value,
                                       '', userprofile.serialize()), 200)

"""更改用户详细信息"""
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
    return make_response(Res.ok(ResCode.USER_PROFILE_SUCCESS.value,
                                '更新成功',
                                {}), 200)





"""获取登录历史"""
@accounts.route('/user/login/history/<uid>', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def get_user_login_history(uid):
    data_user_login_history_list = UserLoginHistory.list_user_login_history_by_uid(uid=uid)
    res_data = []
    data_user_login_history_list = list(data_user_login_history_list)
    print(data_user_login_history_list)
    if len(data_user_login_history_list) > 7:
        # 0:7 必须紧挨着写
        data_user_login_history_list = data_user_login_history_list[0:7]
    for i in data_user_login_history_list:
        i = i.serialize()
        content = '用户@' + i.get('username') + '在 ip 为' +i.get('ip') + '使用' + i.get('ua')  + '登录了系统'
        e_data = {
            'content': content,
            'timestamp': i.get('created_at')
        }
        res_data.append(e_data)

    return Res.ok(ResCode.USER_SUCCESS.value, '成功', res_data)
