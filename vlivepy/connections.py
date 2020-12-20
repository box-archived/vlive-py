# -*- coding: utf-8 -*-

import reqWrapper

from . import variables as gv
from .exception import (
    auto_raise, APIJSONParesError, APINetworkError, APISignInFailedError
)


def getUserSession(email, pwd, silent=False):
    r""" Get user session

    :param email: VLIVE email
    :param pwd: VLIVE password
    :param silent: Return `None` instead of Exception
    :return: :class 'requests.Session` Session Object
    :rtype: reqWrapper.requests.Session
    """

    # Make request
    data = {'email': email, 'pwd': pwd}
    headers = {**gv.HeaderCommon, **gv.APISignInReferer}
    sr = reqWrapper.post(gv.APISignInUrl, data=data, headers=headers, wait=0.5)

    if sr.success:
        # Case <Sign-in Failed (Exception)>
        if 'auth/email' in sr.response.url:
            auto_raise(APISignInFailedError("Sign-in Failed"), silent)

        # Case <Sign-in>
        else:
            return sr.session

    # Case <Connection failed (Exception)>
    else:
        auto_raise(APINetworkError, silent)


def postIdToVideoSeq(post, silent=False):
    r""" postId to videoSeq

    :param post: postId from VLIVE (like #-########)
    :param silent: Return `None` instead of Exception
    :return: str `videoSeq`
    :rtype: str
    """

    # Make request
    headers = {**gv.APIPostReferer(post), **gv.HeaderAcceptLang, **gv.HeaderUserAgent}
    sr = reqWrapper.get(gv.APIPostUrl(post), headers=headers, wait=0.5)

    if sr.success:
        # Parse response json
        json_result = sr.response.json()

        # Case <LIVE, VOD>
        if 'officialVideo' in json_result:
            return json_result['officialVideo']['videoSeq']

        # Case <Fanship Live, VOD, Post>
        elif 'data' in json_result:
            # Case <Fanship Live, VOD>
            if 'officialVideo' in json_result['data']:
                return json_result['data']['officialVideo']['videoSeq']
            # Case <Post (Exception)>
            else:
                return auto_raise(APIJSONParesError("post-%s is not video" % post), silent)
        # Case <Connection failed (Exception)>
        else:
            auto_raise(APIJSONParesError("Cannot find any video: %s " % post), silent)
    else:
        if not silent:
            auto_raise(APINetworkError, silent)

    return None
