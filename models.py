import json
from datetime import datetime

from flask import jsonify
from flask_sqlalchemy import SQLAlchemy


from utils import constants
db = SQLAlchemy()

class User(db.Model):
    """ 用户模型 """
    __tablename__ = 'accounts_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    # 用户名，用于登录
    username = db.Column(db.String(64))
    # 用户昵称
    nickname = db.Column(db.String(64))
    password = db.Column(db.String(256))
    # 用户的头像地址
    avatar = db.Column(db.String(256))

    # 是否有效，无效用户将不能登录系统
    status = db.Column(db.SmallInteger,
                       default=constants.UserStatus.USER_ACTIVE.value,
                       comment='用户状态')
    # 是否是超级管理员，管理员可以对所有内容进行管理
    is_super = db.Column(db.SmallInteger,
                         default=constants.UserRole.COMMON.value)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 最后修改的时间
    updated_at = db.Column(db.DateTime,
                           default=datetime.now, onupdate=datetime.now)
    # profile = db.relationship('UserProfile')

    def __init__(self):
        super(User, self).__init__()
        print('hello word')

    def get_objects(self):

        data = {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'created_at': self.created_at,

        }
        return jsonify(data)




class Note(db.Model):
    """ 用户模型 """
    __tablename__ = 'note_note'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    # 标题
    title = db.Column(db.String(128))
    #
    content = db.Column(db.Text)
    is_valid = db.Column(db.SmallInteger, default=1)
    #
    view_count = db.Column(db.String(256), default=1)

    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 最后修改的时间
    updated_at = db.Column(db.DateTime,
                           default=datetime.now, onupdate=datetime.now)
    # 关联用户
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 建立用户的一对一关系属性user.note_list  note.user
    user = db.relationship('User', backref=db.backref('note_list', lazy='dynamic'))

    """序列化"""
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'is_valid': self.is_valid,
            'view_count': self.view_count,
            'created_at': self.created_at.strftime('%Y/%m/%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y/%m/%d %H:%M:%S'),
            'user_id': self.user_id,
        }