# -*- coding: utf-8 -*-

from .model import UserSession
import pickle


def dumpSession(
        session: UserSession,
        fp
) -> None:
    """Dump UserSession

    Danger:
        Dumped UserSession file is unencrypted plain binary. Do not upload/commit dumped file to public place.

    Arguments:
        session (:class:`UserSession`) : UserSession object to dump
        fp (Any) : BufferedWriter to write file
    """

    pickle.dump(session, fp)


def loadSession(
        fp
):
    """Load UserSession

    Arguments:
        fp (Any) : BufferedReader to read file

    Returns:
        :class:`UserSession`
    """

    session = pickle.load(fp)

    return session
