# -*- coding: utf-8 -*-

import reqWrapper
from . import variables as gv
from .controllers import sessionUserCheck
from .exception import auto_raise, APINetworkError, APIJSONParesError
from .parser import parseVodIdFromOffcialVideoPost, response_json_stripper


def getOfficialVideoPost(videoSeq, session=None, silent=False):
    r""" get video info from video/"videoSeq"

    :param videoSeq: postId from VLIVE (like ######)(Numbers)
    :param session: use specific session
    :param silent: Return `None` instead of Exception
    :return: Video post info
    :rtype: dict
    """

    sr = reqWrapper.get(**gv.endpoint_official_video_post(videoSeq),
                        session=session, wait=0.5, status=[200, 403])

    if sr.success:
        return response_json_stripper(sr.response.json(), silent=silent)
    else:
        auto_raise(APINetworkError, silent)

    return None


def getLivePlayInfo(videoSeq, session=None, vpdid2=None, silent=False):
    r""" Get live play info (player's init data)

    :param videoSeq: postId from VLIVE (like ######)(Numbers)
    :param session: use specific session
    :param vpdid2: vpdid2 from api.getInkeyData()
    :param silent: Return `None` instead of Exception
    :return: `LivePlayInfoV3` Data
    :rtype: dict
    """

    # Get vpdid2, if session is valid
    if session is not None and vpdid2 is None:
        if sessionUserCheck(session):
            vpdid2 = getVpdid2(session, silent=silent)

    # Make request
    sr = reqWrapper.get(**gv.endpoint_live_play_info(videoSeq, vpdid2),
                        session=session, status=[200, 403])

    if sr.success:
        return response_json_stripper(sr.response.json(), silent=silent)
    else:
        auto_raise(APINetworkError, silent)

    return None


def getLiveStatus(videoSeq, silent=False):
    r""" Get live status (player's interval check)

    :param videoSeq: postId from VLIVE (like ######)(Numbers)
    :param silent: Return `None` instead of Exception
    :return: `LiveStatus` Data
    :rtype: dict
    """

    # Make request
    sr = reqWrapper.get(**gv.endpoint_live_status(videoSeq),
                        wait=0.2, status=[200])

    if sr.success:
        return response_json_stripper(sr.response.json(), silent=silent)
    else:
        auto_raise(APINetworkError, silent)

    return None


def getVodId(videoSeq, silent=False):
    data = getOfficialVideoPost(videoSeq, silent=silent)
    if data is not None:
        return parseVodIdFromOffcialVideoPost(data, silent=silent)

    return None


def getInkeyData(videoSeq, session=None, silent=False):
    r""" get Inkey Data
    With valid session, API also returns vpdid2

    :param videoSeq: postId from VLIVE (like ######)(Numbers)
    :param session: use specific session
    :param silent: Return `None` instead of Exception
    :return: Inkey data
    :rtype: dict
    """

    # Make request
    sr = reqWrapper.get(**gv.endpoint_vod_inkey(videoSeq),
                        wait=0.5, session=session, status=[200])

    if sr.success:
        return response_json_stripper(sr.response.json(), silent=silent)
    else:
        auto_raise(APINetworkError, silent)

    return None


def getVpdid2(session, silent=False):
    r""" get vpdid2 value
    request to video "142851"

    :param session: use specific session
    :type session: reqWrapper.requests.Session
    :param silent: Return `None` instead of Exception
    :return: vpdid2 data
    :rtype: str
    """

    inkey = getInkeyData("142851", session=session, silent=silent)
    if inkey is None:
        return None
    else:
        if 'vpdid2' not in inkey:
            auto_raise(APIJSONParesError("Server didn't return vpdid2"), silent=silent)
        return inkey['vpdid2']


def getVodPlayInfo(videoSeq, vodId=None, session=None, silent=False):
    r""" Get VOD Data

    :param videoSeq: postId from VLIVE (like ######)(Numbers)
    :param vodId: VOD ID to parse (Hex string)
    :param session: use specific session
    :param silent: Return `None` instead of Exception
    :return:
    """

    inkey = getInkeyData(videoSeq, session=session, silent=silent)['inkey']
    if vodId is None:
        vodId = getVodId(videoSeq)

    # make request
    sr = reqWrapper.get(**gv.endpoint_vod_play_info(vodId, inkey),
                        session=session, wait=0.3, status=[200, 403])

    if sr.success:
        return response_json_stripper(sr.response.json(), silent=silent)
    else:
        auto_raise(APINetworkError, silent=silent)
