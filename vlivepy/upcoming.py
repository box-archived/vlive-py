from time import time
import reqWrapper
from . import variables as gv
from .exception import auto_raise, APINetworkError
from .parser import UpcomingVideo, parseUpcomingFromPage


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

        upcomings = getUpcomingList(date=date, silent=silent)

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
