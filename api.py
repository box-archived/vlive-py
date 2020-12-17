import requests

from . import variables as gv
from .exception import PostParseError


def postIdToVideoSeq(post):
    headers = {}
    headers.update(gv.APIPostReferer(post))
    headers.update(gv.HeaderAcceptLang)
    headers.update(gv.HeaderUserAgent)
    res = requests.get(gv.APIPost % post, headers=headers)
    result = res.json()
    if 'officialVideo' not in result:
        raise PostParseError("post(%s) is not live video" % post)
    return result['officialVideo']['videoSeq']
