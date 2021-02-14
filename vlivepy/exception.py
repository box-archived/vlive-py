# -*- coding: utf-8 -*-


# auto raise exception
def auto_raise(exception, silent):
    if not silent:
        raise exception


class APIError(Exception):
    """ Common API Error """


class APINetworkError(APIError):
    """ Failed to load API request """


class APIJSONParesError(APIError):
    """ Failed to parse target """


class APISignInFailedError(APIError):
    """ Failed to Sign in """


class APIServerResponseError(APIError):
    """ Warning if server response only error"""


class ModelError(Exception):
    """ Common Model Error """


class ModelInitError(Exception):
    """ Model Initialize Error """


class APIServerResponseWarning(Warning):
    """ Warning if server response with error"""


class ModelRefreshWarning(Warning):
    """ Model refresh failed """
