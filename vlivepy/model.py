# -*- coding: utf-8 -*-

from . import api
from . import utils
from . import controllers
from . import parser
from .parser import UpcomingVideo, CommentItem
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
            data = api.getOfficialVideoPost(self.videoSeq, silent=True)
            if data is not None:
                # Set data
                self.__cachedTime = int(time())
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


class Upcoming(object):
    def __init__(self, refresh_rate=5, show_vod=True, show_upcoming_vod=True, show_upcoming_live=True, show_live=True):
        self.refresh_rate = refresh_rate
        self.__cached_data = []
        self.__cached_time = 0
        self.show_live = show_live
        self.show_vod = show_vod
        self.show_upcoming_vod = show_upcoming_vod
        self.show_upcoming_live = show_upcoming_live

        # refresh data
        self.refresh(True)

    def refresh(self, force=False):
        distance = time() - self.__cached_time
        if distance >= self.refresh_rate or force:
            new_data = self.load(date=None, silent=True,
                                 show_vod=True, show_upcoming_vod=True,
                                 show_live=True, show_upcoming_live=True)
            if new_data is not None:
                self.__cached_data = new_data
                self.__cached_time = int(time())
                return True
        return False

    def load(self, date, show_vod=None, show_upcoming_vod=None, show_upcoming_live=None, show_live=None, silent=False):
        if show_live is None:
            show_live = self.show_live
        if show_vod is None:
            show_vod = self.show_vod
        if show_upcoming_vod is None:
            show_upcoming_vod = self.show_upcoming_vod
        if show_upcoming_live is None:
            show_upcoming_live = self.show_upcoming_live

        upcomings = utils.getUpcomingList(date=date, silent=silent)

        if upcomings is not None:
            data_list = []
            for item in upcomings:
                item: UpcomingVideo
                if item.type == "VOD" and show_vod:
                    data_list.append(item)
                elif item.type == "LIVE" and show_live:
                    data_list.append(item)
                elif item.type == "UPCOMING_VOD" and show_upcoming_vod:
                    data_list.append(item)
                elif item.type == "UPCOMING_LIVE" and show_upcoming_live:
                    data_list.append(item)

            return data_list
        return None

    def upcoming(self, force=False, show_vod=None, show_upcoming_vod=None, show_upcoming_live=None, show_live=None):
        r""" get upcoming list, auto refresh

        :return: Upcoming list
        :rtype: list[parser.upcomingVideo]
        """
        self.refresh(force=force)
        if show_live is None:
            show_live = self.show_live
        if show_vod is None:
            show_vod = self.show_vod
        if show_upcoming_vod is None:
            show_upcoming_vod = self.show_upcoming_vod
        if show_upcoming_live is None:
            show_upcoming_live = self.show_upcoming_live

        data_list = []
        for item in self.__cached_data:
            item: UpcomingVideo
            if item.type == "VOD" and show_vod:
                data_list.append(item)
            elif item.type == "LIVE" and show_live:
                data_list.append(item)
            elif item.type == "UPCOMING_VOD" and show_upcoming_vod:
                data_list.append(item)
            elif item.type == "UPCOMING_LIVE" and show_upcoming_live:
                data_list.append(item)

        return data_list
