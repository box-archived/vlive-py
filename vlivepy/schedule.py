import reqWrapper
from . import variables as gv
from .exception import auto_raise, APINetworkError
from .parser import response_json_stripper


def getScheduleData(schedule, session, silent=False):

    r""" get post info
    :param schedule: schedule Id from VLIVE
    :param session: use specific session
    :param silent: Return `None` instead of Exception
    :return: Schedule Data
    :rtype: dict
    """

    sr = reqWrapper.get(**gv.endpoint_schedule_data(schedule),
                        wait=0.5, session=session, status=[200, 403])

    if sr.success:
        return response_json_stripper(sr.response.json(), silent=silent)
    else:
        auto_raise(APINetworkError, silent)

    return None
