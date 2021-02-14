from warnings import warn
from .connections import getCommentData
from .exception import ModelRefreshWarning
from .parser import v_timestamp_parser


class Comment(object):
    __slots__ = ['_cached_data', '_comment_id', 'session']

    def __init__(self, commentId, init_data=None, session=None):
        self.session = session
        self._comment_id = commentId
        if init_data:
            self._cached_data = init_data
        else:
            self.refresh()

    def __repr__(self):
        return "<Comment [%s]>" % self._comment_id

    def refresh(self):
        res = getCommentData(commentId=self._comment_id, session=self.session, silent=True)
        if res:
            self._cached_data = res
        else:
            warn("Failed to refresh %s" % self, ModelRefreshWarning)

        # commentId = comment['commentId'],
        # author = comment['author'],
        # body = comment['body'],
        # sticker = comment['sticker'],
        # createdAt = comment['createdAt'],
        # commentCount = comment['commentCount'],
        # emotionCount = comment['emotionCount'],
        # isRestricted = comment['isRestricted'],
        # parent = comment['parent'],
        # root = comment['root']
    @property
    def commentId(self) -> str:
        return self._comment_id

    @property
    def author(self) -> dict:
        return self._cached_data['author']

    @property
    def author_nickname(self) -> str:
        return self._cached_data['author']['nickname']

    @property
    def author_memberId(self) -> str:
        return self._cached_data['author']['memberId']

    @property
    def body(self) -> str:
        return self._cached_data['body']

    @property
    def sticker(self) -> list:
        return self._cached_data['sticker']

    @property
    def created_at(self) -> float:
        return v_timestamp_parser(self._cached_data['createdAt'])

    @property
    def comment_count(self) -> int:
        return self._cached_data['commentCount']

    @property
    def emotion_count(self) -> int:
        return self._cached_data['emotionCount']

    @property
    def is_restricted(self) -> bool:
        return self._cached_data['isRestricted']

    @property
    def parent(self) -> dict:
        return self._cached_data['parent']

    @property
    def root(self) -> dict:
        return self._cached_data['root']

    @property
    def written_in(self) -> str:
        return self._cached_data['writtenIn']

    def parent_info_tuple(self):
        tp = self.parent['type']
        key = "%sId" % tp.lower()
        return self.parent['type'], self.parent['data'][key]

    def root_info_tuple(self):
        tp = self.root['type']
        key = "%sId" % tp.lower()
        return tp, self.root['data'][key]
