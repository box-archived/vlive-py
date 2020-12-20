# -*- coding: utf-8 -*-

import reqWrapper

from . import variables as gv
from .exception import auto_raise, APIJSONParesError, APINetworkError


def postIdToVideoSeq(post, silent=False):
    r""" postId to videoSeq

    :param post: postId from VLIVE (like #-########)
    :param silent: Return `None` instead of Exception
    :return: str `videoSeq`
    :rtype: str
    """

    # make header
    headers = {**gv.APIPostReferer(post), **gv.HeaderAcceptLang, **gv.HeaderUserAgent}

    sr = reqWrapper.get(gv.APIPostUrl(post), headers=headers, wait=0.5)

    if sr.success:
        json_result = sr.response.json()

        # Case LIVE, VOD
        if 'officialVideo' in json_result:
            return json_result['officialVideo']['videoSeq']

        # Case Fanship Live, VOD, Post
        elif 'data' in json_result:
            # Case Fanship Live, VOD
            if 'officialVideo' in json_result['data']:
                return json_result['data']['officialVideo']['videoSeq']
            # Case Post
            else:
                return auto_raise(APIJSONParesError("post-%s is not video" % post), silent)
        # Exception
        else:
            auto_raise(APIJSONParesError("Cannot find any video: %s " % post), silent)
    else:
        if not silent:
            auto_raise(APINetworkError, silent)

    return None
