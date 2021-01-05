# -*- coding: utf-8 -*-

from . import api
from . import utils
from . import controllers
from . import parser
from time import time


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
            self.__VideoSeq = utils.postIdToVideoSeq(number)
        # Case <videoSeq>
        else:
            self.__VideoSeq = number

        # Variable declaration
        self.userSession = session
        self.refresh_rate = refresh_rate
        self.__cachedTime = 0
        self.__cached_post = {}
        self.__is_paid = None
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
        distance = int(time()) - self.__cachedTime
        if distance >= self.refresh_rate or force:
            # Get data
            data = api.getOfficialVideoPost(self.videoSeq)
            if data is not None:
                # Set Fanship info, when it is None
                if self.__is_paid is None:
                    if 'data' in data:
                        self.__is_paid = True
                    else:
                        self.__is_paid = False

                # Set data
                self.__cachedTime = int(time())
                if self.__is_paid:
                    self.__cached_post = data['data']
                else:
                    self.__cached_post = data

                if 'vodId' in self.__cached_post['officialVideo']:
                    self.__is_VOD = True
                    self.__vodId = parser.parseVodIdFromOffcialVideoPost(self.__cached_post, silent=True)

    def getOfficialVideoPost(self, silent=False):
        return api.getOfficialVideoPost(self.videoSeq, session=self.userSession, silent=silent)

    def getLivePlayInfo(self, silent=False):
        return api.getLivePlayInfo(self.videoSeq, session=self.userSession, silent=silent)

    def getInkeyData(self, silent=False):
        return api.getInkeyData(self.videoSeq, session=self.userSession, silent=silent)

    def getLiveStatus(self, silent=False):
        return api.getLiveStatus(self.videoSeq, silent=silent)

    def getUserSession(self, email, pwd, silent):
        self.userSession = api.getUserSession(email, pwd, silent)
        self.refresh(force=True)

    def loadSession(self, fp):
        r"""

        :param fp:
        :return: Nothing
        """
        self.userSession = controllers.loadSession(fp)
        self.refresh(force=True)

    def getVodPlayInfo(self, silent=False):
        if self.is_vod:
            return api.getVodPlayInfo(self.videoSeq, self.vod_id, session=self.userSession, silent=silent)
        else:
            return None
