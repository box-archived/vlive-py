# -*- coding: utf-8 -*-

from typing import (
    Optional,
    Union
)
from . import variables as gv
from .exception import (
    auto_raise,
    APINetworkError,
    APIJSONParesError,
)
from .parser import (
    response_json_stripper,
)
from .router import rew_get
from .session import UserSession


def getPostInfo(
        post_id: str,
        session: UserSession = None,
        silent: bool = False
) -> Optional[dict]:
    """Get detailed post data.

    Arguments:
        post_id (:class:`str`) : Unique id of the post to load data.
        session (:class:`vlivepy.UserSession`, optional) : Session for loading data with permission, defaults to None.
        silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.

    Returns:
        :class:`dict`. Parsed json data
    """

    sr = rew_get(**gv.endpoint_post(post_id),
                 wait=0.5, session=session, status=[200, 403])

    if sr.success:
        return response_json_stripper(sr.response.json(), silent=silent)
    else:
        auto_raise(APINetworkError, silent)

    return None


def postIdToVideoSeq(
        post_id: str,
        silent=False
) -> Optional[str]:
    """Convert post id to videoSeq id

    Arguments:
        post_id (:class:`str`) : Post id to convert to videoSeq id.
        silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.

    Returns:
        :class:`str`. Paired videoSeq id of the post.
    """

    post = getPostInfo(post_id, silent=silent)

    if post:
        if 'officialVideo' in post:
            return post['officialVideo']['videoSeq']
        else:
            auto_raise(APIJSONParesError("Post-%s is not official video post" % post_id), silent)

    return None


def videoSeqToPostId(
        video_seq: Union[str, int],
        silent=False
) -> Optional[str]:
    """Convert videoSeq id to post id
    
    Arguments:
        video_seq (:class:`str`, optional) : VideoSeq to convert to post id.
        silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.
    
    Returns:
        :class:`str`. Paired post id of the videoSeq.
    """

    from .video import getOfficialVideoPost

    post = getOfficialVideoPost(video_seq, silent=silent)

    if post:
        return post['postId']
    else:
        return None


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
