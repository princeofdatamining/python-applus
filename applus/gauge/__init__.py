""" getgauge 扩展 """
from django.utils.functional import cached_property


class AccessDict(dict):
    """ 属性获取 """

    def __getattr__(self, attr, *args):
        if not args:
            return self[attr]
        return self.get(attr, args[0])


class User:
    """ User

    user = User(data_store.spec, USERNAME)

    user.save_cookie(resp, 'sessionid')
    user.cookies.sessionid

    user.save_token(content, 'token', 'key')
    user.tokens.token

    user.fill_cookie('sessionid', cookies={})
    """

    def __new__(cls, container, user):
        if hasattr(container, user):
            return getattr(container, user)
        instance = super().__new__(cls)
        setattr(container, user, instance)
        return instance

    def __init__(self, container, user):
        pass

    # pylint: disable=no-self-use
    @cached_property
    def cookies(self):
        """ cookies """
        return AccessDict()

    # pylint: disable=no-self-use
    @cached_property
    def tokens(self):
        """ tokens """
        return AccessDict()

    def save_cookie(self, resp, *cookie_names):
        """ 记住 cookies """
        for cookie_name in cookie_names:
            self.cookies[cookie_name] = resp.cookies[cookie_name]

    def save_token(self, content, token_name, content_name=None):
        """ 记住 token """
        self.tokens[token_name] = content[content_name or token_name]

    # pylint: disable=dangerous-default-value
    def fill_cookie(self, cookie_name='sessionid', cookies={}):
        """ 填充 sessionid Cookies """
        cookies[cookie_name] = self.cookies[cookie_name]
        return cookies

    # pylint: disable=dangerous-default-value
    def fill_csrf(self, cookie_name='csrftoken', headers={}, header_name="X-CSRFToken"):
        """ 填充 CSRF Headers """
        headers[header_name] = self.cookies[cookie_name]
        return headers

    # pylint: disable=dangerous-default-value
    def fill_token(self, token_name='token', headers={}, middleware_name='token'):
        """ 填充 Authorization Headers """
        headers['Authorization'] = '{} {}'.format(middleware_name, self.tokens[token_name])
        return headers


def assert_results(content, *args, **kwargs):
    """ 结果集断言 """
    results = content["results"]
    for key in args:
        for row in results:
            if key in row:
                break
        else:
            assert False, "'{}' Not in results.".format(key)
    for key, val in kwargs.items():
        for row in results:
            if val == row.get(key, object):
                break
        else:
            assert False, "'{}': '{}' Not in results.".format(key, val)
