# -*- coding: utf-8 -*-
""" 权限 """
from operator import eq
from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    """ Allows access only to super users. """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


def from_attr(attr, expected, **kwargs):
    """ 利用对象的属性生成 permission 类
    """
    base_class = kwargs.pop('base', permissions.BasePermission)
    instanced = kwargs.pop('instanced', None)
    operator = kwargs.pop('operator', eq)

    # pylint: disable=too-few-public-methods,unused-argument,no-self-use
    class AttrPermission(base_class):
        """ 根据属性判断权限 """

        def has_object_permission(self, request, view, obj):
            """ 算子(属性、期望值) """
            return operator(getattr(obj, attr), expected)

    if instanced:
        return AttrPermission()
    return AttrPermission


def from_method(method, *args, **kwargs):
    """ 利用对象类方法生成 permission 类
    """
    base_class = kwargs.pop('base', permissions.BasePermission)
    instanced = kwargs.pop('instanced', None)

    # pylint: disable=too-few-public-methods,unused-argument,no-self-use
    class MethodPermission(base_class):
        """ 使用指定方法判断权限 """

        def has_object_permission(self, request, view, obj):
            """ 根据执行结果判定 """
            return method(obj, *args, **kwargs)

    if instanced:
        return MethodPermission()
    return MethodPermission
