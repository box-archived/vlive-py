# -*- coding: utf-8 -*-

import reqWrapper

from . import variables as gv
from .exception import (
    auto_raise, APINetworkError, APISignInFailedError, APIJSONParesError
)
from .parser import (parseVideoSeqFromPostInfo, sessionUserCheck,
                     parseVodIdFromOffcialVideoPost, parseUpcomingFromPage, response_json_stripper)


def getUserSession(email, pwd, silent=False):
    r""" Get user session

    :param email: VLIVE email
    :param pwd: VLIVE password
    :param silent: Return `None` instead of Exception
    :return: :class 'requests.Session` Session Object
    :rtype: reqWrapper.requests.Session
    """

    # Make request
    data = {'email': email, 'pwd': pwd}
    headers = {**gv.HeaderCommon, **gv.APISignInReferer}
    sr = reqWrapper.post(gv.APISignInUrl, data=data, headers=headers, wait=0.5, status=[200])

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


def getInkeyData(videoSeq, session=None, silent=False):
    r""" get Inkey Data
    With valid session, API also returns vpdid2

    :param videoSeq: postId from VLIVE (like ######)(Numbers)
    :param session: use specific session
    :type session: reqWrapper.requests.Session
    :param silent: Return `None` instead of Exception
    :return: Inkey data
    :rtype: dict
    """

    # Make request
    headers = {**gv.HeaderCommon, **gv.APIofficialVideoPostReferer(videoSeq)}
    sr = reqWrapper.get(gv.APIInkeyUrl(videoSeq), headers=headers, wait=0.5, session=session, status=[200])

    if sr.success:
        return response_json_stripper(sr.response.json())
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


def getPostInfo(post, session=None, silent=False):
    r""" get post info

    :param post: postId from VLIVE (like #-########)
    :param session: use specific session
    :type session: reqWrapper.requests.Session
    :param silent: Return `None` instead of Exception
    :return: videoInfo
    :rtype: dict
    """

    # Make request
    headers = {**gv.HeaderCommon, **gv.APIPostReferer(post)}
    sr = reqWrapper.get(gv.APIPostUrl(post), headers=headers, wait=0.5, session=session, status=[200, 403])

    if sr.success:
        return response_json_stripper(sr.response.json())
    else:
        auto_raise(APINetworkError, silent)

    return None


def getOfficialVideoPost(videoSeq, session=None, silent=False):
    r""" get video info from video/"videoSeq"

    :param videoSeq: postId from VLIVE (like ######)(Numbers)
    :param session: use specific session
    :param silent: Return `None` instead of Exception
    :return: Video post info
    :rtype: dict
    """

    headers = {**gv.HeaderCommon, **gv.APIofficialVideoPostReferer(videoSeq)}
    sr = reqWrapper.get(gv.APIofficialVideoPostUrl(videoSeq), headers=headers,
                        session=session, wait=0.5, status=[200, 403])

    if sr.success:
        return response_json_stripper(sr.response.json())
    else:
        auto_raise(APINetworkError, silent)

    return None


def getLivePlayInfo(videoSeq, session=None, vpdid2=None, silent=False):
    r""" Get live play info (player's init data)

    :param videoSeq: postId from VLIVE (like ######)(Numbers)
    :param session: use specific session
    :type session: reqWrapper.requests.Session
    :param vpdid2: vpdid2 from api.getInkeyData()
    :param silent: Return `None` instead of Exception
    :return: `LivePlayInfoV3` Data
    :rtype: dict
    """

    # Get vpdid2, if session is valid
    if session is not None and vpdid2 is None:
        if sessionUserCheck(session):
            vpdid2 = getVpdid2(session, silent=silent)

    # Add vpdid2 param, if vpdid2 is valid
    url = gv.APILiveV3PlayInfoUrl(videoSeq)
    if vpdid2 is not None:
        url += "&vpdid2=%s" % vpdid2

    # Make request
    headers = {**gv.HeaderCommon, **gv.APIofficialVideoPostReferer(videoSeq)}
    sr = reqWrapper.get(url, headers=headers, session=session, status=[200, 403])

    if sr.success:
        return response_json_stripper(sr.response.json())
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
    headers = {**gv.HeaderCommon, **gv.APIofficialVideoPostReferer(videoSeq)}
    sr = reqWrapper.get(gv.APILiveV2StatusUrl(videoSeq), headers=headers, wait=0.2, status=[200])

    if sr.success:
        return response_json_stripper(sr.response.json())
    else:
        auto_raise(APINetworkError, silent)

    return None


def getVodId(videoSeq, silent=False):
    data = getOfficialVideoPost(videoSeq, silent=silent)
    if data is not None:
        return parseVodIdFromOffcialVideoPost(data, silent=silent)

    return None


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
    url = gv.APIVodPlayInfoUrl(vodId, inkey)
    headers = {**gv.HeaderCommon, **gv.APIVodPlayInfoReferer}
    sr = reqWrapper.get(url, headers=headers, session=session, wait=0.3, status=[200, 403])

    if sr.success:
        return response_json_stripper(sr.response.json())
    else:
        auto_raise(APINetworkError, silent=silent)


def loadUpcoming(day=None, silent=False):
    params = dict()
    if day is not None:
        params.update({"d": day})

    # make request
    url = "https://www.vlive.tv/upcoming"
    headers = gv.HeaderCommon
    sr = reqWrapper.get(url, params=params, headers=headers)
    if sr.success:
        return sr.response.text
    else:
        auto_raise(APINetworkError, silent=silent)

    return None


def getUpcomingList(date=None, silent=False):
    html = loadUpcoming(day=date, silent=silent)
    if html is None:
        return None
    else:
        return parseUpcomingFromPage(html)


def getPostData(post, session=None, silent=False):
    r""" Get detailed post data

    :param post: postId from VLIVE (like #-########)
    :param session: use specific session
    :param silent: Return `None` instead of Exception
    :return: postData
    :rtype: dict
    """

    # Make request
    headers = {**gv.HeaderCommon, **gv.APIPostDataReferer(post)}
    sr = reqWrapper.get(gv.APIPostDataUrl(post), headers=headers, wait=0.5, session=session, status=[200, 403])

    if sr.success:
        return response_json_stripper(sr.response.json())
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

    postInfo = getPostInfo(post, silent=silent)

    return parseVideoSeqFromPostInfo(postInfo, silent=silent)


def postTypeDetector(post, silent=False):
    r""" Check given postId is Post or Video

    :param post: postId from VLIVE (like #-########)
    :param silent: Return `None` instead of Exception
    :return: str "Post" or "Video"
    :rtype: str
    """
    data = getPostInfo(post, silent=silent)
    if data is not None:
        if "officialVideo" in data:
            return "Video"
        else:
            return "Post"

    return None
