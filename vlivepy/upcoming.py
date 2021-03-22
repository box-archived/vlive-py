# -*- coding: utf-8 -*-

from typing import (
    List,
    Optional,
    Union
)

from bs4 import BeautifulSoup
import reqWrapper

from . import variables as gv
from .exception import auto_raise, APINetworkError


class UpcomingVideo(object):
    """This is the object for upcoming list item"""

    __slots__ = ['__seq', '__time', '__cseq', '__cname', '__ctype', '__name', '__type', '__product']

    def __init__(self, seq, time, cseq, cname, ctype, name, type, product):
        self.__seq = seq
        self.__time = time
        self.__cseq = cseq
        self.__cname = cname
        self.__ctype = ctype
        self.__name = name
        self.__type = type
        self.__product = product

    def __eq__(self, other):
        if type(self) == type(other):
            if self.seq == other.seq:
                return True
        return False

    def __repr__(self):
        return "<UpcomingVideo [%s:%s]>" % (self.__seq, self.__type)

    @property
    def seq(self) -> str:
        """VideoSeq of item.

        :rtype: :class:`str`
        """
        return self.__seq

    @property
    def time(self) -> str:
        """String start time of item.

        :rtype: :class:`str`
        """
        return self.__time

    @property
    def cseq(self) -> str:
        """Origin channel seq id of item.

        :rtype: :class:`str`
        """
        return self.__seq

    @property
    def cname(self) -> str:
        """Origin channel name of item.

        :rtype: :class:`str`
        """
        return self.__cname

    @property
    def ctype(self) -> str:
        """Origin channel type of item.

        Returns:
            "BASIC" if the channel type is normal. "PREMIUM" if the channel type is membership.

        :rtype: :class:`str`
        """
        return self.__ctype

    @property
    def name(self) -> str:
        """Title of item.

        :rtype: :class:`str`
        """
        return self.__name

    @property
    def type(self) -> str:
        """Type of item.

        Returns:
             "VOD", "UPCOMING_VOD", "UPCOMING_LIVE", "LIVE"

        :rtype: :class:`str`
        """
        return self.__type

    @property
    def product(self) -> str:
        """ Product type of item.

        Returns:
            "NONE" if the item is normal live. "PAID" if the item is VLIVE+ product.

        :rtype: :class:`str`
        """
        return self.__product


def getUpcomingList(
        date: Union[str, int] = None,
        silent: bool = False
) -> Optional[List[UpcomingVideo]]:
    """Load upcoming webpage and parse each item.

    Arguments:
        date (:class:`Union[str, int]`, optional) : The date with yyyyMMdd format to load upcoming, defaults to None.
        silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.

    Returns:
        List of :class:`UpcomingVideo`
    """
    params = dict()
    if date is not None:
        params.update({"d": date})

    # make request
    url = "https://www.vlive.tv/upcoming"
    sr = reqWrapper.get(url, params=params, headers=gv.HeaderCommon)

    if sr.success:
        upcoming = []

        soup = BeautifulSoup(sr.response.text, 'html.parser')
        soup_upcoming_list = soup.find("ul", {"class": "upcoming_list"})
        for item in soup_upcoming_list.find_all("li"):
            item_type_vod = False

            # find replay class in <li> tag
            soup_item_class_tag = item.get("class")
            if soup_item_class_tag is not None:
                if soup_item_class_tag[0] == "replay":
                    item_type_vod = True

            soup_time = item.find("span", {"class": "time"})
            release_time = soup_time.get_text()

            # get title <a> tag
            soup_info_tag = item.find("a", {"class": "_title"})

            # parse upcoming data
            ga_name = soup_info_tag.get("data-ga-name")
            ga_type = soup_info_tag.get("data-ga-type")
            ga_seq = soup_info_tag.get("data-ga-seq")
            ga_cseq = soup_info_tag.get("data-ga-cseq")
            ga_cname = soup_info_tag.get("data-ga-cname")
            ga_ctype = soup_info_tag.get("data-ga-ctype")
            ga_product = soup_info_tag.get("data-ga-product")
            if ga_type == "UPCOMING":
                if item_type_vod:
                    ga_type += "_VOD"
                else:
                    ga_type += "_LIVE"

            # create item and append
            upcoming.append(UpcomingVideo(seq=ga_seq, time=release_time, cseq=ga_cseq, cname=ga_cname,
                                          ctype=ga_ctype, name=ga_name, product=ga_product, type=ga_type))

        return upcoming
    else:
        auto_raise(APINetworkError, silent=silent)

    return None
