import json
from datetime import datetime

from flask import jsonify, session
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
            'created_at': self.created_at
        }
        return jsonify(data)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'password': self.password,
            'avatar': self.avatar,
            'status': self.status,
            'is_super': self.is_super,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }

    @staticmethod
    def save_user(user):
        """添加用户"""
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def get_user(username, password):
        """查找用户"""
        user = User.query.filter_by(username=username, password=password).first()
        return user

    @staticmethod
    def get_user_by_id(id):
        """查找用户"""
        user = User.query.filter_by(id=id).first()
        return user

    @staticmethod
    def list_user():
        """查找用户"""
        user_list = User.query.filter_by().all()
        return user_list


class UserLoginHistory(db.Model):
    """ 用户模型 """
    __tablename__ = 'accounts_login_history'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    # 用户名，用于登录
    username = db.Column(db.String(64))
    login_type = db.Column(db.String(64))
    ip = db.Column(db.String(64))
    ua = db.Column(db.String(64))

    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 关联用户
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 建立用户的一对一关系属性user.note_list  note.user
    user = db.relationship('User', backref=db.backref('login_history', lazy='dynamic'))



class UserProfile(db.Model):
    """ 用户模型 """
    __tablename__ = 'accounts_user_profile'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    #
    real_name = db.Column(db.String(64))
    # 用户昵称
    sex = db.Column(db.String(1))
    maxim = db.Column(db.String(256))
    address = db.Column(db.String(256))

    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 最后修改的时间
    updated_at = db.Column(db.DateTime,
                           default=datetime.now, onupdate=datetime.now)
    # 关联用户
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 建立用户的一对一关系属性user.note_list  note.user
    user = db.relationship('User', backref=db.backref('profile', lazy='dynamic'))


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
    view_count = db.Column(db.Integer, default=1)

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
            'created_at': self.created_at.strftime('%Y-%m-%d'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d'),
            'user_id': self.user_id,
        }

    @staticmethod
    def save_note(note):
        db.session.add(note)
        db.session.commit()

    @staticmethod
    def get_note_by_id(id):
        note = Note.query.filter_by(id=id).first()
        return note

    @staticmethod
    def update_note(note):
        db.session.add(note)
        db.session.commit()


class NoteForward(db.Model):
    """ 笔记分享 """
    __tablename__ = 'note_note_forward'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    content = db.Column(db.Text)
    is_valid = db.Column(db.SmallInteger, default=1)
    view_count = db.Column(db.String(256), default=1)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 最后修改的时间
    updated_at = db.Column(db.DateTime,
                           default=datetime.now, onupdate=datetime.now)
    # 关联用户
    from_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    to_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    note_id = db.Column(db.Integer, db.ForeignKey('note_note.id'))
    # 建立用户的一对一关系属性user.note_list  note.user
    #user = db.relationship('User', backref=db.backref('note_forward_list', lazy='dynamic'))
    # note = db.relationship('Note', backref=db.backref('note_forward_list', lazy='dynamic'))

    """序列化"""
    def serialize(self):
        return {
            'id': self.id,
            'view_count': self.view_count,
            'content': self.content,
            'is_valid': self.is_valid,
            'created_at': self.created_at.strftime('%Y/%m/%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y/%m/%d %H:%M:%S'),
            'from_id': self.from_id,
            'to_id': self.to_id,
            'note_id': self.note_id
        }



class NoteTag(db.Model):
    """ 笔记分享 """
    __tablename__ = 'note_note_tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    tag_name = db.Column(db.String(128))
    is_valid = db.Column(db.SmallInteger, default=1)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 最后修改的时间
    updated_at = db.Column(db.DateTime,
                           default=datetime.now, onupdate=datetime.now)
    # 关联用户
    note_id = db.Column(db.Integer, db.ForeignKey('note_note.id'))
    # 建立用户的一对一关系属性user.note_list  note.user
    note = db.relationship('Note', backref=db.backref('note_tag_list', lazy='dynamic'))

    """序列化"""
    def serialize(self):
        return {
            'id': self.id,
            'tag_name': self.tag_name,
            'is_valid': self.is_valid,
            'created_at': self.created_at.strftime('%Y/%m/%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y/%m/%d %H:%M:%S'),
            'note_id': self.note_id
        }

    @staticmethod
    def save(tag_name, note_id):
        note_tag = NoteTag()
        note_tag.tag_name = tag_name
        note_tag.note_id = note_id
        db.session.add(note_tag)
        db.session.commit()

    @staticmethod
    def delete_note_tag_by_note_id(note_id):
        note_tag_list = NoteTag.query.filter_by(note_id=note_id).all()
        for note_tag in note_tag_list:
            note_tag.is_valid = 0
            db.session.add(note_tag)
            db.session.commit()

    @staticmethod
    def list_note_tag_by_note_id(note_id):

        note_tag_list = NoteTag.query.filter_by(note_id=note_id, is_valid=1).all()
        return note_tag_list

    @staticmethod
    def list_note_tag():
        note_tag_list = NoteTag.query.filter_by(is_valid=1).all()
        return note_tag_list

    @staticmethod
    def get_note_tag_by_name(tag_name, note_id):
        note_tag = NoteTag.query.filter_by(tag_name=tag_name,note_id=note_id,is_valid=1).first()
        return note_tag





class NoteCollect(db.Model):
    """ 笔记分享 """
    __tablename__ = 'note_note_collect'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    is_valid = db.Column(db.SmallInteger, default=1)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 关联用户
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    note_id = db.Column(db.Integer, db.ForeignKey('note_note.id'))
    # 建立用户的一对一关系属性user.note_list  note.user
    user = db.relationship('User', backref=db.backref('note_collect_list', lazy='dynamic'))
    note = db.relationship('Note', backref=db.backref('note_collect_list', lazy='dynamic'))

    """序列化"""
    def serialize(self):
        return {
            'id': self.id,
            'is_valid': self.is_valid,
            'created_at': self.created_at.strftime('%Y/%m/%d %H:%M:%S'),
            'user_id': self.user_id,
            'note_id': self.note_id
        }