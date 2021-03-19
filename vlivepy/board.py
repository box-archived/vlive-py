# -*- coding: utf-8 -*-

from typing import (
    Generator,
    Union,
    Optional,
)
from . import variables as gv
from .exception import APINetworkError, auto_raise
from .model import OfficialVideoPost, Post
from .parser import response_json_stripper, next_page_checker
from .router import rew_get
from .session import UserSession


class BoardPostItem(object):
    """This is the object for board post list.

   Arguments:
       post_id (:class:`str`) : Unique id of post.
       official_video (:class:`bool`) : Session for loading data with permission, defaults to None.
       session (:class:`vlivepy.UserSession`, optional) : Session for loading data with permission.

   Attributes:
       session (:class:`vlivepy.UserSession`) : Optional. Session for loading data with permission.
   """
    __slots__ = ['__post_id', '__official_video', 'session']

    def __init__(
            self,
            post_id: str,
            official_video: bool,
            session: UserSession
    ):
        self.__post_id = post_id
        self.__official_video = official_video
        self.session = session

    def __repr__(self):
        return "<BoardPostItem [%s]>" % self.__post_id

    @property
    def post_id(self) -> str:
        """Unique id of post.

        :rtype: :class:`str`
        """
        return self.__post_id

    @property
    def has_official_video(self) -> bool:
        """Boolean value for having official video

        :rtype: :class:`bool`
        """
        return self.__official_video

    def to_object(self) -> Union[Post, OfficialVideoPost]:
        """Initialize matched object from post_id

        Returns:
            :class:`vlivepy.Post`, if the post is normal post.
            :class:`vlivepy.OfficialVideoPost`, if the post is official video
        """
        if self.__official_video:
            return OfficialVideoPost(self.post_id, session=self.session)
        else:
            return Post(self.post_id, session=self.session)


def getBoardPosts(
        board_id: Union[str, int],
        channel_code: str,
        session: UserSession = None,
        after: str = None,
        latest: bool = False,
        silent: bool = False
) -> Optional[dict]:
    """Get board post from page

    Arguments:
        board_id (:class:`str`) : Unique id of the board to load.
        channel_code (:class:`str`) : Unique id of the channel which contains board.
        session (:class:`vlivepy.UserSession`, optional) : Session for loading data with permission, defaults to None.
        after (:class:`str`, optional) : After parameter to load another page, defaults to None.
        latest (:class:`bool`, optional) : Load latest post first, defaults to False.
        silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.

    Returns:
        :class:`dict`. Parsed json data.
    """

    # Make request
    sr = rew_get(**gv.endpoint_board_posts(board_id, channel_code, after=after, latest=latest),
                 wait=0.5, session=session, status=[200, 403])

    if sr.success:
        stripped_data = response_json_stripper(sr.response.json(), silent=silent)
        if 'data' in stripped_data:
            parsed_data = []
            for item in stripped_data['data']:
                parsed_data.append(BoardPostItem(
                    item['postId'],
                    "officialVideo" in item,
                    session
                ))
            stripped_data['data'] = parsed_data
        return stripped_data
    else:
        auto_raise(APINetworkError, silent)

    return None


def getBoardPostsIter(
        board_id: Union[str, int],
        channel_code: str,
        session: UserSession = None,
        latest: bool = False
) -> Generator[BoardPostItem, None, None]:
    """Get board post as iterable (generator).

    Arguments:
        board_id (:class:`str`) : Unique id of the board to load.
        channel_code (:class:`str`) : Unique id of the channel which contains board.
        session (:class:`vlivepy.UserSession`, optional) : Session for loading data with permission, defaults to None.
        latest (:class:`str`, optional) : Load latest post first.

    Yields:
        :class:`BoardPostItem`
    """

    data = getBoardPosts(board_id, channel_code, session=session, latest=latest)
    after = next_page_checker(data)
    for item in data['data']:
        yield item

    while after:
        data = getBoardPosts(board_id, channel_code, session=session, after=after, latest=latest)
        after = next_page_checker(data)
        for item in data['data']:
            yield item
