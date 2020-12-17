# -*- coding: utf-8 -*-

class APIError(Exception):
    """ Common API Error """


class PostParseError(APIError):
    """ Error about Post Info API """
