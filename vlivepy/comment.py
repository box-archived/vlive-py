# -*- coding: utf-8 -*-

from typing import Generator
import reqWrapper
from . import variables as gv
from .exception import APINetworkError, auto_raise
from .parser import response_json_stripper, next_page_checker


def comment_parser(comment_list: list, session=None):
    from .model import Comment
    n_list = []
    for comment in comment_list:
        n_list.append(Comment(comment['commentId'], session=session, init_data=comment))

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
