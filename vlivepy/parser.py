# -*- coding: utf-8 -*-
from .exception import auto_raise, APIJSONParesError
from collections import namedtuple
from bs4 import BeautifulSoup

UpcomingVideo = namedtuple("UpcomingVideo", "seq cseq cname ctype name type product")


def parseVideoSeqFromPostInfo(info, silent=False):
    """ Parse `videoSeq` item from PostInfo

    :param info: postInfo data from api.getPostInfo
    :type info: dict
    :param silent: Return `None` instead of Exception
    :return: `videoSeq` string
    :rtype: str
    """

    # Case <LIVE, VOD>
    if 'officialVideo' in info:
        return info['officialVideo']['videoSeq']

    # Case <Fanship Live, VOD, Post>
    elif 'data' in info:
        # Case <Fanship Live, VOD>
        if 'officialVideo' in info['data']:
            return info['data']['officialVideo']['videoSeq']
        # Case <Post (Exception)>
        else:
            return auto_raise(APIJSONParesError("post-%s is not video" % info['data']['postId']), silent)

    # Case <Connection failed (Exception)>
    else:
        auto_raise(APIJSONParesError("Cannot find any video"), silent)

    return None


def parseUpcomingFromPage(html):
    upcoming = []

    soup = BeautifulSoup(html, 'html.parser')
    for item in soup.find_all("a", {"class": "_title"}):
        ga_name = item.get("data-ga-name")
        ga_type = item.get("data-ga-type")
        ga_seq = item.get("data-ga-seq")
        ga_cseq = item.get("data-ga-cseq")
        ga_cname = item.get("data-ga-cname")
        ga_ctype = item.get("data-ga-ctype")
        ga_product = item.get("data-ga-product")

        upcoming.append(UpcomingVideo(seq=ga_seq, cseq=ga_cseq, cname=ga_cname,
                                      ctype=ga_ctype, name=ga_name, product=ga_product, type=ga_type))

    return upcoming


def sessionUserCheck(session):
    r"""

    :param session: session to evaluate
    :type session: reqWrapper.requests.Session
    :return: bool `isUser`
    :rtype: bool
    """
    if 'NEO_SES' in session.cookies.keys():
        return True
    else:
        return False


def parseVodIdFromOffcialVideoPost(post, silent=False):
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
