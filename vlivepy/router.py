# -*- coding: utf-8 -*-

import reqWrapper


def rew_get(url, session=None, **kwargs) -> reqWrapper.SafeResponse:
    if session:
        local_session = session.session
    else:
        local_session = None

    return reqWrapper.get(url=url, session=local_session, **kwargs)
