# -*- coding: utf-8 -*-

import reqWrapper

from . import variables as gv
from .exception import (
    auto_raise,
    APINetworkError,
)
from .parser import channel_info_from_channel_page


def getChannelInfo(channel_code, session=None, silent=False):
    # Make request
    sr = reqWrapper.get(**gv.endpoint_channel_webpage(channel_code),
                        wait=0.5, session=session, status=[200])

    if sr.success:
        return channel_info_from_channel_page(sr.response.text)
    else:
        auto_raise(APINetworkError, silent)

    return None


def getGroupedBoards(channel_code, session=None, silent=False):
    # Make request
    sr = reqWrapper.get(**gv.endpoint_channel_grouped_boards(channel_code),
                        wait=0.5, session=session, status=[200])

    if sr.success:
        return sr.response.json()
    else:
        auto_raise(APINetworkError, silent)

    return None