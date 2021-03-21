# -*- coding: utf-8 -*-

from typing import (
    Generator,
    Optional,
)
from . import variables as gv
from .exception import APINetworkError, auto_raise
from .parser import response_json_stripper, next_page_checker
from .router import rew_get
from .session import UserSession


def comment_parser(
        comment_list: list,
        session: UserSession = None
) -> list:
    """Parse each comment json data to :class:`vlivepy.Comment` object.

    Arguments:
        comment_list (:class:`list`) : Comment list to parse.
        session (:class:`vlivepy.UserSession`, optional) : Session for loading data with permission, defaults to None.

    Returns:
        List of :class:`vlivepy.Comment`
    """

    from .model import Comment
    n_list = []
    for comment_item in comment_list:
        n_list.append(Comment(comment_item['commentId'], session=session, init_data=comment_item))

    return n_list


def getPostComments(
        post_id: str,
        session: UserSession = None,
        after: str = None,
        silent: bool = False
) -> Optional[dict]:
    """Get comments of the post.

    Arguments:
        post_id (:class:`str`) : Unique id of the post to load comment.
        session (:class:`vlivepy.UserSession`, optional) : Session for loading data with permission, defaults to None.
        after (:class:`str`, optional) : After parameter to load another page, defaults to None.
        silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.

    Returns:
        :class:`dict`. Parsed json data.
    """

    # Make request
    sr = rew_get(**gv.endpoint_post_comments(post_id, after),
                 wait=0.5, session=session, status=[200, 403])

    if sr.success:
        stripped_data = response_json_stripper(sr.response.json(), silent=silent)
        if 'data' in stripped_data:
            stripped_data['data'] = comment_parser(stripped_data['data'], session=session)
        return stripped_data
    else:
        auto_raise(APINetworkError, silent)

    return None


def getPostCommentsIter(
        post_id: str,
        session: UserSession = None
):
    """Get comments of post as iterable (generator).

    Arguments:
        post_id (:class:`str`) : Unique id of the post to load comment.
        session (:class:`vlivepy.UserSession`, optional) : Session for loading data with permission, defaults to None.

    :rtype: Generator[vlivepy.Comment, None, None]

    Yields:
        :class:`vlivepy.Comment`
    """

    data = getPostComments(post_id, session=session)
    after = next_page_checker(data)
    for item in data['data']:
        yield item

    while after:
        data = getPostComments(post_id, session=session, after=after)
        after = next_page_checker(data)
        for item in data['data']:
            yield item


def getPostStarComments(
        post_id: str,
        session: UserSession = None,
        after: str = None,
        silent: bool = False
) -> Optional[dict]:
    """Get star comments of the post.

    Arguments:
        post_id (:class:`str`) : Unique id of the post to load star comment.
        session (:class:`vlivepy.UserSession`, optional) : Session for loading data with permission, defaults to None.
        after (:class:`str`, optional) : After parameter to load another page, defaults to None.
        silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.

    Returns:
        :class:`dict`. Parsed json data.
    """

    # Make request
    sr = rew_get(**gv.endpoint_post_star_comments(post_id, after),
                 wait=0.5, session=session, status=[200, 403])

    if sr.success:
        stripped_data = response_json_stripper(sr.response.json(), silent=silent)
        if 'data' in stripped_data:
            stripped_data['data'] = comment_parser(stripped_data['data'], session=session)
        return stripped_data
    else:
        auto_raise(APINetworkError, silent)

    return None


def getPostStarCommentsIter(
        post_id: str,
        session: UserSession = None
):
    """Get star comments of post as iterable (generator).

    Arguments:
        post_id (:class:`str`) : Unique id of the post to load star comment.
        session (:class:`vlivepy.UserSession`, optional) : Session for loading data with permission, defaults to None.

    :rtype: Generator[vlivepy.Comment, None, None]

    Yields:
        :class:`vlivepy.Comment`
    """

    data = getPostStarComments(post_id, session=session)
    after = next_page_checker(data)
    for item in data['data']:
        yield item

    while after:
        data = getPostStarComments(post_id, session=session, after=after)
        after = next_page_checker(data)
        for item in data['data']:
            yield item


def getCommentData(
        comment_id: str,
        session: UserSession = None,
        silent: bool = False
) -> Optional[dict]:
    """Get detailed comment data.

    Arguments:
        comment_id (:class:`str`) : Unique id of the comment to load data.
        session (:class:`vlivepy.UserSession`, optional) : Session for loading data with permission, defaults to None.
        silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.

    Returns:
        :class:`dict`. Parsed json data
    """

    # Make request
    sr = rew_get(**gv.endpoint_comment_data(comment_id),
                 wait=0.5, session=session, status=[200, 403])

    if sr.success:
        return response_json_stripper(sr.response.json(), silent=silent)
    else:
        auto_raise(APINetworkError, silent)

    return None


def getNestedComments(
        comment_id: str,
        session: UserSession = None,
        after: str = None,
        silent: bool = False
) -> Optional[dict]:
    """Get nested comments of the comment.

    Arguments:
        comment_id (:class:`str`) : Unique id of the comment to load nested comment.
        session (:class:`vlivepy.UserSession`, optional) : Session for loading data with permission, defaults to None.
        after (:class:`str`, optional) : After parameter to load another page, defaults to None.
        silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.

    Returns:
        :class:`dict`. Parsed json data.
    """

    # Make request
    sr = rew_get(**gv.endpoint_comment_nested(comment_id, after),
                 wait=0.5, session=session, status=[200, 403])

    if sr.success:
        stripped_data = response_json_stripper(sr.response.json(), silent=silent)
        if 'data' in stripped_data:
            stripped_data['data'] = comment_parser(stripped_data['data'], session=session)
        return stripped_data
    else:
        auto_raise(APINetworkError, silent)

    return None


def getNestedCommentsIter(
        comment_id: str,
        session: UserSession = None
):
    """Get nested comments of the comment as iterable (generator).

    Arguments:
        comment_id (:class:`str`) : Unique id of the comment to load nested comment.
        session (:class:`vlivepy.UserSession`, optional) : Session for loading data with permission, defaults to None.

    :rtype: Generator[vlivepy.Comment, None, None]

    Yields:
        :class:`vlivepy.Comment`
    """

    data = getNestedComments(comment_id, session=session)
    after = next_page_checker(data)
    for item in data['data']:
        yield item

    while after:
        data = getNestedComments(comment_id, session=session, after=after)
        after = next_page_checker(data)
        for item in data['data']:
            yield item
