# -*- coding: utf-8 -*-

from typing import (
    Optional
)

from . import variables as gv
from .exception import auto_raise, APINetworkError
from .parser import response_json_stripper
from .router import rew_get
from .session import UserSession


def getScheduleData(
        schedule_id: str,
        session: UserSession,
        silent: bool = False
) -> Optional[dict]:
    """Get detailed schedule data.

    Arguments:
        schedule_id (:class:`str`) : Unique id of the schedule to load data.
        session (:class:`vlivepy.UserSession`) : Session for loading data with permission.
        silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.

    Returns:
        :class:`dict`. Parsed json data
    """

    sr = rew_get(**gv.endpoint_schedule_data(schedule_id),
                 wait=0.5, session=session, status=[200, 403])

    if sr.success:
        return response_json_stripper(sr.response.json(), silent=silent)
    else:
        auto_raise(APINetworkError, silent)

    return None
