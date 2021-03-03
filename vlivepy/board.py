# -*- coding: utf-8 -*-

from typing import Generator, Union
import reqWrapper
from . import variables as gv
from .exception import APINetworkError, auto_raise
from .model import OfficialVideoPost, Post
from .parser import response_json_stripper, next_page_checker


class BoardPostItem(object):
    __slots__ = ['__post_id', '__official_video', 'session']

    def __init__(self, post_id, official_video, session):
        self.__post_id = post_id
        self.__official_video = official_video
        self.session = session

    def __repr__(self):
        return "<BoardPostItem [%s]>" % self.__post_id

    @property
    def post_id(self) -> str:
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
    sr = reqWrapper.get(**gv.endpoint_board_posts(board, channel_code, after=after, latest=latest),
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