# -*- coding: utf-8 -*-

from warnings import catch_warnings
from typing import (
    Generator,
    Union,
    Optional,
)
from . import variables as gv
from .exception import APINetworkError, auto_raise
from .model import OfficialVideoPost, Post
from .parser import response_json_stripper, next_page_checker, v_timestamp_parser
from .router import rew_get
from .session import UserSession


class BoardPostItem(object):
    """This is the object for board post list.

   Arguments:
       post_item (:class:`bool`) : Post item dict from :func:`getBoardPost`.
       session (:class:`vlivepy.UserSession`, optional) : Session for loading data with permission.

   Attributes:
       session (:class:`vlivepy.UserSession`) : Optional. Session for loading data with permission.
   """
    __slots__ = [
        '__post_id',
        '__title',
        '__author_nickname',
        '__created_at',
        '__content_type',
        'session',
    ]

    def __init__(
            self,
            post_item: dict,
            session: UserSession,
    ):
        self.__post_id = post_item['postId']
        self.__author_nickname = post_item['author']['nickname']
        self.__created_at = post_item['createdAt']
        self.__content_type = post_item['contentType']
        self.__title = post_item['title']
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
        if self.__content_type == "VIDEO":
            return True
        else:
            return False

    @property
    def title(self) -> str:
        """Title of the post

        :rtype: :class:`str`
        """
        return self.__title

    @property
    def created_at(self) -> float:
        """Epoch timestamp about created time. The nanosecond units are displayed below the decimal point.

        :rtype: :class:`float`
        """
        return v_timestamp_parser(self.__created_at)

    @property
    def author_nickname(self) -> str:
        """Nickname of author.

        :rtype: :class:`str`
        """
        return self.__author_nickname

    @property
    def content_type(self) -> str:
        """Type of post.

        Returns:
            "POST" if the post is normal Post.
            "VIDEO" if the post is OfficialVideoPost

        :rtype: :class:`str`
        """
        return self.__content_type

    def to_object(self) -> Union[Post, OfficialVideoPost]:
        """Initialize matched object from post_id

        Returns:
            :class:`vlivepy.Post`, if the post is normal post.
            :class:`vlivepy.OfficialVideoPost`, if the post is official video
        """
        if self.__content_type == "VIDEO":
            return OfficialVideoPost(self.post_id, session=self.session)
        else:
            return Post(self.post_id, session=self.session)


def getBoardPosts(
        channel_code: str,
        board_id: Union[str, int],
        session: UserSession = None,
        after: str = None,
        latest: bool = False,
        silent: bool = False,
        raise_message: bool = False,
) -> Optional[dict]:
    """Get board post from page

    Arguments:
        channel_code (:class:`str`) : Unique id of the channel which contains board.
        board_id (:class:`str`) : Unique id of the board to load.
        session (:class:`vlivepy.UserSession`, optional) : Session for loading data with permission, defaults to None.
        after (:class:`str`, optional) : After parameter to load another page, defaults to None.
        latest (:class:`bool`, optional) : Load latest post first, defaults to False.
        silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.
        raise_message (:class:`bool`, optional) : Raise exception instead of parser warning, defaults to False.

    Returns:
        :class:`dict`. Parsed json data.
    """

    # Make request
    sr = rew_get(**gv.endpoint_board_posts(channel_code, board_id, after=after, latest=latest),
                 wait=0.5, session=session, status=[200, 403])

    if sr.success:
        stripped_data = response_json_stripper(sr.response.json(), silent=silent, raise_message=raise_message)
        if 'data' in stripped_data:
            parsed_data = []
            for item in stripped_data['data']:
                parsed_data.append(BoardPostItem(item, session))
            stripped_data['data'] = parsed_data
        return stripped_data
    else:
        auto_raise(APINetworkError, silent)

    return None


def getBoardPostsIter(
        channel_code: str,
        board_id: Union[str, int],
        session: UserSession = None,
        latest: bool = False
) -> Generator[BoardPostItem, None, None]:
    """Get board post as iterable (generator).

    Arguments:
        channel_code (:class:`str`) : Unique id of the channel which contains board.
        board_id (:class:`str`) : Unique id of the board to load.
        session (:class:`vlivepy.UserSession`, optional) : Session for loading data with permission, defaults to None.
        latest (:class:`str`, optional) : Load latest post first.

    Yields:
        :class:`BoardPostItem`
    """

    data = getBoardPosts(channel_code, board_id, session=session, latest=latest, raise_message=True)
    after = next_page_checker(data)
    for item in data['data']:
        yield item

    while after:
        data = getBoardPosts(channel_code, board_id, session=session, after=after, latest=latest, raise_message=True)
        after = next_page_checker(data)
        for item in data['data']:
            yield item
