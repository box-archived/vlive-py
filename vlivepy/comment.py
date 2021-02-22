from warnings import warn
import reqWrapper
from . import variables as gv
from .exception import ModelRefreshWarning, APINetworkError, auto_raise
from .parser import v_timestamp_parser, response_json_stripper, next_page_checker
from typing import Generator


def comment_parser(comment_list: list, session=None):
    n_list = []
    for comment in comment_list:
        n_list.append(Comment(comment['commentId'], init_data=comment, session=session))

    return n_list


def getPostComments(post, session=None, after=None, silent=False):
    r""" Get post's comments

    :param post: postId from VLIVE (like #-########)
    :param after: load page after #comment-Id
    :param session: use specific session
    :param silent: Return `None` instead of Exception
    :return: comments
    :rtype: dict
    """

    # Make request
    sr = reqWrapper.get(**gv.endpoint_post_comments(post, after),
                        wait=0.5, session=session, status=[200, 403])

    if sr.success:
        stripped_data = response_json_stripper(sr.response.json(), silent=silent)
        if 'data' in stripped_data:
            stripped_data['data'] = comment_parser(stripped_data['data'], session=session)
        return stripped_data
    else:
        auto_raise(APINetworkError, silent)

    return None


def getPostCommentsIter(post, session=None):
    r""" Get post's comments

    :param post: postId from VLIVE (like #-########)
    :param session: use specific session
    :return: comments generator
    :rtype: Generator[Comment, None, None]
    """

    data = getPostComments(post, session=session)
    after = next_page_checker(data)
    for item in data['data']:
        yield item

    while after:
        data = getPostComments(post, session=session, after=after)
        after = next_page_checker(data)
        for item in data['data']:
            yield item


def getPostStarComments(post, session=None, after=None, silent=False):
    r""" Get post's star comments

    :param post: postId from VLIVE (like #-########)
    :param after: load page after #comment-Id
    :param session: use specific session
    :param silent: Return `None` instead of Exception
    :return: comments
    :rtype: dict
    """

    # Make request
    sr = reqWrapper.get(**gv.endpoint_post_star_comments(post, after),
                        wait=0.5, session=session, status=[200, 403])

    if sr.success:
        stripped_data = response_json_stripper(sr.response.json(), silent=silent)
        if 'data' in stripped_data:
            stripped_data['data'] = comment_parser(stripped_data['data'], session=session)
        return stripped_data
    else:
        auto_raise(APINetworkError, silent)

    return None


def getPostStarCommentsIter(post, session=None):
    r""" Get post's star comments as Iterable

    :param post: postId from VLIVE (like #-########)
    :param session: use specific session
    :return: comments generator
    :rtype: Generator[Comment, None, None]
    """

    data = getPostStarComments(post, session=session)
    after = next_page_checker(data)
    for item in data['data']:
        yield item

    while after:
        data = getPostStarComments(post, session=session, after=after)
        after = next_page_checker(data)
        for item in data['data']:
            yield item


def getCommentData(commentId, session=None, silent=False):
    r""" Get post's star comments

    :param commentId: comment ID from VLIVE (like #-########)
    :param session: use specific session
    :param silent: Return `None` instead of Exception
    :return: comment
    :rtype: dict
    """

    # Make request
    sr = reqWrapper.get(**gv.endpoint_comment_data(commentId),
                        wait=0.5, session=session, status=[200, 403])

    if sr.success:
        return response_json_stripper(sr.response.json(), silent=silent)
    else:
        auto_raise(APINetworkError, silent)

    return None


class Comment(object):
    __slots__ = ['__cached_data', '__comment_id', 'session']

    def __init__(self, commentId, init_data=None, session=None):
        self.session = session
        self.__comment_id = commentId
        if init_data:
            self.__cached_data = init_data
        else:
            self.refresh()

    def __repr__(self):
        return "<Comment [%s]>" % self.__comment_id

    def refresh(self):
        res = getCommentData(commentId=self.__comment_id, session=self.session, silent=True)
        if res:
            self.__cached_data = res
        else:
            warn("Failed to refresh %s" % self, ModelRefreshWarning)

    @property
    def commentId(self) -> str:
        return self.__comment_id

    @property
    def author(self) -> dict:
        return self.__cached_data['author']

    @property
    def author_nickname(self) -> str:
        return self.__cached_data['author']['nickname']

    @property
    def author_memberId(self) -> str:
        return self.__cached_data['author']['memberId']

    @property
    def body(self) -> str:
        return self.__cached_data['body']

    @property
    def sticker(self) -> list:
        return self.__cached_data['sticker']

    @property
    def created_at(self) -> float:
        return v_timestamp_parser(self.__cached_data['createdAt'])

    @property
    def comment_count(self) -> int:
        return self.__cached_data['commentCount']

    @property
    def emotion_count(self) -> int:
        return self.__cached_data['emotionCount']

    @property
    def is_restricted(self) -> bool:
        return self.__cached_data['isRestricted']

    @property
    def parent(self) -> dict:
        return self.__cached_data['parent']

    @property
    def root(self) -> dict:
        return self.__cached_data['root']

    @property
    def written_in(self) -> str:
        return self.__cached_data['writtenIn']

    def parent_info_tuple(self):
        tp = self.parent['type']
        key = "%sId" % tp.lower()
        return self.parent['type'], self.parent['data'][key]

    def root_info_tuple(self):
        tp = self.root['type']
        key = "%sId" % tp.lower()
        return tp, self.root['data'][key]
