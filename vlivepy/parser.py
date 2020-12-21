# -*- coding: utf-8 -*-
from .exception import auto_raise, APIJSONParesError


def parseVideoSeqFromPostInfo(info, silent=False):
    """ Parse `videoSeq` item from PostInfo

    :param info: postInfo data from api.getPostInfo
    :type info: dict
    :param silent: Return `None` instead of Exception
    :return: `videoSeq` string
    :rtype: str
    """

    # Case <LIVE, VOD>
    if 'officialVideo' in info:
        return info['officialVideo']['videoSeq']

    # Case <Fanship Live, VOD, Post>
    elif 'data' in info:
        # Case <Fanship Live, VOD>
        if 'officialVideo' in info['data']:
            return info['data']['officialVideo']['videoSeq']
        # Case <Post (Exception)>
        else:
            return auto_raise(APIJSONParesError("post-%s is not video" % info['data']['postId']), silent)

    # Case <Connection failed (Exception)>
    else:
        auto_raise(APIJSONParesError("Cannot find any video"), silent)

    return None