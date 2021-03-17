# -*- coding: utf-8 -*-

from . import variables as gv
from .exception import auto_raise, APINetworkError
from .parser import response_json_stripper
from .router import rew_get


def getFVideoInkeyData(fvideo, session=None, silent=False):
    r""" get Inkey Data

    :param fvideo: file video id from VLIVE (like ######)(Numbers)
    :param session: use specific session
    :param silent: Return `None` instead of Exception
    :return: Inkey data
    :rtype: dict
    """

    # Make request
    sr = rew_get(**gv.endpoint_fvideo_inkey(fvideo),
                 wait=0.5, session=session, status=[200])

    if sr.success:
        return response_json_stripper(sr.response.json(), silent=silent)['inKey']
    else:
        auto_raise(APINetworkError, silent)

    return None


def getFVideoPlayInfo(videoSeqId, videoVodId, session=None, silent=False):
    r""" Get fvideo VOD Data

    :param videoSeqId: videoId from attachment-id (like #-########)
    :param videoVodId: videoId from attachment/uploadInfo (like #-########)
    :param session: use specific session
    :param silent: Return `None` instead of Exception
    :return:
    """

    inkey = getFVideoInkeyData(fvideo=videoSeqId, session=session)
    sr = rew_get(**gv.endpoint_vod_play_info(videoVodId, inkey),
                 session=session, wait=0.3, status=[200, 403])

    if sr.success:
        return response_json_stripper(sr.response.json(), silent=silent)
    else:
        auto_raise(APINetworkError, silent=silent)
