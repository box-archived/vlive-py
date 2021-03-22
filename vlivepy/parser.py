# -*- coding: utf-8 -*-

from datetime import datetime
import json
from warnings import warn

from bs4 import BeautifulSoup

from .exception import auto_raise, APIServerResponseWarning, APIServerResponseError


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
