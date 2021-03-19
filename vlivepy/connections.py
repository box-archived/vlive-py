# -*- coding: utf-8 -*-

from typing import (
    Optional,
    Union
)
import reqWrapper
from . import variables as gv
from .exception import (
    auto_raise, APINetworkError, APISignInFailedError
)
from .parser import (
    parseVideoSeqFromPostInfo, response_json_stripper,
)
from .router import rew_get


def getPostInfo(post, session=None, silent=False):
    r""" get post info

    :param post: postId from VLIVE (like #-########)
    :param session: use specific session
    :param silent: Return `None` instead of Exception
    :return: videoInfo
    :rtype: dict
    """

    sr = rew_get(**gv.endpoint_post(post),
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


def postIdToVideoSeq(
        post_id: str,
        silent=False
) -> str:
    """Convert post id to videoSeq id

    Arguments:
        post_id (:class:`str`) : Post id to convert to videoSeq id.
        silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.

    Returns:
        :class:`str`. Paired videoSeq id of the post.
    """

    postInfo = getPostInfo(post_id, silent=True)

    return parseVideoSeqFromPostInfo(postInfo, silent=silent)


def videoSeqToPostId(
        videoSeq: Union[str, int],
        silent=False
) -> str:
    from .video import getOfficialVideoPost
    """Convert videoSeq id to post id
    
    Arguments:
        videoSeq (:class:`str`, optional) : VideoSeq to convert to post id.
        silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.
    
    Returns:
        :class:`str`. Paired post id of the videoSeq.
    """

    post = getOfficialVideoPost(videoSeq, silent=silent)

    return post['postId']


def postTypeDetector(post_id, silent=False):
    """Check type of the post

    Arguments:
        post_id (:class:`str`, optional) : Unique id of the post to check.
        silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.

    Returns:
        :class:`str`. “POST” if the post is normal Post. “VIDEO” if the post is OfficialVideoPost
    """

    data = getPostInfo(post_id, silent=silent)
    if data is not None:
        return data['contentType']

    return None


def decode_channel_code(
        channel_code: str,
        silent: bool = False
) -> Optional[int]:
    """Decode channel code to unique channel seq

    Arguments:
        channel_code (:class:`str`, optional) : Unique id of the post to check.
        silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.

    Returns:
        :class:`int`. Decoded channel code as channel seq.
    """

    sr = rew_get(**gv.endpoint_decode_channel_code(channel_code),
                 wait=0.5, status=[200])

    if sr.success:
        if len(sr.response.text) > 0:
            return sr.response.json()['result']['channelSeq']
        else:
            auto_raise(ValueError("inappropriate ChannelCode"), silent)
    else:
        auto_raise(APINetworkError, silent)

    return None
