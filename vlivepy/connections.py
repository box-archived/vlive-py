# -*- coding: utf-8 -*-

import reqWrapper
from . import variables as gv
from .exception import (
    auto_raise, APINetworkError, APISignInFailedError
)
from .parser import (
    parseVideoSeqFromPostInfo, response_json_stripper,
)


def getPostInfo(post, session=None, silent=False):
    r""" get post info

    :param post: postId from VLIVE (like #-########)
    :param session: use specific session
    :param silent: Return `None` instead of Exception
    :return: videoInfo
    :rtype: dict
    """

    sr = reqWrapper.get(**gv.endpoint_post(post),
                        wait=0.5, session=session, status=[200, 403])

    if sr.success:
        return response_json_stripper(sr.response.json(), silent=silent)
    else:
        auto_raise(APINetworkError, silent)

    return None


def getUserSession(email, pwd, silent=False):
    r""" Get user session

    :param email: VLIVE email
    :param pwd: VLIVE password
    :param silent: Return `None` instead of Exception
    :return: :class 'requests.Session` Session Object
    :rtype: reqWrapper.requests.Session
    """

    # Make request
    sr = reqWrapper.post(**gv.endpoint_auth(email, pwd),
                         wait=0.5, status=[200])

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

    return None


def postIdToVideoSeq(post, silent=False):
    r""" postId to videoSeq

    :param post: postId from VLIVE (like #-########)
    :param silent: Return `None` instead of Exception
    :return: str `videoSeq`
    :rtype: str
    """

    postInfo = getPostInfo(post, silent=True)

    return parseVideoSeqFromPostInfo(postInfo, silent=silent)


def videoSeqToPostId(videoSeq, silent=False):
    from .video import getOfficialVideoPost
    r""" postId to videoSeq

    :param post: postId from VLIVE (like #-########)
    :param silent: Return `None` instead of Exception
    :return: str `videoSeq`
    :rtype: str
    """

    post = getOfficialVideoPost(videoSeq, silent=silent)

    return post['postId']


def postTypeDetector(post, silent=False):
    r""" Check given postId is Post or Video

    :param post: postId from VLIVE (like #-########)
    :param silent: Return `None` instead of Exception
    :return: str "POST" or "VIDEO"
    :rtype: str
    """
    data = getPostInfo(post, silent=silent)
    if data is not None:
        return data['contentType']

    return None


def decode_channel_code(channel_code, silent=False):
    sr = reqWrapper.get(**gv.endpoint_decode_channel_code(channel_code),
                        wait=0.5, status=[200])

    if sr.success:
        if len(sr.response.text) > 0:
            return sr.response.json()['result']['channelSeq']
        else:
            auto_raise(ValueError("inappropriate ChannelCode"), silent)
    else:
        auto_raise(APINetworkError, silent)

    return None
