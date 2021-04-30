""" 常量配置 """
from enum import Enum


class ResCode(Enum):
    PARAM_ERROR = 1001

    USER_SUCCESS = 2000
    USER_EXISTS = 2001
    USER_NOT_EXISTS = 2002
    USER_USERNAME_PASSWORD_DISPATCH = 2003
    USER_PROFILE_SUCCESS = 2100
    USER_PROFILE_NOT_EXISTS = 2101
    USER_LOGIN_INFO_SUCCESS = 2200

    NOTE_SUCCESS = 3000
    NOTE_DELETE_SUCCESS=3100
    NOTE_TAG_SUCCESS = 3200
    NOTE_FORWARD_SUCCESS = 3200


class UserStatus(Enum):
    """ 用户状态 """
    # 启用，可以登录系统
    USER_ACTIVE = 1
    # 禁用，不能登录系统
    USER_IN_ACTIVE = 0


class UserRole(Enum):
    """ 用户的角色 """
    # 普通用户，可以使用前台功能
    COMMON = 0
    # 管理员用户，可以使用后台管理功能
    ADMIN = 1
    # 超级管理员用户，可以删除敏感数据，如用户等
    SUPER_ADMIN = 2

