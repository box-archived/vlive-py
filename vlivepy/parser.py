# -*- coding: utf-8 -*-

from collections import namedtuple
from datetime import datetime
import json
from warnings import warn
from typing import NamedTuple

from bs4 import BeautifulSoup

from .exception import auto_raise, APIJSONParesError, APIServerResponseWarning, APIServerResponseError


# UpcomingVideo = namedtuple("UpcomingVideo", "seq time cseq cname ctype name type product")


class UpcomingVideo(NamedTuple):
    """This is the named-tuple item of parsed upcoming list

    Parameters:
        seq (:class:`str`) : VideoSeq of item.
        time (:class:`str`) : String start time of item.
        cseq (:class:`str`) : Origin channel seq id of item.
        cname (:class:`str`) : Origin channel name of item.
        ctype (:class:`str`) : Origin channel type of item. "BASIC" if the channel type is normal. "PREMIUM" if the channel type is membership.
        name (:class:`str`) : Title of item.
        type (:class:`str`) : Type of item. Returns "VOD", "UPCOMING_VOD", "UPCOMING_LIVE", "LIVE"
        product (:class:`str`) : Product type of item. "NONE" if the item is normal live. "PAID" if the item is VLIVE+ product.
    """
    seq: str
    time: str
    cseq: str
    cname: str
    ctype: str
    name: str
    type: str
    product: str


def parseUpcomingFromPage(html):
    upcoming = []

    soup = BeautifulSoup(html, 'html.parser')
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


def parseVodIdFromOfficialVideoPost(post, silent=False):
    r"""

    :param post: OfficialVideoPost data from api.getOfficialVideoPost
    :type post: dict
    :param silent: Return `None` instead of Exception
    :return: VOD id of post
    :rtype: str0
    """

    # Normalize paid content data
    if 'data' in post:
        data = post['data']
    else:
        data = post

    if 'officialVideo' in data:
        if 'vodId' in data['officialVideo']:
            return data['officialVideo']['vodId']
        else:
            auto_raise(APIJSONParesError("Given data is live data"), silent=silent)
    else:
        auto_raise(APIJSONParesError("Given data is post data"), silent=silent)

    return None


def response_json_stripper(parsed_json_dict: dict, silent=False):
    # if data has success code
    if "code" in parsed_json_dict:
        if "result" in parsed_json_dict:
            parsed_json_dict = parsed_json_dict['result']
        else:
            parsed_json_dict = None
    elif 'errorCode' in parsed_json_dict:
        err_tuple = (parsed_json_dict['errorCode'], parsed_json_dict['message'].replace("\n", " "))
        if 'data' in parsed_json_dict:
            warn("Response has error [%s] %s" % err_tuple, APIServerResponseWarning)
            parsed_json_dict = parsed_json_dict['data']
        else:
            auto_raise(APIServerResponseError('[%s] %s' % err_tuple), silent=silent)

    # if data has data field (Fanship)
    if "data" in parsed_json_dict and len(parsed_json_dict) == 1:
        parsed_json_dict = parsed_json_dict["data"]

    return parsed_json_dict


def next_page_checker(page):
    if 'nextParams' in page['paging']:
        return page['paging']['nextParams']['after']
    else:
        return None


def max_res_from_play_info(play_info):
    vl = play_info['videos']['list']
    sorted_res = sorted(vl, key=lambda x: x['bitrate']['video'], reverse=True)
    return sorted_res[0]


def format_epoch(epoch, fmt):
    return datetime.fromtimestamp(epoch).strftime(fmt)


def v_timestamp_parser(ts):
    str_ts = str(ts)
    return float("%s.%s" % (str_ts[:-3], str_ts[-3:]))


def channel_info_from_channel_page(html):
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all("script"):
        if "__PRELOADED_STATE__" in str(item):
            script: str = item.contents[0].split("function")[0]
            return json.loads(script[script.find("{"): -1])['channel']['channel']
