# -*- coding: utf-8 -*-

import pickle
from .parser import sessionUserCheck


def dumpSession(session, fp):
    r""" Dump `UserSession`

    :param session: valid User Session to dump
    :type session: vlivepy.UserSession
    :param fp: file to dump
    :return: Nothing
    """
    if sessionUserCheck(session.session):
        pickle.dump(session, fp)
    else:
        raise ValueError("Can't find user data from session")


def loadSession(fp):
    r""" load `UserSession`

    :param fp: file to load
    :return: Loaded Session
    :rtype: vlivepy.UserSession
    """

    session = pickle.load(fp)

    return session
