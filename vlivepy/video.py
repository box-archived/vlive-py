# -*- coding: utf-8 -*-

from time import time
import reqWrapper
from . import variables as gv
from .connections import postIdToVideoSeq, getUserSession
from .controllers import loadSession, sessionUserCheck
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


class Video(object):
    def __init__(self, number, session=None, refresh_rate=10):
        r""" Init

        :param number: video post-id or videoSeq
        :param session: use specific session
        :param refresh_rate: cache refresh rate
        """

        # interpret number
        if type(number) == int:
            number = str(number)

        # Case <post-id>
        if "-" in number:
            self.__VideoSeq = postIdToVideoSeq(number)
        # Case <videoSeq>
        else:
            self.__VideoSeq = number

        # Variable declaration
        self.session = session
        self.refresh_rate = refresh_rate
        self.__cachedTime = 0
        self.__cached_post = {}
        self.__is_VOD = False
        self.__vodId = None

        # init variables
        while self.__cachedTime == 0:
            self.refresh(force=True)

    def __repr__(self):
        if self.is_vod:
            return "<VLIVE Video(VOD) [%s]>" % self.videoSeq
        else:
            return "<VLIVE Video(LIVE) [%s]>" % self.videoSeq

    @property
    def videoSeq(self) -> str:
        return self.__VideoSeq

    @property
    def postInfo(self) -> dict:
        self.refresh()
        return self.__cached_post.copy()

    @property
    def is_vod(self) -> bool:
        return self.__is_VOD

    @property
    def vod_id(self) -> str:
        return self.__vodId

    @property
    def title(self) -> str:
        return self.__cached_post['officialVideo']['title']

    @property
    def channelCode(self) -> str:
        return self.__cached_post['author']['channelCode']

    @property
    def channelName(self) -> str:
        return self.__cached_post['author']['nickname']

    def refresh(self, force=False):
        # Cached time distance
        distance = time() - self.__cachedTime
        if distance >= self.refresh_rate or force:
            # Get data
            data = getOfficialVideoPost(self.videoSeq, silent=True)
            if data is not None:
                # Set data
                self.__cachedTime = int(time())
                self.__cached_post = data

                if 'vodId' in self.__cached_post['officialVideo']:
                    self.__is_VOD = True
                    self.__vodId = parseVodIdFromOffcialVideoPost(self.__cached_post, silent=True)

    def getOfficialVideoPost(self, silent=False):
        return getOfficialVideoPost(self.videoSeq, session=self.session, silent=silent)

    def getLivePlayInfo(self, silent=False):
        return getLivePlayInfo(self.videoSeq, session=self.session, silent=silent)

    def getInkeyData(self, silent=False):
        return getInkeyData(self.videoSeq, session=self.session, silent=silent)

    def getLiveStatus(self, silent=False):
        return getLiveStatus(self.videoSeq, silent=silent)

    def getUserSession(self, email, pwd, silent):
        self.session = getUserSession(email, pwd, silent)
        self.refresh(force=True)

    def loadSession(self, fp):
        r"""

        :param fp:
        :return: Nothing
        """
        self.session = loadSession(fp)
        self.refresh(force=True)

    def getVodPlayInfo(self, silent=False):
        if self.is_vod:
            return getVodPlayInfo(self.videoSeq, self.vod_id, session=self.session, silent=silent)
        else:
            return None
