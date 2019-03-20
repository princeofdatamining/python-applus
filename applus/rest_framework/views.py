from django.http import Http404
from rest_framework import exceptions#, status
from rest_framework.views import set_rollback
from rest_framework.response import Response
# from rest_framework import views


def _convert_exception(exc):
    if isinstance(exc, Http404):
        return exceptions.NotFound()
    # if isinstance(exc, PermissionDenied):
    #     exc = exceptions.PermissionDenied()
    return exc


def _make_response_data(exc):
    # if isinstance(exc.detail, (list, dict)):
    #     return exc.detail
    # else:
    #     return {'detail': exc.detail}


def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    exc = _convert_exception(exc)
    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        data = _make_response_data(exc)

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return None
