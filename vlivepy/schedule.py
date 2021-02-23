import reqWrapper
from . import variables as gv
from .exception import auto_raise, APINetworkError
from .parser import response_json_stripper


def getScheduleData(schedule_id, session, silent=False):

    r""" get post info
    :param schedule_id: schedule Id from VLIVE
    :param session: use specific session
    :param silent: Return `None` instead of Exception
    :return: Schedule Data
    :rtype: dict
    """

    sr = reqWrapper.get(**gv.endpoint_schedule_data(schedule_id),
                        wait=0.5, session=session, status=[200, 403])

    if sr.success:
        return response_json_stripper(sr.response.json(), silent=silent)
    else:
        auto_raise(APINetworkError, silent)

    return None


class Schedule(object):
    __slots__ = ["__cached_data", "__schedule_id", "session"]

    def __init__(self, schedule_id, session):
        self.__schedule_id = schedule_id
        self.__cached_data = {}
        self.session = session
        self.refresh()

    def refresh(self, silent=False):
        data = getScheduleData(self.__schedule_id, self.session, silent)
        if data is not None:
            self.__cached_data = data

    @property
    def raw(self) -> dict:
        return self.__cached_data.copy()

    @property
    def author(self) -> dict:
        return self.raw['author'].copy()

    @property
    def author_nickname(self) -> str:
        return self.raw['author']['nickname']

    @property
    def author_id(self) -> str:
        return self.raw['author']
