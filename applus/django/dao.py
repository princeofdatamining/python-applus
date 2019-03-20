# -*- coding: utf-8 -*-
""" Model/Manager/Queryset utils and lazy """
from functools import partial
from django.conf import settings
from django.apps import apps
from django.utils import functional
from django.utils import module_loading


def get_model(alias):
    """ Model
    """
    if not alias:
        alias = settings.AUTH_USER_MODEL
    return apps.get_model(alias)


def get_dao(alias):
    """ Manager
    """
    return get_model(alias).objects


def get_spec_dao(alias, dao_class_or_namespace):
    """ Manager
    """
    model = get_model(alias)
    if isinstance(dao_class, str):
        dao_class = module_loading.import_string(dao_class_or_namespace)
    else:
        dao_class = dao_class_or_namespace
    dao = dao_class()
    dao.model = model
    return dao


def get_queryset(alias):
    """ Queryset
    """
    return get_dao(alias).all()


def get_lazy_model(alias):
    """ Model(lazy)
    """
    return functional.SimpleLazyObject(partial(get_model, alias))


def get_lazy_dao(alias):
    """ Manager(lazy)
    """
    return functional.SimpleLazyObject(partial(get_dao, alias))


def get_lazy_spec_dao(alias, dao_class):
    """ Manager(lazy)
    """
    return functional.SimpleLazyObject(partial(
        get_spec_dao, alias, dao_class))


def get_lazy_queryset(alias):
    """ Queryset(lazy)
    """
    return functional.SimpleLazyObject(partial(get_queryset, alias))
