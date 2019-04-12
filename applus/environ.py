# -*- coding: utf-8 -*-
""" 环境配置相关功能 """
import os
import urllib


def get_envfunc(prefix=""):
    """ 允许指定配置前缀 """
    def wrapper(key, default, func=None):
        """ 读取环境配置并处理，支持默认值 """
        env_key = prefix + key
        if env_key not in os.environ:
            return default
        env_val = os.environ.get(env_key)
        if not func:
            return env_val
        if func is bool:
            return env_val.lower() in ["true"]
        return func(env_val)
    return wrapper


def decode_result(result, method='unquote'):
    """ 转义处理 """
    if not result or method is None:
        return result
    return urllib.parse.unquote(result)


def parse_uri(uri, **defaults):
    """ uri 解析 """
    result = urllib.parse.urlparse(uri)
    return {
        "scheme": result.scheme,
        "username": result.username or defaults.get("username"),
        "password": decode_result(result.password) or defaults.get("password"),
        "netloc": result.netloc,
        "hostname": result.hostname or defaults.get("hostname"),
        "port": result.port or defaults.get("port"),
        "path": result.path,
        "query": result.query,
        "queries": urllib.parse.parse_qs(result.query, keep_blank_values=True),
        "params": result.params,
        "fragment": result.fragment,
    }


def merge_uri(parsed, **kwargs):
    """ uri 替换 """
    return urllib.parse.urlunparse(urllib.parse.ParseResult(
        scheme=kwargs.get("scheme", parsed["scheme"]),
        netloc=kwargs.get("netloc", parsed["netloc"]),
        path=kwargs.get("path", parsed["path"]),
        query=kwargs.get("query", parsed["query"]),
        params=kwargs.get("params", parsed["params"]),
        fragment=kwargs.get("fragment", parsed["fragment"]),
    ))


def update_django_db(databases, alias, uri, **default_db_values):
    """ django settings DATABASES """
    if not uri:
        return
    parsed = parse_uri(uri, **default_db_values)
    databases[alias] = {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': parsed['hostname'],
        'PORT': parsed['port'],
        'USER': parsed['username'],
        'PASSWORD': parsed['password'],
        'NAME': parsed['path'].split('/')[1],
        'OPTIONS': {
            'charset': parsed['queries'].get('charset', ['utf8'])[0],
            'sql_mode': default_db_values['sql_mode'],
        },
        'TEST': {
            'charset': parsed['queries'].get('charset', ['utf8'])[0],
            'sql_mode': default_db_values['sql_mode'],
        },
    }
