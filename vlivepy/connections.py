# -*- coding: utf-8 -*-

import reqWrapper

from . import variables as gv
from .exception import (
    auto_raise, APINetworkError, APISignInFailedError, APIJSONParesError
)
from .parser import (
    parseVideoSeqFromPostInfo, sessionUserCheck, parseVodIdFromOffcialVideoPost,
    parseUpcomingFromPage, response_json_stripper, comment_parser, CommentItem,
    next_page_checker
)
from typing import Generator


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


def getFVideoInkeyData(fvideo, session=None, silent=False):
    r""" get Inkey Data

    :param fvideo: file video id from VLIVE (like ######)(Numbers)
    :param session: use specific session
    :param silent: Return `None` instead of Exception
    :return: Inkey data
    :rtype: dict
    """

    # Make request
    sr = reqWrapper.get(**gv.endpoint_fvideo_inkey(fvideo),
                        wait=0.5, session=session, status=[200])

    if sr.success:
        return response_json_stripper(sr.response.json(), silent=silent)['inKey']
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


def getFVideoPlayInfo(videoSeqId, videoVodId, session=None, silent=False):
    r""" Get fvideo VOD Data

    :param videoSeqId: videoId from attachment-id (like #-########)
    :param videoVodId: videoId from attachment/uploadInfo (like #-########)
    :param session: use specific session
    :param silent: Return `None` instead of Exception
    :return: 
    """

    inkey = getFVideoInkeyData(fvideo=videoSeqId, session=session)
    sr = reqWrapper.get(**gv.endpoint_vod_play_info(videoVodId, inkey),
                        session=session, wait=0.3, status=[200, 403])

    if sr.success:
        return response_json_stripper(sr.response.json(), silent=silent)
    else:
        auto_raise(APINetworkError, silent=silent)


def getUpcomingList(date=None, silent=False):
    params = dict()
    if date is not None:
        params.update({"d": date})

    # make request
    url = "https://www.vlive.tv/upcoming"
    sr = reqWrapper.get(url, params=params, headers=gv.HeaderCommon)

    if sr.success:
        return parseUpcomingFromPage(sr.response.text)
    else:
        auto_raise(APINetworkError, silent=silent)

    return None


def getPostComments(post, session=None, after=None, silent=False):
    r""" Get post's comments

    :param post: postId from VLIVE (like #-########)
    :param after: load page after #comment-Id
    :param session: use specific session
    :param silent: Return `None` instead of Exception
    :return: comments
    :rtype: dict
    """

    # Make request
    sr = reqWrapper.get(**gv.endpoint_post_comments(post, after),
                        wait=0.5, session=session, status=[200, 403])

    if sr.success:
        stripped_data = response_json_stripper(sr.response.json(), silent=silent)
        if 'data' in stripped_data:
            stripped_data['data'] = comment_parser(stripped_data['data'])
        return stripped_data
    else:
        auto_raise(APINetworkError, silent)

    return None


def getPostCommentsIter(post, session=None):
    r""" Get post's comments

    :param post: postId from VLIVE (like #-########)
    :param session: use specific session
    :return: comments generator
    :rtype: Generator[CommentItem, None, None]
    """

    data = getPostComments(post, session=session)
    after = next_page_checker(data)
    for item in data['data']:
        yield item

    while after:
        data = getPostComments(post, session=session, after=after)
        after = next_page_checker(data)
        for item in data['data']:
            yield item


def getPostStarComments(post, session=None, after=None, silent=False):
    r""" Get post's star comments

    :param post: postId from VLIVE (like #-########)
    :param after: load page after #comment-Id
    :param session: use specific session
    :param silent: Return `None` instead of Exception
    :return: comments
    :rtype: dict
    """

    # Make request
    sr = reqWrapper.get(**gv.endpoint_post_star_comments(post, after),
                        wait=0.5, session=session, status=[200, 403])

    if sr.success:
        stripped_data = response_json_stripper(sr.response.json(), silent=silent)
        if 'data' in stripped_data:
            stripped_data['data'] = comment_parser(stripped_data['data'])
        return stripped_data
    else:
        auto_raise(APINetworkError, silent)

    return None


def getPostStarCommentsIter(post, session=None):
    r""" Get post's star comments as Iterable

    :param post: postId from VLIVE (like #-########)
    :param session: use specific session
    :return: comments generator
    :rtype: Generator[CommentItem, None, None]
    """

    data = getPostStarComments(post, session=session)
    after = next_page_checker(data)
    for item in data['data']:
        yield item

    while after:
        data = getPostStarComments(post, session=session, after=after)
        after = next_page_checker(data)
        for item in data['data']:
            yield item


def postIdToVideoSeq(post, silent=False):
    r""" postId to videoSeq

    :param post: postId from VLIVE (like #-########)
    :param silent: Return `None` instead of Exception
    :return: str `videoSeq`
    :rtype: str
    """

    postInfo = getPostInfo(post, silent=True)

    return parseVideoSeqFromPostInfo(postInfo, silent=silent)


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
