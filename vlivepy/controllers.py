# -*- coding: utf-8 -*-

import pickle

from .parser import sessionUserCheck
from reqWrapper import Session


def dumpSession(session, fp):
    r""" Dump `UserSession`

    :param session: valid User Session to dump
    :type session: Session
    :param fp: file to dump
    :return: Nothing
    """
    if sessionUserCheck(session):
        pickle.dump(session.cookies, fp)
    else:
        raise ValueError("Can't find user data from session")


def loadSession(fp):
    r""" load `UserSession`

    :param fp: file to load
    :return: Loaded Session
    :rtype: Session
    """
    session = Session()
    session.cookies = pickle.load(fp)

    return session
