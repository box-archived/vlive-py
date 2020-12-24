# -*- coding: utf-8 -*-

import pickle

from .parser import sessionUserCheck


def dumpSession(session, fp):
    r""" Dump `UserSession`

    :param session: valid User Session to dump
    :type session: reqWrapper.Session
    :param fp: file to dump
    :return: Nothing
    """
    if sessionUserCheck(session):
        pickle.dump(session.cookies, fp)
    else:
        raise PermissionError("Can't find user data from session")


def loadSession(fp, session):
    r""" load `UserSession`

    :param fp: file to load
    :param session: empty Session to load User Session
    :type session: reqWrapper.Session
    :return: Nothing
    """

    session.cookies = pickle.load(fp)
