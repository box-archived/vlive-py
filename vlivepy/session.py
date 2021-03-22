# -*- coding: utf-8 -*-

import pickle
from typing import (
    Optional
)

import reqWrapper

from .exception import (
    auto_raise,
    APISignInFailedError,
    APINetworkError,
)
from . import variables as gv


def getUserSession(
        email: str,
        pwd: str,
        silent: bool = False
) -> Optional[reqWrapper.Session]:
    """Get logged in :class:`reqWrapper.Session` session

    Arguments:
        email (:class:`str`) : Email of the account to sign-in.
        pwd (:class:`vlivepy.UserSession`, optional) : Password of the account to sign-in.
        silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.

    Returns:
        :class:`reqWrapper.Session`. Logged in session.
    """

    # Make request
    sr = reqWrapper.post(**gv.endpoint_auth(email, pwd),
                         wait=0.5, status=[200])

    if sr.success:
        # Case <Sign-in Failed (Exception)>
        if 'auth/email' in sr.response.url:
            auto_raise(APISignInFailedError("Sign-in Failed"), silent)

        # Case <Sign-in>
        else:
            return sr.session

    # Case <Connection failed (Exception)>
    else:
        auto_raise(APINetworkError, silent)

    return None


class UserSession(object):
    """This is the object for using vlivepy with user permission.
    You need to use UserSession when you load user-only content (e.g VLIVE+, Membership, etc..)

    Email-account info(email, pwd) should be used as login info. This is not working with social login info.

    Caution:
        Too frequent login-try will be banned from VLIVE.

        Use :func:`vlivepy.dumpSession` and :func:`vlivepy.loadSession` to saving UserSession

    Arguments:
        email (:class:`str`) : Sign-in email
        pwd (:class:`str`) : Sign-in password

    """
    __slots__ = ["__email", "__pwd", "__session"]

    def __init__(
            self,
            email: str,
            pwd: str
    ):
        self.__email = email
        self.__pwd = pwd
        self.__session = None
        self.__session: reqWrapper.Session

        self.refresh()

    def __repr__(self):
        return "<VLIVE UserSession [%s]>" % self.__email

    def refresh(self) -> None:
        """Reload login data"""
        self.__session = getUserSession(email=self.__email, pwd=self.__pwd)

    @property
    def session(self) -> reqWrapper.Session:
        """Get logged-in Session

        :rtype: :class:`reqWrapper.Session`
        """
        return self.__session


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
) -> UserSession:
    """Load UserSession

    Arguments:
        fp (Any) : BufferedReader to read file

    Returns:
        :class:`UserSession`
    """

    session = pickle.load(fp)

    return session
