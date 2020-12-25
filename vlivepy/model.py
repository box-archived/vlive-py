# -*- coding: utf-8 -*-

from . import api
from . import utils
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

        # init variables
        while self.__cachedTime == 0:
            self.refresh(force=True)

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
