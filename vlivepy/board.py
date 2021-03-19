# -*- coding: utf-8 -*-

from typing import Generator, Union
from . import variables as gv
from .exception import APINetworkError, auto_raise
from .model import OfficialVideoPost, Post, UserSession
from .parser import response_json_stripper, next_page_checker
from .router import rew_get


class BoardPostItem(object):
    """This is the object for board post list.

   Arguments:
       post_id (:class:`str`) : Unique id of post.
       official_video (:class:`bool`) : Session for loading data with permission.
       session (:class:`UserSession`, optional) : Session for loading data with permission.

   Attributes:
       session (:class:`UserSession`) : Optional. Session for loading data with permission.
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
        return self.__official_video

    def to_object(self) -> Union[Post, OfficialVideoPost]:
        if self.__official_video:
            return OfficialVideoPost(self.post_id, session=self.session)
        else:
            return Post(self.post_id, session=self.session)


def post_list_parser(data, session):
    n_list = []
    for item in data:
        n_list.append(BoardPostItem(item['postId'],
                                    "officialVideo" in item,
                                    session))

    return n_list


def getBoardPosts(board, channel_code, session=None, after=None, latest=False, silent=False):

    # Make request
    sr = rew_get(**gv.endpoint_board_posts(board, channel_code, after=after, latest=latest),
                 wait=0.5, session=session, status=[200, 403])

    if sr.success:
        stripped_data = response_json_stripper(sr.response.json(), silent=silent)
        if 'data' in stripped_data:
            stripped_data['data'] = post_list_parser(stripped_data['data'], session)
        return stripped_data
    else:
        auto_raise(APINetworkError, silent)

    return None


def getBoardPostsIter(board, channel_code, session=None, latest=False) -> Generator[BoardPostItem, None, None]:

    data = getBoardPosts(board, channel_code, session=session, latest=latest)
    after = next_page_checker(data)
    for item in data['data']:
        yield item

    while after:
        data = getBoardPosts(board, channel_code, session=session, after=after, latest=latest)
        after = next_page_checker(data)
        for item in data['data']:
            yield item
