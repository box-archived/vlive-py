# -*- coding: utf-8 -*-

import json
from typing import (
    Optional
)

from bs4 import BeautifulSoup

from . import variables as gv
from .exception import (
    auto_raise,
    APINetworkError,
    APIJSONParesError
)
from .router import rew_get
from .session import UserSession


def getChannelInfo(
        channel_code: str,
        session: UserSession = None,
        silent: bool = False
) -> Optional[dict]:
    """Get detailed Channel info.

    Arguments:
        channel_code (:class:`str`, optional) : Unique id of channel to load.
        session (:class:`vlivepy.UserSession`, optional) : Session for loading data with permission, defaults to None.
        silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.

    Returns:
        :class:`dict`. Parsed channel data
    """

    # Make request
    sr = rew_get(**gv.endpoint_channel_webpage(channel_code),
                 wait=0.5, session=session, status=[200])

    if sr.success:
        soup = BeautifulSoup(sr.response.text, "html.parser")
        for item in soup.find_all("script"):
            if "__PRELOADED_STATE__" in str(item):
                script: str = item.contents[0].split("function")[0]
                return json.loads(script[script.find("{"): -1])['channel']['channel']
        else:
            auto_raise(APIJSONParesError("Cannot find channel data from page"), silent)
    else:
        auto_raise(APINetworkError, silent)

    return None


def getGroupedBoards(
        channel_code: str,
        session: UserSession = None,
        silent: bool = False
) -> Optional[dict]:
    """Get grouped boards info.

    Arguments:
        channel_code (:class:`str`, optional) : Unique id of channel to load boards.
        session (:class:`vlivepy.UserSession`, optional) : Session for loading data with permission, defaults to None.
        silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.

    Returns:
        :class:`dict`. Parsed json data.
    """

    # Make request
    sr = rew_get(**gv.endpoint_channel_grouped_boards(channel_code),
                 wait=0.5, session=session, status=[200])

    if sr.success:
        return sr.response.json()
    else:
        auto_raise(APINetworkError, silent)

    return None
