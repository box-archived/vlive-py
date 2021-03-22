# -*- coding: utf-8 -*-

from datetime import datetime
from typing import (
    Optional,
    Union
)
from warnings import warn

from .exception import auto_raise, APIServerResponseWarning, APIServerResponseError


def response_json_stripper(
        parsed_json_dict: dict,
        silent: bool = False
) -> Optional[dict]:
    """General parser for normalize response data format of json.
    This parses result and deletes response code. Also strip "data" field when dealing with membership response.

    Arguments:
        parsed_json_dict (:class:`dict`) : Loaded json data to normalize.
        silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.

    Returns:
        :class:`dict`. Parsed json data
    """

    # if data has success code
    if "code" in parsed_json_dict:
        if "result" in parsed_json_dict:
            parsed_json_dict = parsed_json_dict['result']
        else:
            parsed_json_dict = {}

    # if data has error code
    elif 'errorCode' in parsed_json_dict:
        err_tuple = (parsed_json_dict['errorCode'], parsed_json_dict['message'].replace("\n", " "))
        if 'data' in parsed_json_dict:
            warn("Response has error [%s] %s" % err_tuple, APIServerResponseWarning)
            parsed_json_dict = parsed_json_dict['data']
        else:
            auto_raise(APIServerResponseError('[%s] %s' % err_tuple), silent=silent)
            return None

    # if data has data field (Membership)
    if "data" in parsed_json_dict and len(parsed_json_dict) == 1:
        parsed_json_dict = parsed_json_dict["data"]

    return parsed_json_dict


def next_page_checker(
        page: dict
) -> Optional[str]:
    """This is the parser for checking "nextParams" from react page data for automatic paging in get*Iter function.

    Arguments:
        page (:class:`dict`) : Page data from get(Comments, Posts, etc..)

    Returns:
        :class:`str`. "after" parameter for paging. This returns None if response doesn't have "nextParams"
    """

    if 'nextParams' in page['paging']:
        return page['paging']['nextParams']['after']
    else:
        return None


def max_res_from_play_info(
        play_info: dict
) -> dict:
    """This is the parser for finding maximum resolution from play info (FVideo, VOD).

    Arguments:
        play_info (:class:`dict`) : Play info dict to find maximum resolution.

    Returns:
        :class:`dict`. Video data that has maximum resolution from play_info
    """

    vl = play_info['videos']['list']
    sorted_res = sorted(vl, key=lambda x: x['bitrate']['video'], reverse=True)
    return sorted_res[0]


def format_epoch(
        epoch: Union[int, float],
        fmt: str
):
    """This is the function for formatting epoch to string easily.

    Arguments:
        epoch (:class:`int`) : Epoch timestamp.
        fmt (:class:`str`) : Format-string to format Epoch.

    Returns:
        :class:`str`. Formatted epoch time.
    """
    return datetime.fromtimestamp(epoch).strftime(fmt)


def v_timestamp_parser(
        ts: Union[str, int]
) -> float:
    """This is the function for parsing VLIVE timeunit(microsecond epoch) to float second.

    Arguments:
        ts (:class:`Union[str, int]`) : VLIVE epoch time to parse.

    Returns:
        :class:`float`. parsed epoch.
    """
    str_ts = str(ts)
    return float("%s.%s" % (str_ts[:-3], str_ts[-3:]))
