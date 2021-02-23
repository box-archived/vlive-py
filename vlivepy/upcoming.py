import reqWrapper
from . import variables as gv
from .exception import auto_raise, APINetworkError
from .parser import parseUpcomingFromPage


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
