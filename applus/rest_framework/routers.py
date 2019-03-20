# -*- coding: utf-8 -*-
""" 扩展 rest_framework Router 功能
"""
from rest_framework import routers


class Router(routers.DefaultRouter):
    """ register 扩展辅助

    class TestView:
        pass

    router.register(prefix, TestView, ...)

    ==>

    @router.register(prefix, ...)
    class TestView:
        pass
    """

    def register_decorator(self, prefix, *args, **kwargs):
        """ register 辅助装饰器 """
        def decorator(viewset):
            self.register(prefix, viewset, *args, **kwargs)
            return viewset
        return decorator
