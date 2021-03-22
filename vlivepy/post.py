# -*- coding: utf-8 -*-

from typing import (
    Optional,
)

from . import variables as gv
from .exception import auto_raise, APINetworkError
from .parser import response_json_stripper
from .router import rew_get
from .session import UserSession


def getFVideoInkeyData(
        f_video_id: str,
        session: UserSession = None,
        silent: bool = False
) -> Optional[dict]:
    """Get InKey data of File video

    Arguments:
        f_video_id (:class:`str`) : Unique id of the FVideo to load InKey data.
        session (:class:`vlivepy.UserSession`, optional) : Session for loading data with permission, defaults to None.
        silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.

    Returns:
        :class:`dict`. Parsed json data
    """

    # Make request
    sr = rew_get(**gv.endpoint_fvideo_inkey(f_video_id),
                 wait=0.5, session=session, status=[200])

    if sr.success:
        return response_json_stripper(sr.response.json(), silent=silent)['inKey']
    else:
        auto_raise(APINetworkError, silent)

    return None


def getFVideoPlayInfo(
        f_video_id: str,
        f_vod_id: str,
        session: UserSession = None,
        silent: bool = False
) -> Optional[dict]:
    """Get InKey data of File video

    Arguments:
        f_video_id (:class:`str`) : Unique id of the video-attachment to load data.
        f_vod_id (:class:`str`) : Unique id of the video-vod to load data.
        session (:class:`vlivepy.UserSession`, optional) : Session for loading data with permission, defaults to None.
        silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.

    Returns:
        :class:`dict`. Parsed json data
    """

    inkey = getFVideoInkeyData(f_video_id=f_video_id, session=session)
    sr = rew_get(**gv.endpoint_vod_play_info(f_vod_id, inkey),
                 session=session, wait=0.3, status=[200, 403])

    if sr.success:
        return response_json_stripper(sr.response.json(), silent=silent)
    else:
        auto_raise(APINetworkError, silent=silent)

    return None
