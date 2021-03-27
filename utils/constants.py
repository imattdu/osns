""" 常量配置 """
from enum import Enum


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
